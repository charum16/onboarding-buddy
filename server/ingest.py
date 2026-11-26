"""Command-line ingestion: python ingest.py <file_path> [fixed_size|paragraph]"""
import asyncio
import sys

from app.core.config import DEFAULT_CHUNK_STRATEGY
from app.core.database import AsyncSessionLocal, close_db
from app.ingestor.chunker import Chunker
from app.repository.chunk_repo import ChunkRepo
from app.repository.document_repo import DocumentRepo
from app.utils.ai_provider import AIProvider


async def main(file_path: str, strategy: str) -> None:
    ai = AIProvider()
    async with AsyncSessionLocal() as db:
        documents = DocumentRepo(db)
        doc_id = await Chunker(documents, ChunkRepo(db, ai), ai).ingest(file_path, strategy)
        document = await documents.get_document(doc_id)
        print(f"Ingested {document.filename} as document {doc_id}")
    await close_db()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python ingest.py <file_path> [fixed_size|paragraph]")
    asyncio.run(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CHUNK_STRATEGY))
