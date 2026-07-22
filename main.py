from graph import graph

def main():
    thread = {"configurable": {"thread_id": "demo-1"}}
    while True:
        question = input("Ty: ")
        if question.strip().lower() in {"exit", "quit"}:
            break
        result = graph.invoke({"question": question}, config=thread)
        print("Bot:", result["answer"])


if __name__ == "__main__":
    main()

