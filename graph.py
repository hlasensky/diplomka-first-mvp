from pathlib import Path
from typing import Annotated, Literal, TypedDict

import duckdb
import yaml
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langchain_core.vectorstores import InMemoryVectorStore
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage
from langchain_huggingface import HuggingFaceEmbeddings



from pydantic import BaseModel

load_dotenv()

ROOT = Path(__file__).parent
SCHEMA = yaml.safe_load((ROOT / "schema" / "semantic_schema.yaml").read_text())

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0, max_tokens=1000)

all_db_categories = None
with duckdb.connect(database=str(ROOT / "data" / "olist.duckdb")) as conn:
    all_db_categories = conn.execute(
        "SELECT DISTINCT product_category_name FROM orders"
    ).fetchall()

cleaned_categories = [c[0].strip().replace("_", " ") for c in all_db_categories if c[0] is not None]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

vectorstore = InMemoryVectorStore.from_texts(
    cleaned_categories,
    embedding=embeddings,
    metadatas=[{"original": c[0]} for c in all_db_categories if c[0] is not None],
)


# hodnoty musí odpovídat klíčům v schema/semantic_schema.yaml
class Filters(BaseModel):
    metric: Literal["revenue", "orders", "avg_order_value", "cancellation_rate", "delivery_time"] | None = None
    dimension: Literal["category", "state", "seller", "time"] | None = None
    category_filter: str | None = None
    state_filter: str | None = None
    date_from: str | None = None
    date_to: str | None = None


class ChartSpec(BaseModel):
    chart_type: Literal["bar", "line"]
    x: str
    y: str
    title: str


class AgentState(TypedDict):
    # perzistentní - přežívá napříč tahy (díky checkpointeru)
    messages: Annotated[list[BaseMessage], add_messages]
    active_filters: Filters
    attempts: int

    # per-turn scratch
    question: str
    category_query_text: str | None
    category_candidates: list[tuple[str, float]] | None
    intent: Filters | None
    sql: str | None
    params: list | None
    validation_error: str | None
    needs_clarification: bool
    clarification_question: str | None
    columns: list[str]
    rows: list[tuple]

    # výstup
    chart_spec: ChartSpec | None
    answer: str

def user_input(state: AgentState) -> AgentState:
    """Vstupní uzel: zabalí `question` (z initial state při invoke()) do HumanMessage v historii."""
    return {"messages": [HumanMessage(content=state["question"])]}

def clarify_intent(state: AgentState) -> AgentState:
    """LLM rozparsuje otázku do `Filters` (sloučené s `active_filters` z minula).
    Nastaví `intent=None` + `needs_clarification`/`clarification_question`, když je dotaz nejednoznačný."""

    structured_llm = llm.with_structured_output(Filters)
    intent = structured_llm.invoke([
        SystemMessage(content=SCHEMA["system_prompt"]),
        HumanMessage(content=state["question"]),
    ])
    is_unclear = intent.metric is None

    return {
        "intent": intent,
        "needs_clarification": is_unclear,
        "clarification_question": "Mohl byste upřesnit co máte na mysli?" if intent.metric is None else None,
        "attempts": state.get("attempts", 0) if is_unclear else 0
    }

def basic_query(state: AgentState) -> AgentState:
    """Jednoduchá větev: metrika (+dimenze) je jasná, žádný fuzzy lookup není potřeba, jde rovnou na execute_query."""

    sql, params = build_sql(state["intent"])
    
    return {
        "sql": sql, 
        "params": params,
        "needs_clarification": False, 
        "clarification_question": None
    }

def complex_query(state: AgentState) -> AgentState:
    """Větev, kde je potřeba dořešit nejasnou referenci (např. kategorie napsaná volným textem) před sestavením SQL."""
    return {"category_query_text": state["intent"].category_filter}

def unclear_query(state: AgentState) -> AgentState:
    """Intent se nepodařilo rozpoznat ani po clarify_intent - ukončí tah a vrátí `clarification_question` uživateli."""
    
    if state["attempts"] >= 3:
        return {
            "needs_clarification": False,
            "clarification_question": "Omlouvám se, stále nerozumím vaší otázce."
        }
    return {
        "attempts": state["attempts"] + 1,
        "needs_clarification": True,
        "clarification_question": state["clarification_question"]
    }

def embedding_lookup(state: AgentState) -> AgentState:
    """Fuzzy matchne uživatelův text (např. "beauty products") na `product_category_name` (73 PT hodnot) přes embeddings, výsledek do `category_candidates`."""

    query = state["category_query_text"].strip().replace("_", " ")
    results = vectorstore.similarity_search_with_score(query, k=3)
    candidates = [(doc.metadata["original"], score) for doc, score in results]
    return {"category_candidates": candidates}


def improve_prompt(state: AgentState) -> AgentState:
    """Self-check: ověří, že resolved intent/SQL dává smysl; při problému zvýší `attempts` a vrátí ke clarify_intent (do limitu), jinak pokračuje na execute_query."""
    
    candidates_have_good_score = any(score > 0.5 for _, score in state["category_candidates"] or [])
    
    if not candidates_have_good_score:
        if state["attempts"] >= 3:
            return {
                "needs_clarification": False,
                "clarification_question": "Omlouvám se, stále nerozumím vaší otázce."
            }
        return {
            "attempts": state["attempts"] + 1,
            "needs_clarification": True,
            "clarification_question": "Mohl byste upřesnit co máte na mysli?"
        }
    
    intent = state["intent"].model_copy(update={"category_filter": state["category_candidates"][0][0]})
    
    
    sql, params = build_sql(intent)
    
    return {
        "intent": intent,
        "sql": sql,
        "params": params,
        "needs_clarification": False,
        "clarification_question": None,
    }



def execute_query(state: AgentState) -> AgentState:
    """Z `intent`/`active_filters` a schema/semantic_schema.yaml sestaví parametrizované SQL a spustí ho nad data/olist.duckdb -> columns/rows."""
    
    sql = state["sql"]
    params = state["params"]
        
    columns, rows = [], []
    error = None
    with duckdb.connect(database=str(ROOT / "data" / "olist.duckdb")) as conn:
        try:
            result = conn.execute(sql, params).fetchall()
            columns = [desc[0] for desc in conn.description]
            rows = result
        except Exception as e:
            error = str(e)

    
    return {
        "columns": columns,
        "rows": rows,
        "needs_clarification": False,
        "clarification_question": None,
        "validation_error": error
    }

def generate_response(state: AgentState) -> AgentState:
    """LLM shrne columns/rows do krátké NL odpovědi (`answer`); `ChartSpec` se odvodí deterministicky z intentu/columns."""

    has_error = state["validation_error"] is not None
    if has_error:
        return {
            "answer": f"Došlo k chybě při vykonávání dotazu: {state['validation_error']}",
            "chart_spec": None
        }

    columns = state["columns"]
    rows = state["rows"]
    intent = state["intent"]

    chart_spec = None
    if intent.dimension is not None and len(columns) == 2:
        chart_spec = ChartSpec(
            chart_type="line" if intent.dimension == "time" else "bar",
            x=columns[0],
            y=columns[1],
            title=SCHEMA["metrics"][intent.metric]["label"],
        )

    preview = "\n".join(str(dict(zip(columns, row))) for row in rows[:20])
    answer = llm.invoke(
        f"Otázka uživatele: {state['question']}\n\n"
        f"Výsledek dotazu (sloupce {columns}):\n{preview}\n\n"
        "Shrň výsledek stručně v češtině (1-3 věty), drž se čísel z dat výše, nic nevymýšlej. "
        "Peněžní částky jsou v brazilských reálech (BRL, R$), nikdy v korunách ani dolarech."
    ).content

    return {"answer": answer, "chart_spec": chart_spec}


# Conditional routing
def route_intent(state: AgentState) -> str:
    if state["intent"].metric is None:
        return "unclear"
    return "complex" if state["intent"].category_filter is not None else "basic"

def route_clarification(state: AgentState) -> str:
    if state["needs_clarification"]:
        return "user_input"
    return "execute_query"

# Helper functions
def build_sql(intent: Filters) -> tuple[str, list]:
    metric_sql = SCHEMA["metrics"][intent.metric]["sql"]
    select = [f"{metric_sql} AS {intent.metric}"]
    group_by = ""
    order_by = f"ORDER BY {intent.metric} DESC"
    limit = 20

    if intent.dimension is not None:
        dim_col = SCHEMA["dimensions"][intent.dimension]["column"]
        if intent.dimension == "time":
            # časová dimenze se agreguje po týdnech a řadí chronologicky, ne podle hodnoty metriky
            dim_expr = f"DATE_TRUNC('week', {dim_col})"
            select.insert(0, f"{dim_expr} AS {dim_col}")
            group_by = f"GROUP BY {dim_expr}"
            order_by = f"ORDER BY {dim_expr}"
            limit = 200
        else:
            select.insert(0, dim_col)
            group_by = f"GROUP BY {dim_col}"

    where_clauses, params = [], []
    if intent.category_filter:
        where_clauses.append("product_category_name = ?")
        params.append(intent.category_filter)
    if intent.state_filter:
        where_clauses.append("customer_state = ?")
        params.append(intent.state_filter)
    if intent.date_from:
        where_clauses.append("order_purchase_timestamp >= ?")
        params.append(intent.date_from)
    if intent.date_to:
        where_clauses.append("order_purchase_timestamp <= ?")
        params.append(intent.date_to)
    where = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    sql = f"SELECT {', '.join(select)} FROM {SCHEMA['table']} {where} {group_by} {order_by} LIMIT {limit}"
    return sql, params


workflow = StateGraph(AgentState)
workflow.add_node("user_input", user_input)
workflow.add_node("clarify_intent", clarify_intent)
workflow.add_node("basic_query", basic_query)
workflow.add_node("complex_query", complex_query)
workflow.add_node("unclear_query", unclear_query)
workflow.add_node("embedding_lookup", embedding_lookup)
workflow.add_node("improve_prompt", improve_prompt)
workflow.add_node("execute_query", execute_query)
workflow.add_node("generate_response", generate_response)


workflow.add_edge(START, "user_input")
workflow.add_edge("user_input", "clarify_intent")
workflow.add_conditional_edges("clarify_intent", route_intent, {
    "basic": "basic_query",
    "complex": "complex_query",
    "unclear": "unclear_query",
})

workflow.add_edge("basic_query", "execute_query")

workflow.add_edge("complex_query", "embedding_lookup")
workflow.add_edge("embedding_lookup", "improve_prompt")
workflow.add_conditional_edges("improve_prompt", route_clarification, {
    "user_input": "user_input",
    "execute_query": "execute_query",
})

workflow.add_edge("unclear_query", END)

workflow.add_edge("execute_query", "generate_response")
workflow.add_edge("generate_response", END)

checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(allowed_msgpack_modules=[("graph", "Filters"), ("graph", "ChartSpec")])
)
graph = workflow.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    graph.get_graph().draw_mermaid_png(output_file_path=str(ROOT / "graph.png"))
