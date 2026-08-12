from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_service import RAGService

app = FastAPI(title="Enterprise RAG Service")

# Initialize once (important for performance)
rag = RAGService("documents")


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=QuestionResponse)
def ask(req: QuestionRequest):
    try:
        result = rag.ask(req.question)

        return {
            "question": req.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise