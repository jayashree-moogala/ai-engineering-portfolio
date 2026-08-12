from app.ingestion.embeddings import EmbeddingGenerator


def main():
    print("=" * 50)
    print("EMBEDDINGS TEST")
    print("=" * 50)

    embedder = EmbeddingGenerator()

    texts = [
        "FastAPI is a Python web framework.",
        "Employees receive 20 days of paid vacation each year.",
        "Artificial Intelligence is transforming software development."
    ]

    embeddings = embedder.embed_texts(texts)

    print(f"\nNumber of embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {len(embeddings[0])}")

    print("\nFirst 10 values of first embedding:")
    print(embeddings[0][:10])


if __name__ == "__main__":
    main()