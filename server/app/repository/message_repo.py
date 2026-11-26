from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_message(self, convo_id: int, message: str) -> None:
        self.db.add(Message(convo_id=convo_id, content=message))
        await self.db.commit()

    async def get_history(self, id: int, history_len: int) -> list[Message]:
        if history_len <= 0:
            return []

        result = await self.db.execute(
            select(Message)
            .where(Message.convo_id == id)
            .order_by(Message.id.desc())
            .limit(history_len)
        )
        return list(reversed(result.scalars().all()))

    async def get_messages(self, convo_id: int) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.convo_id == convo_id)
            .order_by(Message.id)
        )
        return list(result.scalars().all())