import time
import logging
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

import config

logger = logging.getLogger(__name__)

# Loading a local HuggingFace embedding model downloads it from the HF Hub
# the first time it runs. On a slow/restricted connection this can look
# exactly like a "stuck" app, so we log clearly around it.
logger.info("Loading embedding model '%s' (first run may download it)...", config.EMBEDDING_MODEL)
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
logger.info("Embedding model ready.")

pc = Pinecone(api_key=config.PINECONE_API_KEY)


def _ensure_index_exists() -> None:
    existing_names = {idx["name"] for idx in pc.list_indexes()}

    if config.PINECONE_INDEX_NAME in existing_names:
        logger.info("Pinecone index '%s' already exists.", config.PINECONE_INDEX_NAME)
        return

    logger.info(
        "Pinecone index '%s' not found. Creating it (dimension=%s)...",
        config.PINECONE_INDEX_NAME,
        config.EMBEDDING_DIMENSION,
    )

    pc.create_index(
        name=config.PINECONE_INDEX_NAME,
        dimension=config.EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud=config.PINECONE_CLOUD,
            region=config.PINECONE_REGION,
        ),
    )

    # Wait until Pinecone reports the index as ready before using it.
    while not pc.describe_index(config.PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

    logger.info("Pinecone index '%s' is ready.", config.PINECONE_INDEX_NAME)


_ensure_index_exists()

index = pc.Index(config.PINECONE_INDEX_NAME)

vector_store = PineconeVectorStore(embedding=embeddings, index=index)