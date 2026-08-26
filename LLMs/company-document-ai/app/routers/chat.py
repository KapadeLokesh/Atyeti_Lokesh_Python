from __future__ import annotations

from fastapi import APIRouter

from app import llm_service
from app.schemas import ChatRequest, ChatResponse, SourceMetadata
from app.services import retrieval_service

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Answer a question using retrieved document context.

    The route fetches ranked chunks, removes duplicates, builds a context string,
    and asks the LLM to synthesize a concise natural-language answer. The final
    response only returns the answer text with lightweight source metadata.
    """
    context, sources = retrieval_service.retrieve_context(request.question, top_k=2)
    answer = llm_service.ask_llm(request.question, context)

    if answer == "I couldn't find that information in the uploaded documents.":
        return ChatResponse(answer=answer, sources=[])

    metadata = [SourceMetadata(**source) for source in sources]
    return ChatResponse(answer=answer, sources=metadata)


 