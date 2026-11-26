from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConverstionRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_conversation(self, convo_name: str) -> Conversation:
        conversation = Conversation(convo_name=convo_name)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def delete_conversation(self, conversation_id: int) -> bool:
        conversation = await self.get_conversation(conversation_id)
        if conversation is None:
            return False

        await self.db.delete(conversation)
        await self.db.commit()
        return True

    async def get_conversation(self, conversation_id: int) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def get_all_conversations(self) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation).order_by(Conversation.id)
        )
        return list(result.scalars().all())
