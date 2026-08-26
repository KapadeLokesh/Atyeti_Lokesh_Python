import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import (
    ColumnSelectionRequest,
    ColumnSelectionResponse,
    TabularChatRequest,
    TabularChatResponse,
)

from app.services.csv_service import CSVService
from app.services.encoding_service import EncodingService
from app.services.mapping_service import MappingService
from app.services.tabular_embedding_service import TabularEmbeddingService
from app.services.tabular_retrieval_service import TabularRetrievalService
from app.services.llm_service import ask_llm


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/tabular",
    tags=["Tabular"],
)


UPLOAD_DIRECTORY = Path("app/uploads/tabular")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
}


@router.post("/upload")
async def upload_tabular_file(
    file: UploadFile = File(...)
):
    """
    Upload a CSV or Excel file and return basic metadata.

    This endpoint only uploads and inspects the dataset.
    Embeddings and tokenization are NOT performed here.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    # Prevent path traversal and keep only the filename.
    filename = Path(file.filename).name

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and XLSX files are supported.",
        )

    destination = UPLOAD_DIRECTORY / filename

    try:

        # Save uploaded file.
        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # Read the dataset using Pandas.
        dataframe = CSVService.load_dataframe(
            destination
        )

        # Extract metadata.
        metadata = CSVService.get_metadata(
            dataframe=dataframe,
            filename=filename,
        )

        logger.info(
            "Tabular dataset uploaded successfully: %s",
            filename,
        )

        return metadata

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(
            "Upload failed for %s",
            filename,
        )

        # Remove partially uploaded file.
        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process uploaded file: {str(exc)}",
        ) from exc


@router.post(
    "/select-columns",
    response_model=ColumnSelectionResponse,
)
async def select_columns(
    request: ColumnSelectionRequest,
):
    """
    Select columns for tokenization.

    Workflow:

    Dataset
        ↓
    Validate columns
        ↓
    Encode selected columns
        ↓
    Save mappings
        ↓
    Save encoded dataset
        ↓
    Generate embeddings
        ↓
    Store in ChromaDB
    """

    dataset_path = (
        UPLOAD_DIRECTORY /
        Path(request.filename).name
    )

    # Check that the original dataset exists.
    if not dataset_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset not found: {request.filename}",
        )

    try:

        # Load original dataset.
        dataframe = CSVService.load_dataframe(
            dataset_path
        )

        # Validate selected columns.
        missing_columns = [
            column
            for column in request.columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "One or more selected columns do not exist.",
                    "missing_columns": missing_columns,
                    "available_columns": dataframe.columns.tolist(),
                },
            )

        if not request.columns:
            raise HTTPException(
                status_code=400,
                detail="At least one column must be selected.",
            )

        logger.info(
            "Selected columns for %s: %s",
            request.filename,
            request.columns,
        )

        # Tokenize selected columns.
        encoded_dataframe, mapping = (
            EncodingService.encode_dataframe(
                dataframe=dataframe,
                selected_columns=request.columns,
            )
        )

        # Save original → token mappings.
        MappingService.save_mapping(
            filename=request.filename,
            mapping=mapping,
        )

        # Save encoded dataset.
        CSVService.save_encoded_dataframe(
            filename=request.filename,
            dataframe=encoded_dataframe,
        )

        # Generate row embeddings and index them in ChromaDB.
        TabularEmbeddingService.index_dataframe(
            filename=request.filename,
            dataframe=encoded_dataframe,
        )

        logger.info(
            "Tabular dataset processed successfully: %s",
            request.filename,
        )

        return ColumnSelectionResponse(
            filename=request.filename,
            selected_columns=request.columns,
            total_selected=len(request.columns),
        )

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(
            "Column selection failed for %s",
            request.filename,
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process selected columns: {str(exc)}",
        ) from exc


@router.post(
    "/chat",
    response_model=TabularChatResponse,
)
async def tabular_chat(
    request: TabularChatRequest,
):
    """
    Ask a natural-language question about
    a processed CSV/Excel dataset.
    """

    try:

        context, sources = (
            TabularRetrievalService.retrieve_context(
                filename=request.filename,
                question=request.question,
                top_k=request.top_k,
            )
        )

        if not context:

            return TabularChatResponse(
                answer=(
                    "I couldn't find relevant information "
                    "in the uploaded dataset."
                ),
                sources=[],
            )

        # Reuse existing LLM service.
        from app.services.llm_service import ask_llm

        answer = ask_llm(
        request.question,
        context,
        tabular=True,
        )

        # Convert tokens back to original values.
        decoded_answer = (
            TabularRetrievalService.decode_answer(
                filename=request.filename,
                answer=answer,
            )
        )

        return TabularChatResponse(
            answer=decoded_answer,
            sources=sources,
        )

    except HTTPException:
        raise

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        logger.exception(
            "Tabular chat failed for %s",
            request.filename,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process tabular question.",
        ) from exc