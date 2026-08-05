from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class SourceMetadata(BaseModel):
    filename: str
    chunk: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceMetadata] = []


class SearchRequest(BaseModel):
    question: str
    top_k: int = 2


class SearchResponse(BaseModel):
    documents: list[list[str]]
    metadatas: list[list[dict[str, Any]]]