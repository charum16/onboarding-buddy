from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.models.document import Document
from app.utils.ai_provider import AIProvider


class ChunkRepo:
    def __init__(self, db: AsyncSession, ai: AIProvider) -> None:
        self.db = db
        self.ai = ai  # retrieve_chunks takes raw text, so the repo must embed it

    async def add_chunk(
        self, doc_id: int, content: str, page_num: int, embeddings: list[float]
    ) -> None:
        """pushes one chunk to the database"""
        self.db.add(
            Chunk(
                doc_id=doc_id,
                content=content,
                page_number=page_num,
                embedding=embeddings,
            )
        )
        await self.db.commit()

    async def add_chunks(
        self, doc_id: int, chunks: list[tuple[str, int, list[float]]]
    ) -> None:
        """pushes many (content, page_num, embedding) chunks in ONE transaction"""
        try:
            self.db.add_all(
                Chunk(doc_id=doc_id, content=content, page_number=page_num, embedding=embedding)
                for content, page_num, embedding in chunks
            )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def retrieve_chunks(self, text: str, top_k: int) -> list[dict]:
        """most similar chunks as {doc_name, page_number, content}"""
        # The embedding client is synchronous, so keep it off the event loop.
        query_embedding = await run_in_threadpool(self.ai.embedder, text)
        result = await self.db.execute(
            select(Chunk, Document.filename)
            .join(Document, Document.id == Chunk.doc_id)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )
        return [
            {"doc_name": filename, "page_number": chunk.page_number, "content": chunk.content}
            for chunk, filename in result.all()
        ]
