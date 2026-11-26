from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.conversation import Conversation
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    convo_name: str

class ConversationResponse(BaseModel):
    id: int
    convo_name: str
    model_config = ConfigDict(from_attributes=True)


def get_conversation_service(
    db: AsyncSession = Depends(get_db),
) -> ConversationService:
    return ConversationService(db)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    conversation: ConversationCreate,
    service: ConversationService = Depends(get_conversation_service),
) -> Conversation:
    return await service.create_conversation(conversation.convo_name)


@router.get("", response_model=list[ConversationResponse])
async def get_all_conversations(
    service: ConversationService = Depends(get_conversation_service),
) -> list[Conversation]:
    return await service.get_all_conversations()


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    service: ConversationService = Depends(get_conversation_service),
) -> Conversation:
    conversation = await service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    service: ConversationService = Depends(get_conversation_service),
) -> Response:
    deleted = await service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)