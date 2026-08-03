from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.llm_service import ask_llm

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Company Document AI Assistant Running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = ask_llm(request.question)

    return ChatResponse(
        answer=answer
    )

    