import json
import os


def save_chunks(
    filename: str,
    chunks: list
):
    os.makedirs(
        "app/data/chunks",
        exist_ok=True
    )

    output_file = os.path.join(
        "app/data/chunks",
        f"{filename}.json"
    )

    data = []

    for i, chunk in enumerate(chunks):

        data.append({
            "chunk_id": i,
            "text": chunk
        })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )