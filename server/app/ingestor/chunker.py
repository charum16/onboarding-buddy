from typing import Iterable, Iterator

from app.core.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.ingestor.ingestion_pipeline import IngestionPipeline


class Chunker(IngestionPipeline):
    def chunk_fixed_size(self, text: str) -> list[tuple[str, list[float]]]:
        step = CHUNK_SIZE - CHUNK_OVERLAP
        return self._embed_all(text[i : i + CHUNK_SIZE] for i in range(0, len(text), step))

    def chunk_paragraph(self, text: str) -> list[tuple[str, list[float]]]:
        return self._embed_all(self._pack_paragraphs(text.split("\n\n")))

    def _embed_all(self, pieces: Iterable[str]) -> list[tuple[str, list[float]]]:
        stripped = (piece.strip() for piece in pieces)
        return [(piece, self._ai.embedder(piece)) for piece in stripped if piece]

    @staticmethod
    def _pack_paragraphs(paragraphs: Iterable[str]) -> Iterator[str]:
        buffer = ""
        for paragraph in (p.strip() for p in paragraphs):
            if not paragraph:
                continue
            if buffer and len(buffer) + len(paragraph) + 2 > CHUNK_SIZE:
                yield buffer
                buffer = paragraph
            else:
                buffer = f"{buffer}\n\n{paragraph}" if buffer else paragraph
        if buffer:
            yield buffer
