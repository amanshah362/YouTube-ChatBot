# 🎥 YouTube Chat-Bot

A Retrieval-Augmented Generation (RAG) chatbot that lets you **chat with any YouTube video's transcript**. Paste a video URL, and ask questions about its content — the bot answers strictly from what's said in the video, not from general knowledge.

Built with **LangChain**, **Streamlit**, **Pinecone** (vector database), and **Hugging Face** (embeddings + LLM inference).

---

## ✨ Features

- 📝 Automatically fetches YouTube video transcripts (manual, auto-generated, or auto-translated to English)
- ✂️ Splits transcripts into overlapping chunks for better retrieval
- 🔎 Stores embeddings in **Pinecone**, scoped per video (`video_id` metadata filter)
- 🤖 Answers questions using a Hugging Face-hosted LLM, grounded only in retrieved transcript chunks
- ⚙️ Optional contextual compression (LLM re-ranks/trims retrieved chunks before answering)
- 🖥️ Simple Streamlit UI — no coding needed to use it

---

## 🏗️ Architecture

```
YouTube URL
     │
     ▼
transcript_fetch.py  →  fetch + clean transcript (youtube-transcript-api)
     │
     ▼
text_splitter.py     →  chunk transcript (RecursiveCharacterTextSplitter)
     │
     ▼
vector_store.py       →  embed chunks (HuggingFace) + upsert to Pinecone
     │
     ▼
retriever.py          →  similarity search scoped to video_id
     │                    (+ optional LLM-based contextual compression)
     ▼
prompt.py + chain.py  →  build context, prompt the LLM (chat_model)
     │
     ▼
main.py (Streamlit)   →  UI: process video → ask question → show answer
```

---

## 📁 Project Structure

```
YouTube-ChatBot/
├── app/
│   ├── config.py            # Centralized settings & env var validation
│   ├── main.py               # Streamlit UI entry point
│   ├── chain.py               # Indexing + RAG chain construction
│   ├── retriever.py           # Retriever + chat model setup
│   ├── vector_store.py        # Pinecone vector store (auto-creates index)
│   ├── text_splitter.py       # Transcript chunking config
│   ├── transcript_fetch.py    # YouTube transcript extraction
│   └── prompt.py               # RAG prompt template
├── chatbot-env/               # Virtual environment (git-ignored)
├── requirements.txt
├── .env                        # Your secrets (git-ignored, create this)
├── .env.example                # Template for required env vars
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/amanshah362/YouTube-ChatBot.git
cd YouTube-ChatBot
```

### 2. Create a virtual environment

```bash
python -m venv chatbot-env
```

Activate it:

- **Windows (Git Bash):** `source chatbot-env/Scripts/activate`
- **Windows (CMD):** `chatbot-env\Scripts\activate.bat`
- **macOS/Linux:** `source chatbot-env/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then fill in your keys:

| Variable | Required | Description |
|---|---|---|
| `HF_TOKEN` | ✅ | Hugging Face access token ([get one here](https://huggingface.co/settings/tokens)) |
| `PINECONE_API_KEY` | ✅ | Pinecone API key ([get one here](https://app.pinecone.io)) |
| `PINECONE_INDEX_NAME` | optional | Defaults to `my-docs-index`. Created automatically if it doesn't exist. |
| `PINECONE_CLOUD` / `PINECONE_REGION` | optional | Defaults to `aws` / `us-east-1` |
| `EMBEDDING_MODEL` | optional | Defaults to `sentence-transformers/all-MiniLM-L6-v2` |
| `LLM_REPO_ID` | optional | Hugging Face model repo used for answering |
| `RETRIEVER_TOP_K` | optional | How many chunks to retrieve per question (default `4`) |
| `USE_CONTEXTUAL_COMPRESSION` | optional | `true`/`false` — LLM trims retrieved chunks before answering (slower, one extra LLM call per chunk). Default `false`. |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | optional | Transcript splitting settings (defaults `1000` / `200`) |

> ⚠️ **Never commit your `.env` file.** It's already listed in `.gitignore`.

### 5. Run the app

```bash
cd app
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🚀 Usage

1. Paste a YouTube video URL (must have captions available).
2. Click **Process Video** — the transcript is fetched, chunked, and indexed into Pinecone.
3. Once processed, type a question about the video in the **Ask a question** box.
4. Click **Ask** — the bot retrieves relevant transcript chunks and answers using only that context.

If the answer isn't in the transcript, the bot will say so instead of guessing.

---

## 🐢 Performance Notes

- **First run is slower**: the embedding model (`sentence-transformers/all-MiniLM-L6-v2`) downloads from Hugging Face the first time it's used.
- **Contextual compression is off by default** because it makes one extra LLM call *per retrieved chunk* (up to `RETRIEVER_TOP_K` extra calls) before generating the final answer. Turn it on via `.env` only if you need higher-precision context and your LLM endpoint is fast enough.
- Large/less common Hugging Face models may have cold-start latency on first inference call — this is normal, not a bug.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [LangChain](https://www.langchain.com/) — RAG orchestration
- [Pinecone](https://www.pinecone.io/) — vector database
- [Hugging Face](https://huggingface.co/) — embeddings (`sentence-transformers`) + LLM inference endpoint
- [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) — transcript fetching

---

## 📄 License

This project is open source. Add a license of your choice (e.g. MIT) if you plan to share it publicly.

---

## 🙋 Troubleshooting

| Symptom | Likely Cause |
|---|---|
| App hangs on "Process Video" | First-time embedding model download, or Pinecone index/network issue |
| App hangs on "Ask" | `USE_CONTEXTUAL_COMPRESSION=true` making multiple sequential LLM calls, or a slow/cold LLM endpoint |
| `Captions are disabled for this video` | The video has no transcript/captions available |
| `PINECONE_API_KEY is missing` / `HF_TOKEN is missing` | `.env` file not created or not in the `app/` working directory |