from app.ingestion.embeddings import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSStore


def main():
    print("=" * 50)
    print("VECTOR STORE TEST")
    print("=" * 50)

    chunks = [
        "Vacation Policy\nEmployees receive 20 days of paid vacation each year.",
        "Remote Work\nEmployees may work remotely up to three days per week.",
        "FastAPI is the preferred framework for building AI services."
    ]

    embedder = EmbeddingGenerator()
    embeddings = embedder.embed_texts(chunks)

    vector_store = FAISSStore(dimension=384)

    vector_store.add(embeddings, chunks)

    print("\nIndex created successfully.")

    print(f"Vectors stored: {vector_store.index.ntotal}")

    query = "How many vacation days do employees get?"

    query_embedding = embedder.embed_texts([query])[0]

    results = vector_store.search(query_embedding, k=2)

    print("\nTop Matches:\n")

    for i, result in enumerate(results, start=1):
        print(f"{i}. Score: {result['score']:.4f}")
        print(result["text"])
        print("-" * 60)


if __name__ == "__main__":
    main()