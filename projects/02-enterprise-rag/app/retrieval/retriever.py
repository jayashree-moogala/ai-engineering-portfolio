from app.ingestion.embeddings import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSStore


class Retriever:
    def __init__(self, vector_store: FAISSStore):
        self.vector_store = vector_store
        self.embedder = EmbeddingGenerator()

    def retrieve(self, query: str, k: int = 3):
        """
        Given a user query, return top-k most relevant chunks.
        """

        # 1. Convert query → embedding
        query_embedding = self.embedder.embed_texts([query])[0]

        # 2. Search FAISS index
        results = self.vector_store.search(query_embedding, k=k)

        return results