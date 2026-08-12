import faiss
import numpy as np
import pickle
import os


class FAISSStore:
    def __init__(self, dimension, index_path="index/faiss.index", meta_path="index/chunks.pkl"):
        self.dimension = dimension
        self.index_path = index_path
        self.meta_path = meta_path

        self.text_chunks = []

        # Try loading existing index
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            self.text_chunks = self._load_chunks()
            print("Loaded FAISS index from disk")
        else:
            self.index = faiss.IndexFlatL2(dimension)
            print("Created new FAISS index")

    def add(self, embeddings, chunks):
        self.index.add(np.array(embeddings).astype("float32"))
        self.text_chunks.extend(chunks)

    def search(self, query_embedding, k=3):
        query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx < len(self.text_chunks):
                results.append({
                    "text": self.text_chunks[idx],
                    "score": float(score)
                })

        return results

    def save(self):
        os.makedirs("index", exist_ok=True)

        faiss.write_index(self.index, self.index_path)
        self._save_chunks()

        print("FAISS index saved to disk")

    def _save_chunks(self):
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.text_chunks, f)

    def _load_chunks(self):
        with open(self.meta_path, "rb") as f:
            return pickle.load(f)