import logging
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
import config
from vector_store import vector_store

logger = logging.getLogger(__name__)

hf_llm = HuggingFaceEndpoint(
    repo_id=config.LLM_REPO_ID,
    task="text-generation",
    max_new_tokens=config.LLM_MAX_NEW_TOKENS,
    temperature=config.LLM_TEMPERATURE,
    huggingfacehub_api_token=config.HF_TOKEN,
    timeout=config.LLM_TIMEOUT_SECONDS,
)

chat_model = ChatHuggingFace(llm=hf_llm)


def get_compression_retriever(video_id: str):
    """
    Returns a retriever scoped to a single video_id.

    If USE_CONTEXTUAL_COMPRESSION is False (default), this returns a plain
    similarity retriever -- fast, one round-trip to Pinecone, no extra LLM
    calls. Set USE_CONTEXTUAL_COMPRESSION=true in .env if you want the LLM
    to trim irrelevant text out of each chunk before answering (slower,
    costs one LLM call per retrieved chunk).
    """

    base_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": config.RETRIEVER_TOP_K,
            "filter": {"video_id": video_id},
        },
    )

    if not config.USE_CONTEXTUAL_COMPRESSION:
        return base_retriever

    logger.info(
        "Contextual compression enabled: up to %s extra LLM calls per question.",
        config.RETRIEVER_TOP_K,
    )

    compressor = LLMChainExtractor.from_llm(chat_model)

    return ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor,
    )