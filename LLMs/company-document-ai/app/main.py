from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.routers.documents import router as document_router
from app.llm_service import ask_llm

app = FastAPI(title="Company Document AI")
app.include_router(document_router)

@app.get("/")
def home():
    return {"message": "Company Document AI Assistant"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = ask_llm(request.question)

    return ChatResponse(
        answer=answer # type: ignore
    )

