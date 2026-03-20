# RAG Document Question Answering System

> Ask any question from a 2000+ page academic textbook and get a context-grounded answer in seconds.
> Built with SentenceTransformers, cosine similarity retrieval, and a local Llama 2 LLM — **no API keys, no data leaving your machine.**

---

## What It Does

This system lets you query large academic documents using natural language. Instead of searching for keywords, it understands the *meaning* of your question, retrieves the most relevant sections, and generates a precise answer grounded in the actual document content.

Built for academic textbooks but designed to work on any structured PDF document.

---

## Demo

### Question: *"Define a BJT"*

**Retrieved:** 5 chunks from Chapters 3, 5, 7, 8 (similarity scores: 0.49 – 0.57)

**Answer:**
> A bipolar junction transistor (BJT) is a type of semiconductor device whose functioning involves both majority and minority charge carriers. It is a 3-layer device containing both types of semiconductor material (either in p-n-p or n-p-n form).

---

### Question: *"What are the characteristics of a BJT?"*

**Retrieved:** 5 chunks across Chapters 3, 7, 8 (top similarity: 0.59)

**Answer:**
> 1. **Three-terminal device** — Emitter (E), Collector (C), and Base (B)
> 2. **Majority and minority carriers** — involves both hole and electron flow
> 3. **Linear/active operating region** — current flows in proportion to applied voltage
> 4. **Stability factor (S)** — indicates degree of change in operating point due to temperature
> 5. **Forward-biased junction** — typically 0.6 to 0.7 V
> 6. **Leakage current** — present due to minority carriers

---

## Architecture

```
User Query
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
Local LLM (Ollama — Llama 2)
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
| LLM | Ollama (Llama 2) | Fully local — no data leaves the machine |
| Metadata filtering | Chapter/section aware | Allows scoped queries within specific document regions |

---

## Features

- **4,953 searchable chunks** indexed from 2000+ page textbooks
- Overlapping chunking (800 tokens, 150 overlap) for boundary-safe retrieval
- Chapter-aware metadata filtering before similarity search
- Cosine similarity ranking with configurable threshold
- Fully local inference — works offline, no API costs
- Modular pipeline — each component is independently replaceable

---

## Project Structure

```
rag-document-qa/
│
├── app.py            # Main entry point and query loop
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
| `sentence-transformers` | Semantic embedding generation |
| `scikit-learn` | Cosine similarity computation |
| `numpy` | Vector operations |
| `ollama` | Local LLM inference (Llama 2) |
| `PyMuPDF / pdfplumber` | PDF text extraction |

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

**1. Start Ollama with Llama 2**
```bash
ollama run llama2
```

**2. Add your documents**
Place PDF files inside the `data/` directory.

**3. Run the application**
```bash
python app.py
```

**4. Ask questions**
```
Ask a question (or type 'quit' to exit): What is a PN junction diode?
```

---
## Future Improvements

-  FAISS / ChromaDB vector database for scalable retrieval
-  Hybrid search (BM25 + dense vectors) for improved recall
-  Retrieval evaluation metrics (RAGAS — precision, faithfulness, recall@k)
-  Web interface (Streamlit / Gradio)
-  Support for multiple document collections

---
## Limitations & Known Tradeoffs

- **No persistent vector database** — embeddings are cached to disk but recomputed on new documents (FAISS integration planned)
- **Retrieval quality depends on chunk boundaries** — questions spanning multiple sections may miss context
- **Llama 2 answer quality** is limited by model size; larger models would improve generation
- **No hallucination detection** — answers are grounded in retrieved context but not formally verified

---


## Author

**Ankita Kundu**
[GitHub](https://github.com/Elixer05) · [LinkedIn](https://linkedin.com/in/ankita-kundu)
