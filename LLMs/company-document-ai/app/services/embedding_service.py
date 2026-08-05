import hashlib
import math
import os
import re
from collections import Counter

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

EMBEDDING_DIMENSION = 256
client = chromadb.PersistentClient(path="app/data/chroma")
collection = client.get_or_create_collection(name="company_documents")


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def _deterministic_embedding(text: str) -> list[float]:
    tokens = _tokenize(text)
    if not tokens:
        return [0.0] * EMBEDDING_DIMENSION

    vector = [0.0] * EMBEDDING_DIMENSION
    counts = Counter(tokens)

    for token, count in counts.items():
        index = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16) % EMBEDDING_DIMENSION
        vector[index] += count

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude:
        vector = [value / magnitude for value in vector]

    return vector


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    return OpenAI(api_key=api_key)


def create_embedding(text: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _deterministic_embedding(text)

    try:
        openai_client = get_openai_client()
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception:
        return _deterministic_embedding(text)


def index_chunks(filename: str, chunks: list[str]):
    if not chunks:
        raise ValueError("No chunks provided for indexing")

    for index, chunk in enumerate(chunks):
        try:
            embedding = create_embedding(chunk)
            collection.add(
                ids=[f"{filename}_{index}"],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "filename": filename,
                    "chunk": index
                }]
            )
        except Exception as exc:
            raise RuntimeError(
                "Embedding indexing failed. Verify that OPENAI_API_KEY is valid and the embedding service is reachable."
            ) from exc


def _lexical_score(question: str, document: str) -> int:
    question_tokens = set(_tokenize(question))
    document_tokens = set(_tokenize(document))
    return len(question_tokens & document_tokens)


def _lexical_rerank(question: str, top_k: int = 3):
    all_items = collection.get(include=["documents", "metadatas"])
    documents = all_items.get("documents", []) or []
    metadatas = all_items.get("metadatas", []) or []

    ranked = []
    for index, document in enumerate(documents):
        score = _lexical_score(question, document)
        ranked.append((score, document, metadatas[index] if index < len(metadatas) else {}))

    ranked.sort(key=lambda item: item[0], reverse=True)
    top_items = ranked[:top_k]

    return {
        "documents": [[item[1] for item in top_items]],
        "metadatas": [[item[2] for item in top_items]]
    }


def search_chunks(question: str, top_k: int = 3):
    try:
        if collection.count() == 0:
            return {
                "documents": [],
                "metadatas": []
            }

        question_embedding = create_embedding(question)
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=top_k
        )

        documents = results.get("documents", []) or []
        metadatas = results.get("metadatas", []) or []

        if not documents and not metadatas:
            return {
                "documents": [],
                "metadatas": []
            }

        lexical_result = _lexical_rerank(question, top_k=top_k)
        lexical_documents = lexical_result.get("documents", [[]])
        lexical_metadatas = lexical_result.get("metadatas", [[]])

        if lexical_documents and lexical_documents[0]:
            return {
                "documents": lexical_documents,
                "metadatas": lexical_metadatas
            }

        return {
            "documents": documents,
            "metadatas": metadatas
        }
    except Exception:
        return {
            "documents": [],
            "metadatas": []
        }