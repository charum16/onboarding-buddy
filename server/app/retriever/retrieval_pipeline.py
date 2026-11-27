import json
from typing import Any, TypedDict

from app.utils.ai_provider import AIProvider
from app.repository.chunk_repo import ChunkRepo
from app.repository.message_repo import MessageRepo
from app.utils.prompts import Prompt
from fastapi.concurrency import run_in_threadpool


class RetrievalResult(TypedDict):
    response: str
    chunks: list[dict[str, Any]]


class RetrievalPipeline:
    def __init__(
        self,
        chunk_repo: ChunkRepo,
        message_repo: MessageRepo,
        ai: AIProvider | None = None,
    ) -> None:
        self.ai = ai if ai is not None else AIProvider()
        self.prompt = Prompt()
        self.chunk_repo = chunk_repo
        self.message_repo = message_repo

    async def run(
        self, convo_id: int, user_query: str, history_len: int = 10
    ) -> RetrievalResult:
        print("inside run")
        history = await self.message_repo.get_history(convo_id, history_len)
        print("fetched history")
        history_text = json.dumps(
            [message.content for message in history], ensure_ascii=False
        )
        print("rephrasing prompt")
        rephrase_prompt = self.prompt.rephraser(user_query, history_text)
        print("prompt rephrased")
        rephrased_query = await run_in_threadpool(self.ai.llm, rephrase_prompt)
        if rephrased_query is None:
            raise RuntimeError("LLM returned no rephrased query")
        print("got rephrased query")
        relevant_chunks = await self.chunk_repo.retrieve_chunks(rephrased_query, 3)
        print("got chunks")
        chunks_text = json.dumps(relevant_chunks, ensure_ascii=False)

        augmentation_prompt = self.prompt.augmenter(
            user_query, history_text, chunks_text
        )
        print("got aug prompt")
        response = await run_in_threadpool(self.ai.llm, augmentation_prompt)
        print("got response")
        if response is None:
            raise RuntimeError("LLM returned no response")

        await self.message_repo.add_message(convo_id, response)
        return {"response": response, "chunks": relevant_chunks}
