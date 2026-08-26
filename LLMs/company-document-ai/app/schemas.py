from typing import Any
from typing import List
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


class TabularUploadResponse(BaseModel):
    filename: str
    rows: int
    columns: List[str]


class ColumnSelectionRequest(BaseModel):
    filename: str
    columns: List[str]


class ColumnSelectionResponse(BaseModel):
    filename: str
    selected_columns: List[str]
    total_selected: int

class TabularChatRequest(BaseModel):
    filename: str
    question: str
    top_k: int = 3


class TabularChatResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]] = []