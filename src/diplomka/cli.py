"""Interactive command-line REPL for the analytics agent."""

from langchain_core.runnables import RunnableConfig

from diplomka.graph import get_graph


def main() -> None:
    graph = get_graph()
    thread: RunnableConfig = {"configurable": {"thread_id": "demo-1"}}
    while True:
        question = input("You: ")
        if question.strip().lower() in {"exit", "quit"}:
            break
        result = graph.invoke({"question": question}, config=thread)
        print("Bot:", result["answer"])


if __name__ == "__main__":
    main()
