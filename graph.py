from pathlib import Path
from typing import Annotated, Literal, TypedDict

import duckdb
import yaml
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langchain_core.vectorstores import InMemoryVectorStore
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage
from langchain_huggingface import HuggingFaceEmbeddings



from pydantic import BaseModel, Field, field_validator, model_validator

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


# metrics/dimension/granularity/fact/agg se validují dynamicky proti schema/semantic_schema.yaml,
# takže přidání nové metriky/dimenze/faktu vyžaduje úpravu jen YAML, ne téhle třídy.
class Filters(BaseModel):
    metrics: list[str] = Field(default_factory=list)
    # obecná (ne pojmenovaná) metrika: agregační funkce nad libovolným faktem ze SCHEMA["facts"]
    fact: str | None = None
    agg: str | None = None
    dimension: str | None = None
    granularity: str | None = None
    category_filter: str | None = None
    state_filter: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    # explicitní přání uživatele na typ grafu (jen když ho v otázce zmíní), jinak se dopočítá automaticky
    chart_type_request: Literal["bar", "line", "pie"] | None = None

    @field_validator("metrics")
    @classmethod
    def validate_metrics(cls, v: list[str]) -> list[str]:
        return [m for m in v if m in SCHEMA["metrics"]]

    @field_validator("fact")
    @classmethod
    def validate_fact(cls, v: str | None) -> str | None:
        return v if v in SCHEMA.get("facts", {}) else None

    @field_validator("agg")
    @classmethod
    def validate_agg(cls, v: str | None) -> str | None:
        return v if v in {"sum", "avg", "min", "max"} else None

    @model_validator(mode="after")
    def validate_fact_agg_pair(self) -> "Filters":
        if self.fact is not None and self.agg is not None:
            allowed = SCHEMA.get("facts", {}).get(self.fact, {}).get("agg", [])
            if self.agg not in allowed:
                self.fact = None
                self.agg = None
        return self

    @field_validator("dimension")
    @classmethod
    def validate_dimension(cls, v: str | None) -> str | None:
        return v if v in SCHEMA["dimensions"] else None

    @field_validator("granularity")
    @classmethod
    def validate_granularity(cls, v: str | None) -> str | None:
        valid = SCHEMA["dimensions"].get("time", {}).get("granularities", [])
        return v if v in valid else None

    def has_metric(self) -> bool:
        return bool(self.metrics) or (self.fact is not None and self.agg is not None)

    def resolve_metrics(self) -> list[dict]:
        """Vrátí seznam {sql, alias, label, additive, unit} pro všechny zvolené metriky (pojmenované i fact+agg)."""
        resolved = [
            {
                "sql": SCHEMA["metrics"][m]["sql"],
                "alias": m,
                "label": SCHEMA["metrics"][m]["label"],
                "additive": SCHEMA["metrics"][m].get("additive", False),
                "unit": SCHEMA["metrics"][m].get("unit", "value"),
            }
            for m in self.metrics
        ]
        if self.fact is not None and self.agg is not None:
            alias = f"{self.agg}_{self.fact}"
            resolved.append({
                "sql": f"{self.agg.upper()}({self.fact})",
                "alias": alias,
                "label": f"{self.agg.upper()} {self.fact}",
                "additive": self.agg == "sum",
                "unit": SCHEMA.get("facts", {}).get(self.fact, {}).get("unit", "value"),
            })
        if not resolved:
            raise ValueError("Filters nemá žádnou metriku ani validní `fact`+`agg` pár")
        return resolved


class ChartSpec(BaseModel):
    chart_type: Literal["bar", "line", "pie"]
    x: str
    y: list[str]
    y_units: list[str]
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
        *state["messages"]
    ])
    
    active_filters = state.get("active_filters", Filters())
    intent.metrics = intent.metrics or active_filters.metrics

    is_unclear = not intent.has_metric()

    return {
        "intent": intent,
        "needs_clarification": is_unclear,
        "clarification_question": "Mohl byste upřesnit co máte na mysli?" if is_unclear else None,
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
        message = "Omlouvám se, stále nerozumím vaší otázce."
        return {
            "needs_clarification": False,
            "clarification_question": message,
            "messages": [AIMessage(content=message)]
        }
    return {
        "attempts": state["attempts"] + 1,
        "needs_clarification": True,
        "clarification_question": state["clarification_question"],
        "messages": [AIMessage(content=state["clarification_question"])]
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
        "validation_error": error,
        "active_filters": state["intent"]
    }

def _intent_summary(intent: Filters) -> str:
    """Deterministický rekap resolved Filters pro AIMessage - vstup pro clarify_intent v dalším tahu."""
    metrics = ", ".join(intent.metrics) if intent.metrics else "-"
    fact_agg = f"{intent.agg} {intent.fact}" if intent.fact and intent.agg else "-"
    return (
        "[KONTEXT PŘEDCHOZÍHO TAHU - jen pro dořešení odkazů, NEKOPÍRUJ automaticky do nové otázky]\n"
        f"metriky: {metrics} | fact/agg: {fact_agg} | dimenze: {intent.dimension or '-'}\n"
        f"kategorie_filtr: {intent.category_filter or '-'} | stát_filtr: {intent.state_filter or '-'} | "
        f"období: {intent.date_from or '-'} až {intent.date_to or '-'}"
    )


def generate_response(state: AgentState) -> AgentState:
    """LLM shrne columns/rows do krátké NL odpovědi (`answer`); `ChartSpec` se odvodí deterministicky z intentu/columns."""

    has_error = state["validation_error"] is not None
    if has_error:
        return {
            "answer": f"Došlo k chybě při vykonávání dotazu: {state['validation_error']}",
            "chart_spec": None,
            "messages": [AIMessage(content="[Předchozí dotaz selhal chybou databáze - ignoruj tento kontext]")]
        }

    columns = state["columns"]
    rows = state["rows"]
    intent = state["intent"]

    chart_spec = None
    if intent.dimension is not None and len(columns) >= 2:
        metrics = intent.resolve_metrics()
        y_cols = columns[1:]

        if intent.chart_type_request is not None:
            chart_type = intent.chart_type_request
        elif intent.dimension == "time":
            chart_type = "line"
        elif len(metrics) == 1 and metrics[0]["additive"] and len(rows) <= 8:
            chart_type = "pie"
        else:
            chart_type = "bar"

        title = metrics[0]["label"] if len(metrics) == 1 else ", ".join(m["label"] for m in metrics)
        y_units = [m["unit"] for m in metrics]
        chart_spec = ChartSpec(chart_type=chart_type, x=columns[0], y=y_cols, y_units=y_units, title=title)

    preview = "\n".join(str(dict(zip(columns, row))) for row in rows[:20])
    answer = llm.invoke(
        f"Otázka uživatele: {state['question']}\n\n"
        f"Výsledek dotazu (sloupce {columns}):\n{preview}\n\n"
        "Shrň výsledek stručně v češtině (1-3 věty), drž se čísel z dat výše, nic nevymýšlej. "
        "Peněžní částky jsou v brazilských reálech (BRL, R$), nikdy v korunách ani dolarech. "
        "Odpověz čistým textem, žádný kód, žádné SQL, žádné bloky s ```."
    ).content

    return {
        "answer": answer,
        "chart_spec": chart_spec,
        "messages": [AIMessage(content=f"{_intent_summary(intent)}\n\nOdpověď uživateli: {answer}")]
    }


# Conditional routing
def route_intent(state: AgentState) -> str:
    if not state["intent"].has_metric():
        return "unclear"
    return "complex" if state["intent"].category_filter is not None else "basic"

def route_clarification(state: AgentState) -> str:
    if state["needs_clarification"]:
        return "user_input"
    return "execute_query"

# Helper functions
def build_sql(intent: Filters) -> tuple[str, list]:
    metrics = intent.resolve_metrics()
    select = [f"{m['sql']} AS {m['alias']}" for m in metrics]
    group_by = ""
    order_by = f"ORDER BY {metrics[0]['alias']} DESC"
    limit = 20

    if intent.dimension is not None:
        dim_col = SCHEMA["dimensions"][intent.dimension]["column"]
        if intent.dimension == "time":
            # časová dimenze se agreguje po týdnech (výchozí) a řadí chronologicky, ne podle hodnoty metriky
            granularity = intent.granularity or "week"
            dim_expr = f"DATE_TRUNC('{granularity}', {dim_col})"
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
    "user_input": "clarify_intent",  # user_input by jen znovu přidal identickou HumanMessage, nic nemění
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
