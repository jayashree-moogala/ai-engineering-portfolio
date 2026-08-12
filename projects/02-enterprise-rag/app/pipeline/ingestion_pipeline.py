from app.ingestion.document_loader import DocumentLoader
from app.ingestion.chunker import TextChunker
from app.ingestion.embeddings import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSStore


class IngestionPipeline:
    def __init__(self, documents_path: str):
        self.loader = DocumentLoader(documents_path)
        self.chunker = TextChunker()
        self.embedder = EmbeddingGenerator()

        # MiniLM produces 384-dimensional vectors
        self.vector_store = FAISSStore(dimension=384)

    def build_index(self):
        """
        Loads documents, chunks them, generates embeddings,
        and stores them in the FAISS index.
        """

        documents = self.loader.load_txt_files()

        all_chunks = []

        for document in documents:
            chunks = self.chunker.chunk_text(document["content"])
            all_chunks.extend(chunks)

        embeddings = self.embedder.embed_texts(all_chunks)

        self.vector_store.add(embeddings, all_chunks)
        self.vector_store.save()
        return self.vector_store