from __future__ import annotations
import hashlib
import hmac
import logging
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

TOKEN_SECRET: Final[str | None] = os.getenv(
    "TOKEN_SECRET_KEY"
)

if not TOKEN_SECRET:
    raise RuntimeError(
        "TOKEN_SECRET_KEY not configured."
    )


class EncodingService:
    """
    Enterprise deterministic tokenization service.
    """

    PREFIX_MAPPING: Final[dict[str, str]] = {
        "Employee Name": "EMP",
        "Department": "DEP",
        "City": "CITY",
        "Email": "EMAIL",
        "Phone": "PHONE",
    }

    @staticmethod
    def generate_token(
        value: str,
        column_name: str,
    ) -> str:
        """
        Generate deterministic token.
        """

        normalized = str(value).strip()

        prefix = (
            EncodingService.PREFIX_MAPPING.get(
                column_name,
                "TOK"
            )
        )

        digest = hmac.new(
            TOKEN_SECRET.encode(),
            normalized.encode(),
            hashlib.sha256,
        ).hexdigest()

        return (
            f"{prefix}_"
            f"{digest[:8].upper()}"
        )

    @staticmethod
    def encode_dataframe(
        dataframe,
        selected_columns: list[str],
    ):
        """
        Return encoded copy of dataframe.
        """

        encoded = dataframe.copy()

        mapping: dict = {}

        for column in selected_columns:

            mapping[column] = {}

            for value in (
                encoded[column]
                .astype(str)
                .unique()
            ):

                token = (
                    EncodingService
                    .generate_token(
                        value,
                        column
                    )
                )

                mapping[column][value] = token

            encoded[column] = (
                encoded[column]
                .astype(str)
                .map(mapping[column])
            )

        return encoded, mapping

    