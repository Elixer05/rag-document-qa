# Retrieval-Augmented Generation (RAG) Document Question Answering

A **Retrieval-Augmented Generation (RAG)** system that performs semantic search over multi-chapter academic documents and generates context-grounded answers using a local LLM.

The system retrieves relevant sections from textbook content and uses them as context for answer generation.

---

## Architecture

PDF Documents → Chunking → Embeddings → Retrieval → LLM Generation

1. Documents are split into overlapping chunks.
2. Each chunk is converted into a semantic embedding.
3. Relevant chunks are retrieved using cosine similarity.
4. Retrieved context is passed to a local LLM to generate answers.

Flow:
## Architecture

```
                User Query
                     │
                     ▼
              Retrieval Module
                     │
          Cosine Similarity Search
                     │
                     ▼
           Relevant Document Chunks
                     │
                     ▼
           Prompt Construction
                     │
                     ▼
          LLM (Ollama - Llama3)
                     │
                     ▼
                Final Answer
```

---

## Features

* Document chunking (~800 token segments with overlap)
* Chapter-aware metadata filtering before retrieval
* Semantic search using dense vector embeddings
* Cosine similarity ranking for relevant context retrieval
* Context-grounded answer generation using a local LLM

---

## Technologies Used

* Python 3.x
* NumPy
* scikit-learn (cosine similarity)
* Transformer-based embedding model (SentenceTransformers)
* Local LLM using Ollama (Llama 2)

---

## Project Structure

```
rag-document-qa
│
├── app.py
├── ingestion.py
├── chunking.py
├── embedding.py
├── retrieval.py
├── generation.py
│
├── data/          # input documents (ignored in git)
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository

```
git clone https://github.com/yourusername/rag-document-qa.git
cd rag-document-qa
```

Create a virtual environment

```
python -m venv .venv
```

Activate it

```
.venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

## Running the System

Make sure Ollama is running locally with the required model.

```
ollama run llama2
```

Run the application

```
python app.py
```

---

## Example Use Case

Ask questions from academic textbooks such as:

```
What is the working principle of a PN junction diode?
```

The system retrieves the most relevant sections from the document and generates a context-grounded answer.

---

## Future Improvements

* Add vector database support (FAISS / Chroma)
* Web interface for querying documents
* Support for multiple document collections
* Retrieval evaluation metrics
