from functools import lru_cache

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.message import Message
from app.repository.chunk_repo import ChunkRepo
from app.repository.message_repo import MessageRepo
from app.retriever.retrieval_pipeline import RetrievalPipeline, RetrievalResult
from app.services.message_service import MessageService
from app.utils.ai_provider import AIProvider

router = APIRouter(
    prefix="/conversations/{convo_id}/messages",
    tags=["messages"],
)


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    convo_id: int
    content: str

    model_config = ConfigDict(from_attributes=True)


class RetrievedChunkResponse(BaseModel):
    doc_name: str
    page_number: int
    content: str


class MessageCreateResponse(BaseModel):
    response: str
    chunks: list[RetrievedChunkResponse]


@lru_cache
def get_ai() -> AIProvider:
    return AIProvider()


def get_message_service(
    db: AsyncSession = Depends(get_db),
) -> MessageService:
    return MessageService(db)


def get_retrieval_pipeline(
    db: AsyncSession = Depends(get_db),
    ai: AIProvider = Depends(get_ai),
) -> RetrievalPipeline:
    return RetrievalPipeline(ChunkRepo(db, ai), MessageRepo(db), ai)


@router.get("", response_model=list[MessageResponse])
async def get_messages(
    convo_id: int,
    service: MessageService = Depends(get_message_service),
) -> list[Message]:
    return await service.get_messages(convo_id)


@router.post("", response_model=MessageCreateResponse)
async def create_message(
    convo_id: int,
    message: MessageCreate,
    pipeline: RetrievalPipeline = Depends(get_retrieval_pipeline),
) -> RetrievalResult:
    return await pipeline.run(convo_id, message.content, history_len=10)
