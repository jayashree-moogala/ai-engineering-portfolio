from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import ask_llm


app = FastAPI(title="AI Chat Service")


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):
    try:
        answer = ask_llm(request.question)

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as ex:
        import traceback

        print("\n===== ERROR IN /ask ENDPOINT =====")
        print(type(ex).__name__)
        print(ex)
        traceback.print_exc()
        print("=================================\n")

        return {
            "question": request.question,
            "answer": f"Error: {str(ex)}"
        }