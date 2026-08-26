from __future__ import annotations

import logging

import chromadb
import pandas as pd

from app.services.embedding_service import create_embedding

logger = logging.getLogger(__name__)


# ==========================================================
# ChromaDB
# ==========================================================

client = chromadb.PersistentClient(
    path="app/data/chroma"
)


collection = client.get_or_create_collection(
    name="tabular_documents"
)


class TabularEmbeddingService:
    """
    Handles embedding generation and ChromaDB
    operations for CSV/Excel datasets.

    Each dataframe row is treated as one
    searchable document.

    Retrieval strategy:

    1. Exact token search is used when a sensitive
       token is available.

    2. Semantic/vector search is used as a fallback
       when no exact token is available.
    """

    # ======================================================
    # DATAFRAME → DOCUMENTS
    # ======================================================

    @staticmethod
    def dataframe_to_documents(
        dataframe: pd.DataFrame,
    ) -> list[str]:
        """
        Convert each dataframe row into
        searchable text.

        Example:

        DataFrame row:

        Employee Name = EMP_A7F29C4D
        Department    = DEP_71D99AA1
        City          = CITY_91AABB22
        Salary        = 50000

        becomes:

        Employee Name=EMP_A7F29C4D
        Department=DEP_71D99AA1
        City=CITY_91AABB22
        Salary=50000
        """

        if dataframe.empty:
            return []

        documents: list[str] = []

        for _, row in dataframe.iterrows():

            fields: list[str] = []

            for column, value in row.items():

                # Convert NaN/None into empty string.
                if pd.isna(value):
                    value = ""

                fields.append(
                    f"{column}={value}"
                )

            document = "\n".join(
                fields
            )

            documents.append(
                document
            )

        return documents

    # ======================================================
    # INDEX DATAFRAME
    # ======================================================

    @staticmethod
    def index_dataframe(
        filename: str,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Generate embeddings for every row
        and store them in ChromaDB.

        Each row is stored as one ChromaDB document.

        Sensitive values should already have been
        tokenized before this method is called.
        """

        if not filename:
            raise ValueError(
                "Filename is required."
            )

        if dataframe.empty:
            raise ValueError(
                "Cannot index an empty dataframe."
            )

        documents = (
            TabularEmbeddingService
            .dataframe_to_documents(
                dataframe
            )
        )

        if not documents:
            raise ValueError(
                "No documents generated from dataframe."
            )

        # --------------------------------------------------
        # Remove previous rows for this file.
        #
        # This prevents duplicate indexing when the same
        # dataset is processed again.
        # --------------------------------------------------

        try:

            collection.delete(
                where={
                    "filename": filename
                }
            )

        except Exception:

            logger.exception(
                "Failed to remove existing vectors for %s",
                filename,
            )

            raise

        # --------------------------------------------------
        # Generate embeddings
        # --------------------------------------------------

        for index, document in enumerate(
            documents
        ):

            try:

                embedding = create_embedding(
                    document
                )

                collection.add(
                    ids=[
                        f"tabular_{filename}_{index}"
                    ],
                    documents=[
                        document
                    ],
                    embeddings=[
                        embedding
                    ],
                    metadatas=[
                        {
                            "filename": filename,

                            # Keep the existing zero-based
                            # dataframe row index.
                            "row": index,
                        }
                    ],
                )

            except Exception as exc:

                logger.exception(
                    "Failed to index row %d from %s",
                    index,
                    filename,
                )

                raise RuntimeError(
                    f"Failed to index row {index} "
                    f"from {filename}."
                ) from exc

        logger.info(
            "%d rows indexed from %s",
            len(documents),
            filename,
        )

    # ======================================================
    # EXACT TOKEN SEARCH
    # ======================================================

    @staticmethod
    def search_exact(
        filename: str,
        token: str,
        top_k: int = 3,
    ) -> dict:
        """
        Search for an exact token inside the
        encoded ChromaDB documents.

        Example:

        token:

            EMP_A7F29C4D

        ChromaDB document:

            Employee Name=EMP_A7F29C4D
            Department=DEP_71D99AA1
            Role=Head of Delivery

        This method returns the row containing
        the exact token.

        Exact token search is preferred over
        semantic search because tokens are identifiers,
        not semantic concepts.
        """

        if not filename:
            raise ValueError(
                "Filename is required."
            )

        if not token or not token.strip():
            return {
                "documents": [],
                "metadatas": [],
            }

        if top_k < 1:
            top_k = 1

        token = token.strip()

        # --------------------------------------------------
        # Check whether the collection contains data.
        # --------------------------------------------------

        try:

            total_rows = collection.count()

            if total_rows == 0:

                logger.warning(
                    "Tabular collection is empty."
                )

                return {
                    "documents": [],
                    "metadatas": [],
                }

        except Exception as exc:

            logger.exception(
                "Failed to inspect ChromaDB."
            )

            raise RuntimeError(
                "Unable to access tabular ChromaDB."
            ) from exc

        # --------------------------------------------------
        # Exact document search.
        #
        # filename restricts the search to the requested
        # dataset.
        #
        # $contains searches the actual stored document
        # text rather than semantic similarity.
        # --------------------------------------------------

        try:

            results = collection.get(
                where={
                    "filename": filename
                },
                where_document={
                    "$contains": token
                },
                limit=top_k,
            )

        except Exception as exc:

            logger.exception(
                "Exact token search failed for %s",
                filename,
            )

            raise RuntimeError(
                f"Failed to search dataset {filename} "
                f"for token {token}."
            ) from exc

        documents = (
            results.get(
                "documents",
                [],
            )
            or []
        )

        metadatas = (
            results.get(
                "metadatas",
                [],
            )
            or []
        )

        logger.info(
            "Exact token search for %s found %d rows in %s",
            token,
            len(documents),
            filename,
        )

        return {
            "documents": documents,
            "metadatas": metadatas,
        }

    # ======================================================
    # SEMANTIC SEARCH
    # ======================================================

    @staticmethod
    def search_dataframe(
        filename: str,
        question: str,
        top_k: int = 3,
    ) -> dict:
        """
        Search the encoded tabular dataset
        using semantic similarity.

        This method is used when exact token
        retrieval is not available.

        The question should already have its
        sensitive values converted into tokens.
        """

        if not filename:
            raise ValueError(
                "Filename is required."
            )

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if top_k < 1:
            top_k = 1

        # --------------------------------------------------
        # Check whether this dataset exists
        # --------------------------------------------------

        try:

            total_rows = collection.count()

            if total_rows == 0:

                logger.warning(
                    "Tabular collection is empty."
                )

                return {
                    "documents": [],
                    "metadatas": [],
                }

        except Exception as exc:

            logger.exception(
                "Failed to inspect ChromaDB."
            )

            raise RuntimeError(
                "Unable to access tabular ChromaDB."
            ) from exc

        # --------------------------------------------------
        # Create embedding for the encoded question
        # --------------------------------------------------

        try:

            query_embedding = create_embedding(
                question
            )

        except Exception as exc:

            logger.exception(
                "Failed to create query embedding."
            )

            raise RuntimeError(
                "Unable to create query embedding."
            ) from exc

        # --------------------------------------------------
        # Search only inside requested dataset
        # --------------------------------------------------

        try:

            results = collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=top_k,
                where={
                    "filename": filename
                },
            )

        except Exception as exc:

            logger.exception(
                "ChromaDB semantic search failed for %s",
                filename,
            )

            raise RuntimeError(
                f"Failed to search dataset {filename}."
            ) from exc

        documents = (
            results.get(
                "documents",
                [],
            )
            or []
        )

        metadatas = (
            results.get(
                "metadatas",
                [],
            )
            or []
        )

        logger.info(
            "Retrieved %d result groups from %s",
            len(documents),
            filename,
        )

        return {
            "documents": documents,
            "metadatas": metadatas,
        }