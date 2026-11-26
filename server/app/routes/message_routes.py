from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.message import Message
from app.services.message_service import MessageService

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


def get_message_service(
    db: AsyncSession = Depends(get_db),
) -> MessageService:
    return MessageService(db)


@router.get("", response_model=list[MessageResponse])
async def get_messages(
    convo_id: int,
    service: MessageService = Depends(get_message_service),
) -> list[Message]:
    return await service.get_messages(convo_id)
