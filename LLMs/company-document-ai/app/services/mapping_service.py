from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MAPPING_DIRECTORY = Path("app/data/mappings")
MAPPING_DIRECTORY.mkdir(parents=True, exist_ok=True)


class MappingService:
    """
    Handles persistent storage and retrieval
    of deterministic token mappings.
    """

    @staticmethod
    def _mapping_path(filename: str) -> Path:
        """
        Build mapping file path.
        """

        return (
            MAPPING_DIRECTORY /
            f"{Path(filename).stem}_mapping.json"
        )

    @staticmethod
    def save_mapping(
        filename: str,
        mapping: dict[str, dict[str, str]],
    ) -> None:
        """
        Save mapping to disk.
        """

        output = MappingService._mapping_path(
            filename
        )

        with output.open(
            "w",
            encoding="utf-8"
        ) as fp:

            json.dump(
                mapping,
                fp,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def load_mapping(
        filename: str,
    ) -> dict[str, dict[str, str]]:

        mapping_file = (
            MappingService
            ._mapping_path(filename)
        )

        if not mapping_file.exists():

            raise FileNotFoundError(
                "Mapping file not found."
            )

        with mapping_file.open(
            "r",
            encoding="utf-8"
        ) as fp:

            return json.load(fp)

    @staticmethod
    def encode_query(
        filename: str,
        question: str,
    ) -> str:
        """
        Replace original values
        inside the question
        with tokens.
        """

        mapping = (
            MappingService
            .load_mapping(filename)
        )

        encoded = question

        for column in mapping.values():

            for original, token in (
                column.items()
            ):

                encoded = encoded.replace(
                    original,
                    token
                )

        return encoded

    @staticmethod
    def decode_text(
        filename: str,
        text: str,
    ) -> str:
        """
        Replace tokens
        with original values.
        """

        mapping = (
            MappingService
            .load_mapping(filename)
        )

        decoded = text

        for column in mapping.values():

            reverse = {
                token: original
                for original, token
                in column.items()
            }

            for token, original in (
                reverse.items()
            ):

                decoded = decoded.replace(
                    token,
                    original
                )

        return decoded