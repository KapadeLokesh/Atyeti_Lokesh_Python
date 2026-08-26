from __future__ import annotations

import json
from pathlib import Path

METADATA_DIRECTORY = Path("app/data/metadata")
METADATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


class MetadataService:
    """Stores metadata related to uploaded tabular datasets."""

    @staticmethod
    def save_selected_columns(
        filename: str,
        columns: list[str],
    ) -> None:

        output_file = (
            METADATA_DIRECTORY /
            f"{Path(filename).stem}_columns.json"
        )

        payload = {
            "filename": filename,
            "selected_columns": columns,
        }

        with output_file.open(
            "w",
            encoding="utf-8"
        ) as fp:

            json.dump(
                payload,
                fp,
                indent=4
            )

    @staticmethod
    def load_selected_columns(
        filename: str,
    ) -> list[str]:

        input_file = (
            METADATA_DIRECTORY /
            f"{Path(filename).stem}_columns.json"
        )

        if not input_file.exists():
            raise FileNotFoundError(
                "Column selection not found."
            )

        with input_file.open(
            "r",
            encoding="utf-8"
        ) as fp:

            payload = json.load(fp)

        return payload["selected_columns"]

        