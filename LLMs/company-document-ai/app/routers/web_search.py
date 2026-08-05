from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse
from app.llm_service import ask_llm

router = APIRouter(
    prefix="/web-search",
    tags=["Web Search AI"]
)


@router.post("/", response_model=ChatResponse)
def web_search(request: ChatRequest):

    try:
        answer = ask_llm(request.question)

        return ChatResponse(
            question=request.question,
            answer=answer
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )