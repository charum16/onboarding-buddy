import tempfile
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import DEFAULT_CHUNK_STRATEGY
from app.core.database import get_db
from app.ingestor.chunker import Chunker
from app.repository.chunk_repo import ChunkRepo
from app.repository.document_repo import DocumentRepo
from app.utils.ai_provider import AIProvider

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_SUFFIXES = {".pdf", ".txt", ".md"}


@lru_cache
def get_ai() -> AIProvider:
    """One AIProvider (and its HTTP clients) shared by every request."""
    return AIProvider()


def get_chunker(
    db: AsyncSession = Depends(get_db), ai: AIProvider = Depends(get_ai)
) -> Chunker:
    return Chunker(DocumentRepo(db), ChunkRepo(db, ai), ai)


@router.post("", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    strategy: str = DEFAULT_CHUNK_STRATEGY,
    chunker: Chunker = Depends(get_chunker),
) -> dict:
    # Path(...).name strips any directory part a client might send.
    filename = Path(file.filename or "").name
    if Path(filename).suffix.lower() not in ALLOWED_SUFFIXES:
        raise HTTPException(400, f"Only {sorted(ALLOWED_SUFFIXES)} files are supported")

    data = await file.read()
    # Saved under its real name because the pipeline stores path.name as the filename.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / filename
        path.write_bytes(data)
        try:
            doc_id = await chunker.ingest(str(path), strategy)
        except (ValueError, UnicodeDecodeError) as exc:
            raise HTTPException(400, str(exc)) from exc
    return {"document_id": doc_id, "filename": filename, "strategy": strategy}
