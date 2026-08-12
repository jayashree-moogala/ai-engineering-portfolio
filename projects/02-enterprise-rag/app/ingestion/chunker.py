#Using LangChain Text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    # with overlap, meaning is preserved.  
    # it does not split by character. It tries the separators in order Paragragh -> sentence -> word -> character
    # The overlap only happens when a chunk exceeds the configured chunk_size.
    def __init__(self, chunk_size: int = 150, chunk_overlap: int = 30):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_text(self, text: str):
        chunks = self.splitter.split_text(text)

        # 🔥 filter tiny junk chunks
        return [c.strip() for c in chunks if len(c.strip()) > 30]