import os
from pathlib import Path
from dotenv import load_dotenv


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_FILE)

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "")

EMBEDDER_BASE_URL = os.getenv("EMBEDDER_BASE_URL", "")
EMBEDDER_API_KEY = os.getenv("EMBEDDER_API_KEY", "")
EMBEDDER_MODEL_NAME = os.getenv("EMBEDDER_MODEL_NAME", "")

DATABASE_URL = os.getenv("DATABASE_URL", "")