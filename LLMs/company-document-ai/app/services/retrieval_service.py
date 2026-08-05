from __future__ import annotations

from typing import Any

from app.services.embedding_service import search_chunks


def _flatten_results(results: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    """Flatten the nested Chroma payload into a single list of documents and metadata."""
    flat_documents: list[str] = []
    flat_metadata: list[dict[str, Any]] = []

    documents = results.get("documents", []) or []
    metadatas = results.get("metadatas", []) or []

    for document_group, metadata_group in zip(documents, metadatas):
        for document, metadata in zip(document_group, metadata_group):
            flat_documents.append(document)
            flat_metadata.append(metadata)

    return flat_documents, flat_metadata


def _dedupe_results(documents: list[str], metadatas: list[dict[str, Any]]) -> tuple[list[str], list[dict[str, Any]]]:
    """Remove duplicate chunks while preserving the first ranked match for each source."""
    unique_documents: list[str] = []
    unique_metadata: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()

    for document, metadata in zip(documents, metadatas):
        filename = metadata.get("filename", "unknown")
        chunk = metadata.get("chunk", -1)
        identity = (filename, chunk, document)
        if identity in seen:
            continue

        seen.add(identity)
        unique_documents.append(document)
        unique_metadata.append(metadata)

    return unique_documents, unique_metadata


def retrieve_context(question: str, top_k: int = 2) -> tuple[str, list[dict[str, Any]]]:
    """Return a clean context string and source metadata for the chat flow.

    The search service already performs similarity lookup. This wrapper normalizes the
    result, removes duplicate chunks, and keeps source metadata in a separate list.
    """
    results = search_chunks(question, top_k=top_k)
    documents, metadatas = _flatten_results(results)
    documents, metadatas = _dedupe_results(documents, metadatas)

    context = "\n\n".join(documents)
    sources = [
        {
            "filename": metadata.get("filename", "unknown"),
            "chunk": metadata.get("chunk", -1)
        }
        for metadata in metadatas
    ]

    return context, sources
