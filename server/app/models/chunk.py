from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import VECTOR

from app.core.database import Base

if TYPE_CHECKING:
    from .document import Document

class Chunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doc_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(VECTOR(1560), nullable=False)
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)

    document: Mapped["Document"] = relationship(back_populates="chunks")