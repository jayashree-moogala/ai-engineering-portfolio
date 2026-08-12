from app.rag_service import RAGService


def main():
    rag = RAGService("documents")

    question = "How many vacation days do employees get?"

    print("\n===== RAG FINAL TEST =====\n")
    print("Q:", question)
    print("\nA:\n")

    answer = rag.ask(question)
    print(answer)


if __name__ == "__main__":
    main()