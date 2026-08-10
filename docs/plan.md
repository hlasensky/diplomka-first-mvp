Perfect — this is the smartest approach for a master's thesis. One dataset, one use case, a working demo. Here is the concrete plan.

---

## Dataset: Olist Brazilian E-commerce

Use Olist — you have it mentioned in memory from earlier conversations and it's ideal because it's free on Kaggle, it has natural OLAP dimensions (time, product, category, state, seller), it contains order time series suitable for anomaly detection, and it's large enough for the demo to look real (~100k orders).

---

## One use case: Sales Performance Analysis

Specifically: the user asks about sales performance, navigates via OLAP operations, the system detects anomalies in the revenue time series and explains them in natural language with a chart.

Three demonstrable things for the defense:
- drill-down from category → product
- slice by state or time period
- revenue anomaly detection with a narrative explanation

---

## MVP architecture — what to drop, what to keep

Compared to the full architecture, the MVP drops Laravel Queue/WebSocket (synchronous HTTP is enough), Qdrant (a simple YAML directly in memory), the anomaly detector will be statistical (Z-score or IQR, not the full AXIS framework), and the frontend will be Chainlit instead of React+Laravel.

```
Chainlit (chat UI + Plotly charts as message elements)
    ↕ HTTP
FastAPI (LangGraph agent)
    ↕
DuckDB (Olist Parquet) + YAML semantic schema + Claude (Sonnet)
```

Three config files, no Docker needed for development, you can run it locally within an hour.

---

## MVP phases — 6 weeks

**Week 1 — data and schema**

Download Olist from Kaggle, load it into DuckDB as Parquet. Write the YAML semantic schema — define 5 metrics (revenue, orders, avg\_order\_value, cancellation\_rate, delivery\_time) and 4 dimensions (time, category, state, seller). This is the foundation of everything else.

```yaml
metrics:
  revenue:
    label: "Total revenue"
    sql: "SUM(payment_value)"
  orders:
    label: "Order count"
    sql: "COUNT(order_id)"

dimensions:
  category:
    label: "Product category"
    column: "product_category_name"
  state:
    label: "Customer state"
    column: "customer_state"
```

**Week 2 — LangGraph agent**

One state graph with three nodes: `parse_intent` (LLM decides which OLAP operation), `execute_query` (DuckDB via schema), `generate_response` (LLM explanation + chart spec). State holds the current filters and dimension.

I'll extend this with more nodes: prompt, rag, improve_prompt, clarify_intent, execute_query, generate_response, possibly more.

**Week 3 — Chainlit UI**

`@cl.on_message` wired to the LangGraph agent, a Plotly chart under each answer as a `cl.Plotly()` element, sidebar/starter messages with the current analysis state (active filters). A few hours of work if you know Python.

**Week 4 — OLAP operations**

Drill-down and slice as explicit tools (LangChain tools) that the agent calls. Test 10 conversational scenarios manually.

**Week 5 — anomalies**

Z-score over the weekly revenue time series. If Z > 2.5, the LLM gets the anomaly context and generates a narrative explanation. 30 lines of Python is enough.

**Week 6 — evaluation**

Prepare 20 test queries over the Olist data, measure OLAP operation accuracy (correct dimension? correct filter?). These are your numbers for the experimental chapter of the thesis.

---
