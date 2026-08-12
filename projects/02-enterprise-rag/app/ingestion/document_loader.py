from pathlib import Path


class DocumentLoader:
    def __init__(self, documents_path: str):
        self.documents_path = Path(documents_path)

    def load_txt_files(self):
        """
        Loads all .txt files from the documents directory.
        Returns a list of dictionaries:
        {
            "content": "...",
            "source": "filename.txt"
        }
        """

        documents = []

        # Find all text files in the folder
        for file_path in self.documents_path.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # metadata-aware RAG- auditability
                documents.append({
                    "content": content,
                    "source": file_path.name
                })

        return documents