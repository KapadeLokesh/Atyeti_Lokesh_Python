from pathlib import Path

import pandas as pd


class CSVService:

    @staticmethod
    def load_dataframe(
        file_path: Path,
    ) -> pd.DataFrame:

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension == ".csv":
            return pd.read_csv(file_path)

        if extension == ".xlsx":
            return pd.read_excel(file_path)

        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    @staticmethod
    def get_metadata(
        dataframe: pd.DataFrame,
        filename: str,
    ) -> dict:

        return {
            "filename": filename,
            "rows": len(dataframe),
            "columns": dataframe.columns.tolist(),
        }

    @staticmethod
    def save_encoded_dataframe(
        filename: str,
        dataframe: pd.DataFrame,
    ) -> Path:

        output_directory = Path(
            "app/data/encoded"
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_filename = Path(filename).name

        output_path = (
            output_directory /
            safe_filename
        )

        extension = output_path.suffix.lower()

        if extension == ".csv":

            dataframe.to_csv(
                output_path,
                index=False,
            )

        elif extension == ".xlsx":

            dataframe.to_excel(
                output_path,
                index=False,
            )

        else:

            raise ValueError(
                f"Unsupported file format: {extension}"
            )

        return output_path