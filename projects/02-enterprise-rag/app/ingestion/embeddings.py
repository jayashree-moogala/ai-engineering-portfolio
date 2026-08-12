from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    #constructor - 
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Lightweight, fast, production-friendlyembedding model - outputs 384-dimensional vectors
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]):
        """
        Converts a list of text chunks into embeddings.
        Returns a list of vectors.
        """

        embeddings = self.model.encode(texts)

        return embeddings