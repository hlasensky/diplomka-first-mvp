import datetime
import os
import re
from pathlib import Path
from typing import Annotated, Literal, TypedDict

import duckdb
import yaml
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
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

# "builder" = rigid semantic-layer builder (Filters + build_sql).
# "freesql"  = free Text-to-SQL: LLM emits raw read-only SQL from the injected schema.
SQL_MODE = os.getenv("SQL_MODE", "builder")

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0, max_tokens=1000)
#llm = ChatOllama(model="qwen2.5:14b", temperature=0)
#llm = ChatOllama(model="m/qwen2514bmax:latest", temperature=0)
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


# Skutečné schéma tabulky `orders` se načte dynamicky (DESCRIBE), ať se free-SQL prompt
# nemusí ručně synchronizovat s DDL. Používá se jen v režimu SQL_MODE="freesql".
with duckdb.connect(database=str(ROOT / "data" / "olist.duckdb"), read_only=True) as conn:
    ORDERS_COLUMNS = conn.execute(f"DESCRIBE {SCHEMA['table']}").fetchall()

_columns_block = "\n".join(f"  {name} {dtype}" for name, dtype, *_ in ORDERS_COLUMNS)


def _freesql_system_prompt() -> str:
    """System prompt pro free Text-to-SQL: obchodní kontext + reálné schéma tabulky + pravidla."""
    return (
        SCHEMA["freesql_system_prompt"]
        + f"\n\nTable `{SCHEMA['table']}` columns (name type):\n{_columns_block}\n"
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
    
    sql = state.get("sql")
    params = state.get("params") or []

    if not sql:
        return {
            "columns": [],
            "rows": [],
            "needs_clarification": False,
            "clarification_question": None,
            "validation_error": state.get("validation_error") or "Nepodařilo se sestavit SQL dotaz.",
        }

    columns, rows = [], []
    error = None
    # read_only=True: obrana do hloubky, LLM-generované SQL nesmí zapisovat do DB
    with duckdb.connect(database=str(ROOT / "data" / "olist.duckdb"), read_only=True) as conn:
        try:
            result = conn.execute(sql, params).fetchall()
            columns = [desc[0] for desc in conn.description]
            rows = result
        except Exception as e:
            error = str(e)

    updates = {
        "columns": columns,
        "rows": rows,
        "needs_clarification": False,
        "clarification_question": None,
        "validation_error": error,
    }
    # v builder režimu si pamatujeme resolved Filters pro navazující tahy; ve free-SQL režimu intent není
    if state.get("intent") is not None:
        updates["active_filters"] = state["intent"]
    return updates

def _intent_summary(intent: Filters) -> str:
    """Deterministic recap of resolved Filters for the AIMessage - fed to clarify_intent next turn."""
    metrics = ", ".join(intent.metrics) if intent.metrics else "-"
    fact_agg = f"{intent.agg} {intent.fact}" if intent.fact and intent.agg else "-"
    return (
        "[CONTEXT FROM PREVIOUS TURN - only for resolving references, do NOT copy automatically into a new question]\n"
        f"metrics: {metrics} | fact/agg: {fact_agg} | dimension: {intent.dimension or '-'}\n"
        f"category_filter: {intent.category_filter or '-'} | state_filter: {intent.state_filter or '-'} | "
        f"period: {intent.date_from or '-'} to {intent.date_to or '-'}"
    )


def _sql_recap(sql: str | None, answer: str) -> str:
    """Free-SQL recap: carry the last executed SQL so follow-ups can edit the prior query."""
    return (
        "[CONTEXT FROM PREVIOUS TURN - only for resolving follow-up references, do NOT blindly repeat]\n"
        f"Executed SQL:\n{sql or '-'}\n\n"
        f"Answer given to user: {answer}"
    )


def _heuristic_chart_spec(columns: list[str], rows: list[tuple]) -> ChartSpec | None:
    """Free-SQL režim: odvodí ChartSpec čistě z tvaru výsledku (bez intentu/sémantické vrstvy)."""
    if len(columns) < 2 or not rows:
        return None

    x = columns[0]
    y_cols = columns[1:]
    first_vals = [r[0] for r in rows]

    is_time = any(isinstance(v, (datetime.date, datetime.datetime)) for v in first_vals) or any(
        kw in x.lower() for kw in ("date", "time", "month", "year", "day", "week", "quarter")
    )

    def is_num(v) -> bool:
        return isinstance(v, (int, float)) and not isinstance(v, bool)

    single_numeric_y = len(y_cols) == 1 and all(len(r) > 1 and is_num(r[1]) for r in rows)

    if is_time:
        chart_type = "line"
    elif single_numeric_y and len(rows) <= 8:
        chart_type = "pie"
    else:
        chart_type = "bar"

    return ChartSpec(
        chart_type=chart_type,
        x=x,
        y=list(y_cols),
        y_units=["value"] * len(y_cols),
        title=", ".join(y_cols),
    )


def generate_response(state: AgentState) -> AgentState:
    """LLM shrne columns/rows do krátké NL odpovědi (`answer`); `ChartSpec` se odvodí z intentu (builder) nebo z tvaru výsledku (free-SQL)."""

    has_error = state["validation_error"] is not None
    if has_error:
        return {
            "answer": f"Došlo k chybě při vykonávání dotazu: {state['validation_error']}",
            "chart_spec": None,
            "messages": [AIMessage(content="[The previous query failed with a database error - ignore this context]")]
        }

    columns = state["columns"]
    rows = state["rows"]
    intent = state.get("intent")

    chart_spec = None
    if intent is not None:
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
    else:
        # free-SQL režim: bez intentu, odvodíme graf heuristicky z výsledku
        chart_spec = _heuristic_chart_spec(columns, rows)

    preview = "\n".join(str(dict(zip(columns, row))) for row in rows[:20])
    answer = llm.invoke(
        f"User question: {state['question']}\n\n"
        f"Query result (columns {columns}):\n{preview}\n\n"
        "Summarize the result briefly (1-3 sentences) in the same language as the user's question, "
        "stick to the numbers in the data above, invent nothing. "
        "Monetary amounts are in Brazilian reais (BRL, R$), never in crowns or dollars. "
        "Reply in plain text, no code, no SQL, no ``` blocks."
    ).content

    recap = _intent_summary(intent) if intent is not None else _sql_recap(state.get("sql"), answer)
    return {
        "answer": answer,
        "chart_spec": chart_spec,
        "messages": [AIMessage(content=recap)]
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


# ---- Free Text-to-SQL (SQL_MODE="freesql") ----

# pozn.: `replace`/`set` schválně NEjsou v blocklistu - jsou to běžné SQL funkce/klauzule
# (replace(), SELECT * REPLACE (...)); jednorázovost + start na SELECT/WITH stejně brání DML/DDL.
_FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|copy|pragma|"
    r"install|load|export|import|call|vacuum|truncate|grant|revoke)\b",
    re.IGNORECASE,
)


def ensure_read_only_select(sql: str) -> str:
    """Guardrail: povolí jen jeden read-only SELECT/WITH dotaz, jinak vyhodí ValueError.
    Připojí LIMIT 200, pokud dotaz žádný nemá. LLM-generované SQL nikdy nesmí zapisovat."""
    if not sql or not sql.strip():
        raise ValueError("prázdný SQL dotaz")

    cleaned = sql.strip().rstrip(";").strip()

    if ";" in cleaned:
        raise ValueError("povolen je jen jeden příkaz (žádné ';')")

    if not re.match(r"^(select|with)\b", cleaned, re.IGNORECASE):
        raise ValueError("povoleny jsou jen dotazy začínající SELECT nebo WITH")

    if _FORBIDDEN_SQL.search(cleaned):
        raise ValueError("dotaz obsahuje zakázané klíčové slovo (povolen je jen read-only SELECT)")

    if not re.search(r"\blimit\b", cleaned, re.IGNORECASE):
        cleaned += " LIMIT 200"

    return cleaned


@tool
def resolve_category(text: str) -> str:
    """Map a free-text product category description (e.g. in Czech or English) to the actual
    Portuguese `product_category_name` values stored in the database. Call this whenever the user
    refers to a product category by a common name and you need the exact DB value for a WHERE filter.
    Returns the top matching Portuguese category values."""
    query = text.strip().replace("_", " ")
    results = vectorstore.similarity_search_with_score(query, k=3)
    return ", ".join(doc.metadata["original"] for doc, _ in results)


@tool
def submit_sql(sql: str) -> str:
    """Submit the final, single read-only SQL SELECT query to run against the `orders` table.
    Call this exactly once when your query is ready."""
    return sql


_FREESQL_TOOLS = [resolve_category, submit_sql]
_llm_freesql = llm.bind_tools(_FREESQL_TOOLS)
_MAX_TOOL_ITERS = 5


def generate_sql_freeform(state: AgentState) -> AgentState:
    """Free Text-to-SQL uzel: LLM napíše raw read-only SQL, kategorie řeší přes `resolve_category`
    a finální dotaz předá přes `submit_sql`. Při chybě z execute_query se sem vrací s error feedbackem."""

    messages: list[BaseMessage] = [SystemMessage(content=_freesql_system_prompt()), *state["messages"]]

    is_retry = bool(state.get("validation_error") and state.get("sql"))
    if is_retry:
        messages.append(HumanMessage(content=(
            "The previous SQL failed. Fix it and submit corrected read-only SQL via submit_sql.\n"
            f"Previous SQL:\n{state['sql']}\n\nDatabase error: {state['validation_error']}"
        )))
    attempts = state.get("attempts", 0) + (1 if is_retry else 0)

    for _ in range(_MAX_TOOL_ITERS):
        ai = _llm_freesql.invoke(messages)
        messages.append(ai)

        tool_calls = getattr(ai, "tool_calls", None) or []
        if not tool_calls:
            # model odpověděl textem bez tool callu - popostrč ho k submit_sql
            messages.append(HumanMessage(content="Submit your SQL query using the submit_sql tool."))
            continue

        submitted = None
        for tc in tool_calls:
            if tc["name"] == "submit_sql":
                submitted = tc["args"].get("sql")
                messages.append(ToolMessage(content="received", tool_call_id=tc["id"]))
            elif tc["name"] == "resolve_category":
                result = resolve_category.invoke(tc["args"])
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            else:
                messages.append(ToolMessage(content="unknown tool", tool_call_id=tc["id"]))

        if submitted is not None:
            try:
                safe_sql = ensure_read_only_select(submitted)
                return {"sql": safe_sql, "params": [], "validation_error": None, "attempts": attempts}
            except ValueError as e:
                messages.append(HumanMessage(content=(
                    f"That SQL was rejected: {e}. Submit a corrected single read-only SELECT via submit_sql."
                )))

    return {
        "sql": None,
        "params": [],
        "validation_error": "Nepodařilo se vygenerovat platný SQL dotaz.",
        "attempts": attempts,
    }


def route_after_execute(state: AgentState) -> str:
    """Free-SQL self-correction: při DB chybě se vrať vygenerovat opravené SQL (do limitu pokusů)."""
    if state.get("validation_error") and state.get("attempts", 0) < 3:
        return "retry"
    return "respond"


def build_graph(mode: str = "builder"):
    """Sestaví a zkompiluje graf. mode="builder" = rigidní semantic-layer builder,
    mode="freesql" = free Text-to-SQL (LLM píše raw SQL)."""
    workflow = StateGraph(AgentState)
    workflow.add_node("user_input", user_input)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("generate_response", generate_response)
    workflow.add_edge(START, "user_input")
    workflow.add_edge("generate_response", END)

    if mode == "freesql":
        workflow.add_node("generate_sql_freeform", generate_sql_freeform)
        workflow.add_edge("user_input", "generate_sql_freeform")
        workflow.add_edge("generate_sql_freeform", "execute_query")
        workflow.add_conditional_edges("execute_query", route_after_execute, {
            "retry": "generate_sql_freeform",
            "respond": "generate_response",
        })
    else:
        workflow.add_node("clarify_intent", clarify_intent)
        workflow.add_node("basic_query", basic_query)
        workflow.add_node("complex_query", complex_query)
        workflow.add_node("unclear_query", unclear_query)
        workflow.add_node("embedding_lookup", embedding_lookup)
        workflow.add_node("improve_prompt", improve_prompt)

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

    checkpointer = InMemorySaver(
        serde=JsonPlusSerializer(allowed_msgpack_modules=[("graph", "Filters"), ("graph", "ChartSpec")])
    )
    return workflow.compile(checkpointer=checkpointer)


graph = build_graph(SQL_MODE)

if __name__ == "__main__":
    graph.get_graph().draw_mermaid_png(output_file_path=str(ROOT / "graph.png"))
