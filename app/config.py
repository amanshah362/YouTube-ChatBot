"""
Centralized configuration for the YouTube Chat-Bot.

Every tunable value (model names, chunk sizes, retriever settings, etc.)
lives here so the rest of the codebase never hardcodes magic values.
Required secrets are validated once, at import time, so the app fails
fast with a clear message instead of hanging or crashing deep inside
a request.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def _require(value: str | None, name: str) -> str:
    if not value or not value.strip():
        raise ValueError(
            f"'{name}' is missing or empty. Please set it in your .env file."
        )
    return value


# Secrets

HF_TOKEN = _require(os.getenv("HF_TOKEN"), "HF_TOKEN")
PINECONE_API_KEY = _require(os.getenv("PINECONE_API_KEY"), "PINECONE_API_KEY")

# Pinecone

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "my-docs-index")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

# Embeddings
""" NOTE: EMBEDDING_DIMENSION must match the output size of EMBEDDING_MODEL.
all-MiniLM-L6-v2 -> 384. If you change the model, update the dimension too,
otherwise Pinecone index creation / upserts will fail with a dimension
mismatch error.
"""

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "384"))

# LLM (Hugging Face Inference Endpoint)

LLM_REPO_ID = os.getenv("LLM_REPO_ID", "zai-org/GLM-5.3-Flash")
LLM_MAX_NEW_TOKENS = int(os.getenv("LLM_MAX_NEW_TOKENS", "512"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))

# Retrieval
""" Contextual compression makes ONE extra LLM call per retrieved chunk.
With TOP_K=5 that is up to 5 extra sequential LLM calls before the final
answer call. Keep it off by default for speed; turn on only if answer
quality needs it and your LLM endpoint is fast enough.
"""

RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", "4"))
USE_CONTEXTUAL_COMPRESSION = os.getenv("USE_CONTEXTUAL_COMPRESSION", "false").lower() == "true"

# Text splitting

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

logger.info(
    "Config loaded | index=%s | llm=%s | top_k=%s | compression=%s",
    PINECONE_INDEX_NAME,
    LLM_REPO_ID,
    RETRIEVER_TOP_K,
    USE_CONTEXTUAL_COMPRESSION,
)