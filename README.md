# 🎥 YouTube Chat-Bot

> **Chat with YouTube videos using Retrieval-Augmented Generation (RAG).**

YouTube Chat-Bot is an AI-powered application that allows users to interact with the transcript of a YouTube video through natural-language questions.

Instead of relying on the model's general knowledge, the application retrieves relevant portions of the video's transcript and uses them as context for generating an answer. This keeps responses grounded in the source material and reduces unsupported or hallucinated answers.

The application combines **YouTube transcript extraction, document chunking, vector search, semantic retrieval, optional contextual compression, and LLM-based generation** into an end-to-end RAG pipeline.

---

## ✨ Key Features

- 🎥 **YouTube Transcript Extraction**
  - Supports manually created transcripts.
  - Supports automatically generated transcripts.
  - Can translate available transcripts into English when required.

- ✂️ **Intelligent Text Chunking**
  - Splits long transcripts into manageable overlapping chunks.
  - Uses `RecursiveCharacterTextSplitter` for document segmentation.

- 🔎 **Semantic Vector Search**
  - Converts transcript chunks into embeddings using Hugging Face embeddings.
  - Stores and retrieves vectors through Pinecone.
  - Uses `video_id` metadata to isolate retrieval to the currently processed video.

- 🤖 **Grounded Question Answering**
  - Retrieves relevant transcript sections before generating an answer.
  - The LLM is instructed to answer from the retrieved transcript context.
  - If the required information is not available, the application avoids guessing.

- ⚙️ **Contextual Compression**
  - Optional LLM-based compression can reduce irrelevant information from retrieved chunks.
  - Useful when retrieved documents contain more context than the final prompt requires.

- 🖥️ **Streamlit Interface**
  - Simple browser-based interface.
  - No coding required after setup.
  - Process a video and ask questions directly from the UI.

- 🔐 **Environment-Based Configuration**
  - API keys and application settings are managed through environment variables.
  - Secrets are kept outside the source code.

---

# 🧠 How It Works

The application follows a standard Retrieval-Augmented Generation architecture:

```text
                    ┌─────────────────────┐
                    │    YouTube URL      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transcript Fetcher  │
                    │ youtube-transcript  │
                    │       -api           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Splitter     │
                    │ RecursiveCharacter  │
                    │  TextSplitter       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Embeddings       │
                    │ Hugging Face Model  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Pinecone       │
                    │    Vector Store     │
                    └──────────┬──────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Similarity Search │
                    │   + video_id filter │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Contextual          │
                    │ Compression         │
                    │    (Optional)        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     RAG Prompt      │
                    │ Transcript Context  │
                    │ + User Question     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Hugging Face     │
                    │        LLM          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Grounded Answer   │
                    └─────────────────────┘
```

### RAG Pipeline

```text
YouTube URL
     ↓
Transcript Extraction
     ↓
Transcript Cleaning
     ↓
Document Chunking
     ↓
Embedding Generation
     ↓
Pinecone Vector Storage
     ↓
User Question
     ↓
Similarity Retrieval
     ↓
Optional Contextual Compression
     ↓
Prompt Construction
     ↓
LLM Generation
     ↓
Transcript-Grounded Answer
```

---

# 📁 Project Structure

```text
YouTube-ChatBot/
│
├── app/
<<<<<<< HEAD
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
=======
│   ├── config.py
│   ├── main.py
│   ├── chain.py
│   ├── retriever.py
│   ├── vector_store.py
│   ├── text_splitter.py
│   ├── transcript_fetch.py
│   └── prompt.py
│
├── chatbot-env/              # Local virtual environment (git-ignored)
│
├── .env                      # Local environment variables (git-ignored)
├── .env.example              # Environment variable template
>>>>>>> f5b3923 (Update README)
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Streamlit application and user interface |
| `chain.py` | Video indexing and RAG chain construction |
| `retriever.py` | Retriever, LLM, and contextual compression configuration |
| `vector_store.py` | Pinecone connection, embeddings, and vector storage |
| `transcript_fetch.py` | YouTube URL parsing and transcript extraction |
| `text_splitter.py` | Transcript chunking configuration |
| `prompt.py` | Grounded RAG prompt definition |
| `config.py` | Centralized application configuration and environment validation |

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/amanshah362/YouTube-ChatBot.git
cd YouTube-ChatBot
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv chatbot-env
```

**Git Bash:**

```bash
source chatbot-env/Scripts/activate
```

**Command Prompt:**

```cmd
chatbot-env\Scripts\activate.bat
```

**PowerShell:**

```powershell
chatbot-env\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv chatbot-env
source chatbot-env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

Use `.env.example` as the template:

```bash
cp .env.example .env
```

For Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then configure the required variables.

### Environment Variables

| Variable | Required | Default | Description |
|---|:---:|---|---|
| `HF_TOKEN` | ✅ | — | Hugging Face access token |
| `PINECONE_API_KEY` | ✅ | — | Pinecone API key |
| `PINECONE_INDEX_NAME` | ❌ | `my-docs-index` | Pinecone index name |
| `PINECONE_CLOUD` | ❌ | `aws` | Pinecone cloud provider |
| `PINECONE_REGION` | ❌ | `us-east-1` | Pinecone region |
| `EMBEDDING_MODEL` | ❌ | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `LLM_REPO_ID` | ❌ | Project default | Hugging Face model repository |
| `RETRIEVER_TOP_K` | ❌ | `4` | Number of chunks retrieved |
| `USE_CONTEXTUAL_COMPRESSION` | ❌ | `false` | Enable contextual compression |
| `CHUNK_SIZE` | ❌ | `1000` | Maximum chunk size |
| `CHUNK_OVERLAP` | ❌ | `200` | Overlap between chunks |

### Example `.env`

```env
HF_TOKEN=your_huggingface_token
PINECONE_API_KEY=your_pinecone_api_key

PINECONE_INDEX_NAME=my-docs-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

RETRIEVER_TOP_K=4

USE_CONTEXTUAL_COMPRESSION=false

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

> ⚠️ **Security:** Never commit `.env` or API keys to GitHub. Make sure `.env` is included in `.gitignore`.

---

# ▶️ Running the Application

Navigate to the application directory:

```bash
cd app
```

Start Streamlit:

```bash
streamlit run main.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 🚀 Usage

### Step 1 — Enter a YouTube URL

Paste the URL of a YouTube video that has captions or transcripts available.

Example:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

### Step 2 — Process the Video

Click **Process Video**.

The application will:

1. Extract the video ID.
2. Retrieve the available transcript.
3. Translate the transcript to English when required.
4. Split the transcript into overlapping chunks.
5. Generate embeddings.
6. Store the vectors in Pinecone.
7. Associate each chunk with the corresponding `video_id`.

### Step 3 — Ask a Question

Enter a question related to the video.

Examples:

```text
What is the main topic of this video?
```

```text
Summarize the key points discussed in the video.
```

```text
What approach does the speaker recommend?
```

```text
What are the advantages mentioned in the video?
```

### Step 4 — Generate the Answer

The application retrieves the most relevant transcript chunks and passes them to the LLM as context.

The model then generates an answer based on the retrieved content.

If the requested information cannot be found in the available transcript context, the application is instructed not to fabricate an answer.

---

# 🔍 Retrieval Strategy

The application uses semantic similarity search rather than simple keyword matching.

Each transcript chunk is converted into a vector representation using the configured embedding model.

When the user asks a question:

```text
User Question
      ↓
Question Embedding
      ↓
Pinecone Similarity Search
      ↓
Relevant Transcript Chunks
      ↓
Optional Contextual Compression
      ↓
LLM
      ↓
Answer
```

### Video-Level Isolation

Each document is associated with metadata similar to:

```python
{
    "video_id": "VIDEO_ID",
    "chunk_index": 0,
    "source": "youtube"
}
```

The retriever uses the `video_id` metadata to ensure that a question is answered from the currently processed video's transcript rather than unrelated documents stored in the same vector index.

---

# ⚙️ Contextual Compression

Contextual compression is available as an optional retrieval enhancement.

Without compression:

```text
Question
   ↓
Similarity Search
   ↓
Top-K Chunks
   ↓
LLM
```

With compression enabled:

```text
Question
   ↓
Similarity Search
   ↓
Top-K Chunks
   ↓
LLM-Based Compression
   ↓
Relevant Content
   ↓
Final LLM
```

The compression stage attempts to remove information that is not useful for answering the current question.

### Enable Compression

Set:

```env
USE_CONTEXTUAL_COMPRESSION=true
```

### Performance Consideration

Contextual compression introduces additional LLM inference calls and therefore increases latency and potentially inference cost.

For faster development and testing, it is disabled by default.

---

# 🧩 Technology Stack

| Technology | Purpose |
|---|---|
<<<<<<< HEAD
| App hangs on "Process Video" | First-time embedding model download, or Pinecone index/network issue |
| App hangs on "Ask" | `USE_CONTEXTUAL_COMPRESSION=true` making multiple sequential LLM calls, or a slow/cold LLM endpoint |
| `Captions are disabled for this video` | The video has no transcript/captions available |
| `PINECONE_API_KEY is missing` / `HF_TOKEN is missing` | `.env` file not created or not in the `app/` working directory |
=======
| **Python** | Core application language |
| **LangChain** | RAG pipeline and orchestration |
| **Streamlit** | Web application interface |
| **Pinecone** | Vector database and similarity search |
| **Hugging Face** | Embeddings and LLM inference |
| **Sentence Transformers** | Transcript embeddings |
| **YouTube Transcript API** | Transcript extraction |
| **python-dotenv** | Environment configuration |

---

# 🏛️ Design Principles

### 1. Grounded Generation

The LLM is instructed to answer from retrieved source material rather than unrelated general knowledge.

### 2. Retrieval Before Generation

Relevant context is retrieved before the model generates an answer.

### 3. Metadata-Aware Retrieval

Documents are associated with a `video_id` so retrieval remains scoped to the selected video.

### 4. Configuration Through Environment Variables

API credentials and deployment-specific settings are separated from application code.

### 5. Modular Architecture

Each major stage of the pipeline is separated into its own module, making the application easier to test, maintain, and extend.

---

# ⚡ Performance Considerations

### First Run

The first execution may take longer because the embedding model may need to be downloaded and initialized locally.

Subsequent runs are typically faster once the model is cached.

### Pinecone

Network latency can affect indexing and retrieval performance because vector operations are performed against the Pinecone service.

### LLM Cold Starts

Some Hugging Face inference endpoints may experience increased latency during their first request due to model initialization or endpoint cold starts.

### Contextual Compression

Compression adds additional LLM calls and should therefore be enabled only when its retrieval-quality benefits justify the additional latency.

---

# 🛠️ Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Application does not start | Dependency/import issue | Verify the virtual environment and run `pip check` |
| `HF_TOKEN is missing` | Missing environment variable | Check `.env` configuration |
| `PINECONE_API_KEY is missing` | Missing Pinecone credentials | Add the key to `.env` |
| Transcript unavailable | Video has no accessible captions | Try a video with captions enabled |
| Processing is slow | Embedding model downloading | Allow the first download to complete |
| Pinecone request is slow | Network/API latency | Verify Pinecone configuration and connectivity |
| Question answering is slow | LLM inference latency | Check the Hugging Face endpoint |
| Compression is slow | Additional LLM calls | Disable `USE_CONTEXTUAL_COMPRESSION` |
| Poor retrieval | Chunking/retrieval configuration | Adjust `CHUNK_SIZE`, `CHUNK_OVERLAP`, or `RETRIEVER_TOP_K` |
| Answers say "I don't know" | Relevant information was not retrieved | Increase `RETRIEVER_TOP_K` or review chunking settings |

---

# 🔒 Security

This project requires external API credentials.

**Never hard-code credentials in Python files.**

Use:

```text
.env
```

and keep it excluded through:

```text
.gitignore
```

Recommended `.gitignore` entries:

```gitignore
.env
chatbot-env/
__pycache__/
*.pyc
.streamlit/
```

If an API key is accidentally committed to a public repository, **revoke and rotate the key immediately**.

---

# 🗺️ Future Improvements

Potential improvements include:

- [ ] Conversation memory for multi-turn discussions
- [ ] Streaming LLM responses
- [ ] Timestamp-aware transcript citations
- [ ] Source chunk visualization
- [ ] Multi-video collections
- [ ] Batch video processing
- [ ] Improved reranking
- [ ] Hybrid keyword + semantic retrieval
- [ ] Advanced document metadata
- [ ] Query rewriting
- [ ] RAG evaluation with dedicated evaluation datasets
- [ ] Automated retrieval-quality metrics
- [ ] Production deployment
- [ ] Authentication and user-specific video collections
- [ ] Background processing for large transcripts

---

# 📊 Example Workflow

```text
                    USER
                     │
                     │ YouTube URL
                     ▼
             ┌─────────────────┐
             │  Streamlit UI   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Transcript API  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │  Text Splitter  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │  HF Embeddings  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    Pinecone     │
             └────────┬────────┘
                      │
                      │ User Question
                      ▼
             ┌─────────────────┐
             │ Semantic Search │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   Compression   │
             │   (Optional)    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │       LLM       │
             └────────┬────────┘
                      │
                      ▼
                FINAL ANSWER
```

---

# 📌 Project Status

**Status: Active Development**

The project demonstrates an end-to-end RAG workflow for interacting with YouTube video transcripts.

The architecture is intentionally modular so additional retrieval, evaluation, memory, and deployment capabilities can be introduced without restructuring the entire application.

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

A typical contribution workflow:

```bash
git checkout -b feature/your-feature
```

Make your changes, test them locally, and open a pull request with a clear description of the changes.

For larger architectural changes, consider opening an issue first to discuss the proposed approach.

---

# 📄 License

This project is licensed under the **MIT License**.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to the conditions of the MIT License.

See the [`LICENSE`](LICENSE) file for the complete license text.

**Copyright © 2026 Aman Shah**

---

# 👨‍💻 Author

**Aman Shah**

Junior Data Scientist focused on:

- Machine Learning
- Deep Learning
- Generative AI
- Retrieval-Augmented Generation
- LangChain
- NLP
- Data Analytics

This project is part of my ongoing work in exploring practical **Generative AI and RAG systems** using modern LLM application frameworks.

---

## ⭐ Support the Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

Your feedback, suggestions, and contributions are welcome.
>>>>>>> f5b3923 (Update README)
