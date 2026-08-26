from __future__ import annotations

import logging
import re
from typing import Any

from app.services.mapping_service import MappingService
from app.services.tabular_embedding_service import (
    TabularEmbeddingService,
)

logger = logging.getLogger(__name__)


class TabularRetrievalService:
    """
    Retrieval service for the CSV/Excel RAG pipeline.

    Retrieval strategy:

    1. Detect mapped original values in the user's question.
    2. Matching is case-insensitive and whitespace-normalized.
    3. Convert detected values into deterministic tokens.
    4. Search ChromaDB using exact token matching.
    5. If no mapped value is detected, use semantic search.
    6. Decode retrieved rows before sending them to the LLM.
    7. Return source metadata.
    """

    # ==========================================================
    # TEXT NORMALIZATION
    # ==========================================================

    @staticmethod
    def normalize_text(
        text: str,
    ) -> str:
        """
        Normalize text for comparison.

        Examples:

            "Akshay Aher"
            "akshay aher"
            "AKSHAY AHER"
            "Akshay   Aher"

        all become:

            "akshay aher"
        """

        if not text:
            return ""

        text = str(text)

        # Replace multiple whitespace characters
        # with a single space.
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip().lower()

    # ==========================================================
    # ENCODE QUESTION
    # ==========================================================

    @classmethod
    def encode_question(
        cls,
        filename: str,
        question: str,
    ) -> str:
        """
        Replace known original values in the user's question
        with their deterministic tokens.

        Matching is:

        - case-insensitive
        - whitespace-normalized

        Example:

            Question:
                What is akshay   aher's role?

            Mapping:
                Akshay Aher -> TOK_E0559447

            Output:
                What is TOK_E0559447's role?
        """

        if not filename:
            raise ValueError(
                "Filename is required."
            )

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        mappings = MappingService.load_mapping(
            filename
        )

        if not mappings:

            logger.warning(
                "No mappings found for %s",
                filename,
            )

            return question

        encoded_question = question

        # ------------------------------------------------------
        # Build mapping list.
        # ------------------------------------------------------

        all_mappings: list[
            tuple[str, str]
        ] = []

        for column_mapping in mappings.values():

            if not isinstance(
                column_mapping,
                dict,
            ):
                continue

            for original_value, token in (
                column_mapping.items()
            ):

                if original_value is None:
                    continue

                if token is None:
                    continue

                original_text = str(
                    original_value
                ).strip()

                token_text = str(
                    token
                ).strip()

                if not original_text:
                    continue

                if not token_text:
                    continue

                all_mappings.append(
                    (
                        original_text,
                        token_text,
                    )
                )

        # ------------------------------------------------------
        # Longest original values first.
        #
        # This prevents:
        #
        # "Lokesh"
        #
        # from being replaced before:
        #
        # "Lokesh Gadiya"
        # ------------------------------------------------------

        all_mappings.sort(
            key=lambda item: len(item[0]),
            reverse=True,
        )

        # ------------------------------------------------------
        # Replace using normalized matching.
        #
        # We cannot simply call str.replace() because
        # whitespace/case may differ.
        # ------------------------------------------------------

        for original_value, token in all_mappings:

            normalized_original = (
                cls.normalize_text(
                    original_value
                )
            )

            if not normalized_original:
                continue

            # Build a regex that allows one or more
            # whitespace characters between words.
          

            words = normalized_original.split()

            escaped_words = [
                re.escape(word)
                for word in words
            ]

            pattern = r"\s+".join(
                escaped_words
            )

            try:

                encoded_question = re.sub(
                    pattern,
                    token,
                    encoded_question,
                    flags=re.IGNORECASE,
                )

            except re.error:

                logger.exception(
                    "Failed to replace mapping value '%s'",
                    original_value,
                )

        logger.info(
            "Question encoded for %s: %s",
            filename,
            encoded_question,
        )

        return encoded_question

    # ==========================================================
    # FIND TOKENS IN QUESTION
    # ==========================================================

    @classmethod
    def find_tokens_in_question(
        cls,
        filename: str,
        question: str,
    ) -> list[str]:
        """
        Find deterministic tokens corresponding to
        mapped original values present in the user's question.

        Matching is:

        - case-insensitive
        - whitespace-normalized

        Example:

            Question:
                What is AKSHAY   AHER's role?

            Mapping:
                Akshay Aher -> TOK_E0559447

            Result:

                ["TOK_E0559447"]
        """

        if not filename:
            raise ValueError(
                "Filename is required."
            )

        if not question or not question.strip():
            return []

        mappings = MappingService.load_mapping(
            filename
        )

        if not mappings:
            return []

        tokens: list[str] = []

        normalized_question = (
            cls.normalize_text(
                question
            )
        )

        # ------------------------------------------------------
        # Build mapping list.
        # ------------------------------------------------------

        all_mappings: list[
            tuple[str, str]
        ] = []

        for column_mapping in mappings.values():

            if not isinstance(
                column_mapping,
                dict,
            ):
                continue

            for original_value, token in (
                column_mapping.items()
            ):

                if original_value is None:
                    continue

                if token is None:
                    continue

                original_text = str(
                    original_value
                ).strip()

                token_text = str(
                    token
                ).strip()

                if not original_text:
                    continue

                if not token_text:
                    continue

                all_mappings.append(
                    (
                        original_text,
                        token_text,
                    )
                )

        # ------------------------------------------------------
        # Longest values first.
        # ------------------------------------------------------

        all_mappings.sort(
            key=lambda item: len(item[0]),
            reverse=True,
        )

        # ------------------------------------------------------
        # Find original values.
        # ------------------------------------------------------

        for original_value, token in all_mappings:

            normalized_original = (
                cls.normalize_text(
                    original_value
                )
            )

            if not normalized_original:
                continue

            # Exact normalized phrase search.
            if normalized_original in normalized_question:

                if token not in tokens:

                    tokens.append(
                        token
                    )

        logger.info(
            "Detected %d token(s) in question for %s: %s",
            len(tokens),
            filename,
            tokens,
        )

        return tokens

    # ==========================================================
    # DECODE DOCUMENT
    # ==========================================================

    @classmethod
    def decode_document(
        cls,
        filename: str,
        document: str,
    ) -> str:
        """
        Decode tokenized values inside a retrieved
        ChromaDB document.
        """

        if not document:
            return ""

        mappings = MappingService.load_mapping(
            filename
        )

        if not mappings:
            return document

        decoded_document = document

        # ------------------------------------------------------
        # Build token → original mapping.
        # ------------------------------------------------------

        reverse_mapping: dict[
            str,
            str,
        ] = {}

        for column_mapping in mappings.values():

            if not isinstance(
                column_mapping,
                dict,
            ):
                continue

            for original_value, token in (
                column_mapping.items()
            ):

                if original_value is None:
                    continue

                if token is None:
                    continue

                original_text = str(
                    original_value
                ).strip()

                token_text = str(
                    token
                ).strip()

                if not original_text:
                    continue

                if not token_text:
                    continue

                reverse_mapping[
                    token_text
                ] = original_text

        # ------------------------------------------------------
        # Longest tokens first.
        # ------------------------------------------------------

        sorted_tokens = sorted(
            reverse_mapping.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for token, original_value in sorted_tokens:

            if token in decoded_document:

                decoded_document = (
                    decoded_document.replace(
                        token,
                        original_value,
                    )
                )

        return decoded_document

    # ==========================================================
    # DECODE ANSWER
    # ==========================================================

    @classmethod
    def decode_answer(
        cls,
        filename: str,
        answer: str,
    ) -> str:
        """
        Decode any remaining tokens from the final
        LLM answer.
        """

        if not answer:
            return ""

        return cls.decode_document(
            filename=filename,
            document=answer,
        )

    # ==========================================================
    # BUILD CONTEXT
    # ==========================================================

    @classmethod
    def build_context(
        cls,
        filename: str,
        documents: list[str],
    ) -> str:
        """
        Convert retrieved ChromaDB documents into
        decoded context for the LLM.
        """

        if not documents:
            return ""

        context_parts: list[str] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            if not document:
                continue

            decoded_document = (
                cls.decode_document(
                    filename=filename,
                    document=document,
                )
            )

            if not decoded_document.strip():
                continue

            context_parts.append(
                f"Row {index}:\n"
                f"{decoded_document}"
            )

        return "\n\n".join(
            context_parts
        )

    # ==========================================================
    # RETRIEVE CONTEXT
    # ==========================================================

    @classmethod
    def retrieve_context(
        cls,
        filename: str,
        question: str,
        top_k: int = 3,
    ) -> tuple[
        str,
        list[dict[str, Any]],
    ]:
        """
        Hybrid retrieval pipeline.

        Flow:

            User Question
                  ↓
            Find mapped value
                  ↓
            Encode question
                  ↓
             Token found?
                /    \
              YES     NO
               ↓       ↓
          Exact search Semantic search
               ↓       ↓
               Retrieved rows
                    ↓
                  Decode
                    ↓
               Build context
                    ↓
                 ask_llm()
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

        logger.info(
            "Starting tabular retrieval for %s",
            filename,
        )

        # ------------------------------------------------------
        # STEP 1
        # Detect mapped original values.
        # ------------------------------------------------------

        tokens = (
            cls.find_tokens_in_question(
                filename=filename,
                question=question,
            )
        )

        # ------------------------------------------------------
        # STEP 2
        # Encode question.
        # ------------------------------------------------------

        encoded_question = (
            cls.encode_question(
                filename=filename,
                question=question,
            )
        )

        # ------------------------------------------------------
        # STEP 3
        # Exact token retrieval.
        # ------------------------------------------------------

        if tokens:

            logger.info(
                "Exact token retrieval selected "
                "for %s. Tokens=%s",
                filename,
                tokens,
            )

            flattened_documents: list[str] = []

            flattened_metadata: list[
                dict[str, Any]
            ] = []

            # --------------------------------------------------
            # Search each detected token.
            # --------------------------------------------------

            for token in tokens:

                result = (
                    TabularEmbeddingService
                    .search_exact(
                        filename=filename,
                        token=token,
                        top_k=top_k,
                    )
                )

                documents = (
                    result.get(
                        "documents",
                        [],
                    )
                    or []
                )

                metadatas = (
                    result.get(
                        "metadatas",
                        [],
                    )
                    or []
                )

                for index, document in enumerate(
                    documents
                ):

                    if not document:
                        continue

                    metadata: dict[
                        str,
                        Any,
                    ] = {}

                    if (
                        index < len(metadatas)
                        and isinstance(
                            metadatas[index],
                            dict,
                        )
                    ):

                        metadata = (
                            metadatas[index]
                        )

                    # ------------------------------------------
                    # Avoid duplicate rows.
                    # ------------------------------------------

                    current_filename = (
                        metadata.get(
                            "filename"
                        )
                    )

                    current_row = (
                        metadata.get(
                            "row"
                        )
                    )

                    duplicate = False

                    for existing_metadata in (
                        flattened_metadata
                    ):

                        if (
                            existing_metadata.get(
                                "filename"
                            )
                            == current_filename
                            and existing_metadata.get(
                                "row"
                            )
                            == current_row
                        ):

                            duplicate = True
                            break

                    if duplicate:
                        continue

                    flattened_documents.append(
                        str(document)
                    )

                    flattened_metadata.append(
                        metadata
                    )

        # ------------------------------------------------------
        # STEP 4
        # Semantic fallback.
        # ------------------------------------------------------

        else:

            logger.info(
                "No mapped value detected for %s. "
                "Using semantic search.",
                filename,
            )

            results = (
                TabularEmbeddingService
                .search_dataframe(
                    filename=filename,
                    question=encoded_question,
                    top_k=top_k,
                )
            )

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

            # --------------------------------------------------
            # Flatten documents.
            # --------------------------------------------------

            flattened_documents = []

            for group in documents:

                if isinstance(
                    group,
                    list,
                ):

                    for document in group:

                        if document:

                            flattened_documents.append(
                                str(document)
                            )

                elif group:

                    flattened_documents.append(
                        str(group)
                    )

            # --------------------------------------------------
            # Flatten metadata.
            # --------------------------------------------------

            flattened_metadata = []

            for group in metadatas:

                if isinstance(
                    group,
                    list,
                ):

                    for metadata in group:

                        if isinstance(
                            metadata,
                            dict,
                        ):

                            flattened_metadata.append(
                                metadata
                            )

                elif isinstance(
                    group,
                    dict,
                ):

                    flattened_metadata.append(
                        group
                    )

        # ------------------------------------------------------
        # STEP 5
        # Nothing retrieved.
        # ------------------------------------------------------

        if not flattened_documents:

            logger.info(
                "No documents retrieved for %s",
                filename,
            )

            return "", []

        # ------------------------------------------------------
        # STEP 6
        # Decode retrieved rows.
        # ------------------------------------------------------

        context = cls.build_context(
            filename=filename,
            documents=flattened_documents,
        )

        # ------------------------------------------------------
        # STEP 7
        # Build sources.
        # ------------------------------------------------------

        sources: list[
            dict[str, Any]
        ] = []

        for metadata in flattened_metadata:

            source_filename = (
                metadata.get(
                    "filename",
                    filename,
                )
            )

            row_number = (
                metadata.get(
                    "row"
                )
            )

            source: dict[str, Any] = {
                "filename": source_filename,
            }

            if row_number is not None:

                source["row"] = row_number

            sources.append(
                source
            )

        logger.info(
            "Retrieved %d rows for %s",
            len(flattened_documents),
            filename,
        )

        logger.debug(
            "Decoded tabular context:\n%s",
            context,
        )

        return context, sources

    # ==========================================================
    # BACKWARD COMPATIBILITY
    # ==========================================================

    @classmethod
    def retrieve(
        cls,
        filename: str,
        question: str,
        top_k: int = 3,
    ) -> tuple[
        str,
        list[dict[str, Any]],
    ]:
        """
        Backward-compatible alias for retrieve_context().
        """

        return cls.retrieve_context(
            filename=filename,
            question=question,
            top_k=top_k,
        )