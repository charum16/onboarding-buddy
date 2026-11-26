from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.repository.message_repo import MessageRepo


class MessageService:
    def __init__(self, db: AsyncSession) -> None:
        self.message_repo = MessageRepo(db)

    async def get_messages(self, convo_id: int) -> list[Message]:
        return await self.message_repo.get_messages(convo_id)