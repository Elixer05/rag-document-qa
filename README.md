# RAG Document Question Answering System

<<<<<<< HEAD
> Ask any question from a large academic PDF and get a context-grounded cited answer in seconds.
> Built with LanchChain, SentenceTransformers, cosine similarity retrieval, and a local phi3 LLM — **no API keys, no data leaving your machine.**
=======
> Ask any question from a 2000+ page academic textbook and get a context-grounded answer in seconds.
> Built with SentenceTransformers, cosine similarity retrieval, and a local phi3 LLM — **no API keys, no data leaving your machine.**
>>>>>>> 280d25f824af448ee62ec8c6f02a67a82b62b21f

---

## What It Does

This system lets you query large academic documents using natural language. Instead of searching for keywords, it understands the *meaning* of your question, retrieves the most relevant sections, and generates a precise answer grounded in the actual document content.

Built for academic textbooks but designed to work on any structured PDF document.

---

## Architecture

```
User Query
    │
    ▼
Streamlit Frontend (frontend.py)
    │
    ▼
Retrieval Module
    │
Chapter/Section Metadata Filter
    │
Cosine Similarity Search (threshold: 0.3)
    │
    ▼
Top-K Relevant Chunks (with source + location)
    │
    ▼
Prompt Construction
    │
    ▼
Local LLM (Ollama — phi3)
    │
    ▼
Context-Grounded Answer
```

**Pipeline:**
`PDF Ingestion → Chunking → Embedding → Indexed Storage → Retrieval → Generation`

---

## Key Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Chunk size | ~800 tokens with 150 overlap | Balances context preservation with retrieval precision |
| Embedding model | SentenceTransformers | Strong semantic similarity, runs locally without API |
| Similarity metric | Cosine similarity | Scale-invariant, effective for dense embeddings |
| Retrieval threshold | 0.3 minimum similarity | Filters noise while preserving recall |
| LLM | Ollama (phi3) | Fully local — no data leaves the machine |
| Text splitter | LangChain RecursiveCharacterTextSplitter | Intelligent boundary-aware chunking |
| Metadata filtering | Chapter/section aware | Allows scoped queries within specific document regions |

---

## Features

- Multi-PDF upload and processing via Streamlit sidebar
- Overlapping chunking (800 tokens, 150 overlap) for boundary-safe retrieval
- Semantic similarity ranking with configurable threshold
- Retrieved context viewer showing similarity scores per chunk
- Source-level citations — document name, page number, chapter, section
- Markdown table generation for comparisons and structured answers
- Conversation history with chat-style interface
- Fully local inference — works offline, no API costs
- Modular pipeline — each component is independently replaceable
- Embedding cache — avoid recomputation on repeated sessions
---

## Project Structure

```
rag-document-qa/
│
├── app.py            # CLI entry point and query loop
├── frontend.py       # Streamlit web interface
├── ingestion.py      # PDF loading and text extraction
├── chunking.py       # Overlapping token-based chunking with metadata
├── embedding.py      # SentenceTransformer embedding generation + caching
├── retrieval.py      # Cosine similarity search with threshold filtering
├── generation.py     # Prompt construction and Ollama LLM inference
│
├── data/             # Input documents (gitignored)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies

| Library | Purpose |
|---|---|
| `langchain` | Document loading and intelligent text splitting |
| `sentence-transformers` | Semantic embedding generation |
<<<<<<< HEAD
| `numpy` | Vector operations and cosine similarity |
| `ollama` | Local LLM inference (phi3) |
| `streamlit` | Web-based frontend interface |
| `pickle` | Embedding cache persistence |
=======
| `scikit-learn` | Cosine similarity computation |
| `numpy` | Vector operations |
| `phi3` | Local LLM inference  |

>>>>>>> 280d25f824af448ee62ec8c6f02a67a82b62b21f

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Elixer05/rag-document-qa.git
cd rag-document-qa

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Running the System

<<<<<<< HEAD
### Option 1 — Streamlit Web Interface (recommended)

**1. Start Ollama with phi3**
```bash
ollama run phi3
=======
**1. Start ollama phi3**
```bash
ollama pull phi3
>>>>>>> 280d25f824af448ee62ec8c6f02a67a82b62b21f
```

**2. Launch the Streamlit app**
```bash
streamlit run frontend.py
```

**3. Upload your PDFs**
Use the sidebar to upload one or more PDF files and click 
"Process Documents."

**4. Ask questions**
Type any question in the chat input and receive a cited, 
context-grounded answer.

---

### Option 2 — Command Line Interface

**1. Add your documents**
Place PDF files inside the `data/` directory.

**2. Run the application**
```bash
python app.py
```

**3. Ask questions**
```
Ask a question (or type 'quit' to exit): What is a PN junction diode?
```

---
## Future Improvements

- Cloud LLM integration (Groq API) for fully deployed version
- FAISS / ChromaDB vector database for scalable retrieval
- Hybrid search (BM25 + dense vectors) for improved recall
- Retrieval evaluation metrics (RAGAS — precision, faithfulness, recall@k)
- Voice query input via Faster-Whisper
- Support for multiple simultaneous document collections
---
## Limitations & Known Tradeoffs

<<<<<<< HEAD
- **Local LLM only** — generation requires Ollama running locally; 
  cloud deployment needs Groq or OpenAI API integration
- **Page number offset** — PyPDFLoader uses zero-based indexing; 
  displayed page numbers may be off by one from the actual PDF
- **Retrieval quality depends on chunk boundaries** — questions spanning 
  multiple sections may miss context
- **phi3 answer quality** is limited by model size; larger models would 
  improve generation quality
- **No hallucination detection** — answers are grounded in retrieved 
  context but not formally verified
=======
- **No persistent vector database** — embeddings are cached to disk but recomputed on new documents (FAISS integration planned)
- **Retrieval quality depends on chunk boundaries** — questions spanning multiple sections may miss context
- **phi3 answer quality** is limited by model size; larger models would improve generation
- **No hallucination detection** — answers are grounded in retrieved context but not formally verified

>>>>>>> 280d25f824af448ee62ec8c6f02a67a82b62b21f
---

## Author

**Ankita Kundu**
[GitHub](https://github.com/Elixer05) · [LinkedIn](https://linkedin.com/in/ankita-kundu)
