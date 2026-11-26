import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import make_url

# server/app/core/config.py -> parents[2] is server/, where .env lives
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "")

EMBEDDER_BASE_URL = os.getenv("EMBEDDER_BASE_URL", "")
EMBEDDER_API_KEY = os.getenv("EMBEDDER_API_KEY", "")
EMBEDDER_MODEL_NAME = os.getenv("EMBEDDER_MODEL_NAME", "")

# Chunking (ingestion)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
DEFAULT_CHUNK_STRATEGY = os.getenv("DEFAULT_CHUNK_STRATEGY", "fixed_size")

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")


def _async_database_url(raw: str) -> str:
    """Turn the plain Neon URL from .env into one the asyncpg driver accepts.

    asyncpg rejects libpq options such as sslmode and channel_binding, and
    wants ssl=require instead.
    """
    if not raw:
        raise RuntimeError(f"DATABASE_URL is empty. Check {ENV_FILE}")
    url = make_url(raw).set(drivername="postgresql+asyncpg", query={"ssl": "require"})
    return url.render_as_string(hide_password=False)


DATABASE_URL = _async_database_url(os.getenv("DATABASE_URL", ""))
