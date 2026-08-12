from app.pipeline.ingestion_pipeline import IngestionPipeline


def main():
    print("\n===== INGESTION PIPELINE TEST =====\n")

    pipeline = IngestionPipeline("documents")

    vector_store = pipeline.build_index()

    print("Index built successfully!\n")

    print(f"Total chunks indexed: {len(vector_store.text_chunks)}")
    print(f"Vector dimension: {vector_store.dimension}")
    print(f"Vectors in FAISS index: {vector_store.index.ntotal}")


if __name__ == "__main__":
    main()