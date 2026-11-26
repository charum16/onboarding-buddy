import math

from openai import OpenAI
from app.core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME, EMBEDDER_API_KEY, EMBEDDER_BASE_URL, EMBEDDER_MODEL_NAME

# Must equal the VECTOR(n) size of document_chunks.embedding
EMBEDDING_DIM = 1560


def _fit_dimension(vector: list[float], dim: int) -> list[float]:
    """Safety net in case the server ignores `dimensions`.

    qwen3-embedding is trained for truncation (Matryoshka), so keeping the
    first `dim` values and re-normalising is a valid smaller embedding.
    Shorter than `dim` cannot be padded meaningfully, so that is an error.
    """
    if len(vector) < dim:
        raise ValueError(f"Embedder returned {len(vector)} dimensions, need at least {dim}")
    if len(vector) == dim:
        return vector
    cut = vector[:dim]
    norm = math.sqrt(sum(x * x for x in cut))
    return [x / norm for x in cut] if norm else cut


class AIProvider:
    def __init__(self):
        self.llm_client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
        self.embedding_client = OpenAI(base_url=EMBEDDER_BASE_URL, api_key=EMBEDDER_API_KEY)

    def llm(self, prompt: str):
        try:
            response = self.llm_client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages= [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                extra_headers={
                    "HTTP-Referer" : "https://localhost:3000",
                    "X-Title" : "incedo app",
                }
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error interacting with llm ({LLM_MODEL_NAME}): {str(e)}"

    def embedder(self, text: str):
        response = self.embedding_client.embeddings.create(
            model = EMBEDDER_MODEL_NAME,
            input=text,
            dimensions=EMBEDDING_DIM
        )
        return _fit_dimension(response.data[0].embedding, EMBEDDING_DIM)
