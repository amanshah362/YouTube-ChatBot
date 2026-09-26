import logging
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from transcript_fetch import extract_video_id, get_english_transcript
from text_splitter import splitter
from vector_store import vector_store
from retriever import chat_model, get_compression_retriever
from prompt import prompt

logger = logging.getLogger(__name__)


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def index_video(url: str) -> tuple[str, int]:
    """
    Fetches a YouTube video's transcript, splits it, and upserts it into
    Pinecone under that video's ID. Returns (video_id, chunk_count).
    """

    video_id = extract_video_id(url)
    logger.info("Indexing video_id=%s", video_id)

    logger.info("Fetching transcript...")
    transcript = get_english_transcript(url)
    logger.info("Transcript fetched (%s characters).", len(transcript))

    logger.info("Splitting transcript into chunks...")
    chunks = splitter.create_documents([transcript])

    if not chunks:
        raise ValueError("No chunks were created from the transcript.")

    logger.info("%s chunks created.", len(chunks))

    for i, chunk in enumerate(chunks):
        chunk.metadata["video_id"] = video_id
        chunk.metadata["chunk_index"] = i
        chunk.metadata["source"] = url

    ids = [f"{video_id}_chunk_{i}" for i in range(len(chunks))]

    logger.info("Upserting %s chunks into Pinecone...", len(chunks))
    vector_store.add_documents(documents=chunks, ids=ids)
    logger.info("Indexing complete for video_id=%s.", video_id)

    return video_id, len(chunks)


def build_chain(video_id: str):
    """
    Builds a runnable chain that takes a question (str) and returns an
    answer (str), retrieving context only from the given video_id.
    """

    compression_retriever = get_compression_retriever(video_id)

    parallel_chain = RunnableParallel(
        {
            "context": compression_retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )

    rag_chain = parallel_chain | prompt | chat_model | StrOutputParser()

    return rag_chain