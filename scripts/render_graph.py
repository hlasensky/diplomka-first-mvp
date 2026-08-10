"""Render the compiled LangGraph agent to graph.png (mermaid PNG)."""

from diplomka.config import GRAPH_PNG
from diplomka.graph import get_graph

if __name__ == "__main__":
    get_graph().get_graph().draw_mermaid_png(output_file_path=str(GRAPH_PNG))
    print(f"Wrote {GRAPH_PNG}")
