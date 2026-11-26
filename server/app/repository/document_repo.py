from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document


class DocumentRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_document(self, filename: str) -> Document:
        document = Document(filename=filename)
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def get_document(self, document_id: int) -> Document | None:
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def delete_document(self, document_id: int) -> bool:
        document = await self.get_document(document_id)
        if document is None:
            return False

        # Its chunks are removed too (relationship cascade + ON DELETE CASCADE).
        await self.db.delete(document)
        await self.db.commit()
        return True
