from app.pipeline.ingestion_pipeline import IngestionPipeline
from app.retrieval.retriever import Retriever


def main():
    print("\n===== RETRIEVER TEST =====\n")

    # 1. Build index
    pipeline = IngestionPipeline("documents")
    vector_store = pipeline.build_index()

    # 2. Create retriever
    retriever = Retriever(vector_store)

    # 3. Test query
    query = "How many vacation days do employees get?"

    print(f"Query: {query}\n")

    results = retriever.retrieve(query)

    print("Top Matches:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")


if __name__ == "__main__":
    main()