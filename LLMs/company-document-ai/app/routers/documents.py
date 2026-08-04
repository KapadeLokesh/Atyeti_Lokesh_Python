import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.storage_service import save_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])
UPLOAD_DIR = "app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    filename = file.filename
    if filename is None or not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDFs allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    chunks = chunk_text(
        extracted_text,
        chunk_size=500,
        overlap=100
    )

    save_chunks(
    file.filename,
    chunks)

    return {
        "filename": file.filename,
        "total_characters": len(extracted_text),
        "number_of_chunks": len(chunks),
        "first_chunk": chunks[0]
    }
