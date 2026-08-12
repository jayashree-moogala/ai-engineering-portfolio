from openai import OpenAI
from app.retrieval.retriever import Retriever
from app.pipeline.ingestion_pipeline import IngestionPipeline
from app.config import OPENAI_API_KEY, OPENAI_MODEL

# User → search → context → LLM → answer
class RAGService:
    def __init__(self, documents_path: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # Build index
        pipeline = IngestionPipeline(documents_path)
        self.vector_store = pipeline.build_index()

        # Retriever
        self.retriever = Retriever(self.vector_store)

    def ask(self, question: str):
        # 1. Retrieve
        results = self.retriever.retrieve(question)

        context_text = "\n\n".join([r["text"] for r in results])

        # 2. Prompt
        prompt = f"""
Use the context to answer the question.

Context:
{context_text}

Question:
{question}

Answer clearly:
"""

        # 3. LLM call
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            input=prompt
        )

        return {
            "answer": response.output_text,
            "sources": results
        }