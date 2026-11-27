from pathlib import Path
from typing import Callable

from fastapi.concurrency import run_in_threadpool
from pypdf import PdfReader

from app.core.config import DEFAULT_CHUNK_STRATEGY
from app.repository.chunk_repo import ChunkRepo
from app.repository.document_repo import DocumentRepo
from app.utils.ai_provider import AIProvider

ChunkFn = Callable[[str], list[tuple[str, list[float]]]]


class IngestionPipeline:
    def __init__(
        self, document_repo: DocumentRepo, chunk_repo: ChunkRepo, ai: AIProvider
    ) -> None:
        self._documents = document_repo
        self._chunks = chunk_repo
        self._ai = ai

    async def ingest(self, file_path: str, strategy: str = DEFAULT_CHUNK_STRATEGY) -> int:
        path = Path(file_path)
        chunk_fn = self._resolve_chunker(strategy)
        pages = await run_in_threadpool(self._read_pages, path)

        # Read, chunk and embed everything BEFORE touching the database,
        # so a failure here leaves nothing behind.
        rows = await run_in_threadpool(self._chunk_pages, pages, chunk_fn)
        if not rows:
            raise ValueError(f"No chunks produced from {path.name}")

        document = await self._documents.add_document(path.name)
        doc_id = document.id
        try:
            await self._chunks.add_chunks(doc_id, rows)
        except Exception:
            await self._documents.delete_document(doc_id)  # no orphan document
            raise
        return doc_id

    @staticmethod
    def _chunk_pages(
        pages: list[str], chunk_fn: ChunkFn
    ) -> list[tuple[str, int, list[float]]]:
        return [
            (content, page_number, embedding)
            for page_number, page_text in enumerate(pages, start=1)
            for content, embedding in chunk_fn(page_text)
        ]

    @staticmethod
    def _read_pages(path: Path) -> list[str]:
        if not path.is_file():
            raise FileNotFoundError(path)
        if path.suffix.lower() == ".pdf":
            pages = [page.extract_text() or "" for page in PdfReader(path).pages]
        else:
            pages = [path.read_text(encoding="utf-8")]
        if not any(page.strip() for page in pages):
            raise ValueError(f"No extractable text in {path.name}")
        return pages

    def _resolve_chunker(self, strategy: str) -> ChunkFn:
        chunker = getattr(self, f"chunk_{strategy}", None)
        if chunker is None:
            raise ValueError(f"Unknown chunking strategy: {strategy!r}")
        return chunker
