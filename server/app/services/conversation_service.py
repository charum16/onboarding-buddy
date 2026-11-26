from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.repository.conversation_repo import ConverstionRepo


class ConversationService:
    def __init__(self, db: AsyncSession) -> None:
        self.conversation_repo = ConverstionRepo(db)

    async def create_conversation(self, convo_name: str) -> Conversation:
        return await self.conversation_repo.create_conversation(convo_name)

    async def get_conversation(self, conversation_id: int) -> Conversation | None:
        return await self.conversation_repo.get_conversation(conversation_id)

    async def get_all_conversations(self) -> list[Conversation]:
        return await self.conversation_repo.get_all_conversations()

    async def delete_conversation(self, conversation_id: int) -> bool:
        return await self.conversation_repo.delete_conversation(conversation_id)