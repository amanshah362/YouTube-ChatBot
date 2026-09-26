import logging
import streamlit as st
import config 
from chain import build_chain, index_video

logger = logging.getLogger(__name__)

# Page Configuration 

st.set_page_config(
    page_title="YouTube Chat-Bot",
    page_icon="🎥",
    layout="centered",
)

# Session State

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "video_url" not in st.session_state:
    st.session_state.video_url = None

# UI

st.title("🎥 YouTube Chat-Bot")
st.write("Ask questions about a YouTube video's transcript.")

url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
)

# Process Video

if st.button("Process Video", use_container_width=True):

    if not url.strip():
        st.warning("Please enter a YouTube video URL.")

    else:
        try:
            with st.spinner(
                "Fetching transcript and indexing video... "
                "(first run may take longer while models download)"
            ):
                video_id, chunk_count = index_video(url.strip())

            st.session_state.video_id = video_id
            st.session_state.video_url = url.strip()

            st.success(f"Video processed successfully. {chunk_count} chunks indexed.")

        except Exception as e:
            logger.exception("Failed to process video")
            st.error(f"Error: {str(e)}")

# Current Video Status

if st.session_state.video_id:
    st.info(f"Video ready: `{st.session_state.video_id}`. You can now ask questions.")

# Question

query = st.text_input(
    "Ask a question",
    placeholder="What is the main topic of this video?",
)

# Ask Question

if st.button("Ask", use_container_width=True):

    if not st.session_state.video_id:
        st.warning("Please process a YouTube video first.")

    elif not query.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Searching transcript and generating answer..."):
                chain = build_chain(st.session_state.video_id)
                answer = chain.invoke(query.strip())

            st.subheader("Answer")
            st.write(answer)

        except Exception as e:
            logger.exception("Failed to answer question")
            st.error(f"Error: {str(e)}")