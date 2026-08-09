from pathlib import Path
from typing import Annotated, Literal, TypedDict

import duckdb
import yaml
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

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

#llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0, max_tokens=1000)
llm = ChatOllama(model="qwen2.5:14b", temperature=0)
#llm = ChatOllama(model="qwen2.5:7b-instruct", temperature=0)


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


# metrics/dimension/granularity/fact/agg are validated dynamically against schema/semantic_schema.yaml,
# so adding a new metric/dimension/fact only requires editing the YAML, not this class.
class Filters(BaseModel):
    metrics: list[str] = Field(default_factory=list)
    # generic (unnamed) metric: aggregation function over any fact from SCHEMA["facts"]
    fact: str | None = None
    agg: str | None = None
    dimension: str | None = None
    granularity: str | None = None
    category_filter: str | None = None
    state_filter: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    # explicit user request for chart type (only when mentioned in the question), otherwise computed automatically
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
        """Return a list of {sql, alias, label, additive, unit} for all chosen metrics (named as well as fact+agg)."""
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
            raise ValueError("Filters has no metric nor a valid `fact`+`agg` pair")
        return resolved


class ChartSpec(BaseModel):
    chart_type: Literal["bar", "line", "pie"]
    x: str
    y: list[str]
    y_units: list[str]
    title: str


class AgentState(TypedDict):
    # persistent - survives across turns (thanks to the checkpointer)
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

    # output
    chart_spec: ChartSpec | None
    answer: str

def user_input(state: AgentState) -> AgentState:
    """Entry node: wraps `question` (from the initial state at invoke()) into a HumanMessage in the history."""
    return {"messages": [HumanMessage(content=state["question"])]}

def clarify_intent(state: AgentState) -> AgentState:
    """LLM parses the question into `Filters` (merged with `active_filters` from before).
    Sets `intent=None` + `needs_clarification`/`clarification_question` when the query is ambiguous."""

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
        "clarification_question": "Could you clarify what you mean?" if is_unclear else None,
        "attempts": state.get("attempts", 0) if is_unclear else 0
    }

def basic_query(state: AgentState) -> AgentState:
    """Simple branch: metric (+dimension) is clear, no fuzzy lookup needed, goes straight to execute_query."""

    sql, params = build_sql(state["intent"])
    
    return {
        "sql": sql, 
        "params": params,
        "needs_clarification": False, 
        "clarification_question": None
    }

def complex_query(state: AgentState) -> AgentState:
    """Branch where an ambiguous reference (e.g. a category written as free text) must be resolved before building SQL."""
    return {"category_query_text": state["intent"].category_filter}

def unclear_query(state: AgentState) -> AgentState:
    """Intent could not be recognized even after clarify_intent - ends the turn and returns `clarification_question` to the user."""

    if state["attempts"] >= 3:
        message = "Sorry, I still don't understand your question."
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
    """Fuzzy-matches the user's text (e.g. "beauty products") to `product_category_name` (73 PT values) via embeddings, result into `category_candidates`."""

    query = state["category_query_text"].strip().replace("_", " ")
    results = vectorstore.similarity_search_with_score(query, k=3)
    candidates = [(doc.metadata["original"], score) for doc, score in results]
    return {"category_candidates": candidates}


def improve_prompt(state: AgentState) -> AgentState:
    """Self-check: verifies the resolved intent/SQL makes sense; on a problem increments `attempts` and returns to clarify_intent (up to the limit), otherwise proceeds to execute_query."""

    candidates_have_good_score = any(score > 0.5 for _, score in state["category_candidates"] or [])

    if not candidates_have_good_score:
        if state["attempts"] >= 3:
            return {
                "needs_clarification": False,
                "clarification_question": "Sorry, I still don't understand your question."
            }
        return {
            "attempts": state["attempts"] + 1,
            "needs_clarification": True,
            "clarification_question": "Could you clarify what you mean?"
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
    """Builds parametrized SQL from `intent`/`active_filters` and schema/semantic_schema.yaml and runs it against data/olist.duckdb -> columns/rows."""
    
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
    """Deterministic recap of the resolved Filters for AIMessage - input for clarify_intent in the next turn."""
    metrics = ", ".join(intent.metrics) if intent.metrics else "-"
    fact_agg = f"{intent.agg} {intent.fact}" if intent.fact and intent.agg else "-"
    return (
        "[PREVIOUS TURN CONTEXT - only for resolving references, DO NOT automatically copy into the new question]\n"
        f"metrics: {metrics} | fact/agg: {fact_agg} | dimension: {intent.dimension or '-'}\n"
        f"category_filter: {intent.category_filter or '-'} | state_filter: {intent.state_filter or '-'} | "
        f"period: {intent.date_from or '-'} to {intent.date_to or '-'}"
    )


def generate_response(state: AgentState) -> AgentState:
    """LLM summarizes columns/rows into a short NL answer (`answer`); `ChartSpec` is derived deterministically from the intent/columns."""

    has_error = state["validation_error"] is not None
    if has_error:
        return {
            "answer": f"An error occurred while executing the query: {state['validation_error']}",
            "chart_spec": None,
            "messages": [AIMessage(content="[The previous query failed with a database error - ignore this context]")]
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
        f"User question: {state['question']}\n\n"
        f"Query result (columns {columns}):\n{preview}\n\n"
        "Summarize the result briefly in English (1-3 sentences), stick to the numbers from the data above, don't make anything up. "
        "Monetary amounts are in Brazilian reais (BRL, R$), never in korunas or dollars. "
        "Answer in plain text, no code, no SQL, no ``` blocks."
    ).content

    return {
        "answer": answer,
        "chart_spec": chart_spec,
        "messages": [AIMessage(content=f"{_intent_summary(intent)}\n\nAnswer to the user: {answer}")]
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
            # the time dimension is aggregated by week (default) and sorted chronologically, not by metric value
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
    "user_input": "clarify_intent",  # user_input would only re-add an identical HumanMessage, changes nothing
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
