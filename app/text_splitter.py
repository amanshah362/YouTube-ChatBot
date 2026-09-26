from langchain_text_splitters import RecursiveCharacterTextSplitter

import config

splitter = RecursiveCharacterTextSplitter(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP,
)