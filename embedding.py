from chunking import chunk_docs
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

EMBEDDINGS_FILE = 'data/embeddings.npy'
CHUNKS_FILE = 'data/chunks.pkl'

model = SentenceTransformer('all-MiniLM-L6-v2')

_cached_chunks = None
_cached_embeddings = None


def cosine_similarity(query_vector, document_vectors):
    """Calculate cosine similarity between query and documents."""
    query_vector = np.array(query_vector)
    document_vectors = np.array(document_vectors)

    dot_products = np.dot(document_vectors, query_vector)
    norms = np.linalg.norm(document_vectors, axis=1) * np.linalg.norm(query_vector)
    norms[norms == 0] = 1e-10
    return (dot_products / norms).tolist()


def embed():
   
    global _cached_chunks, _cached_embeddings

    if _cached_chunks is not None and _cached_embeddings is not None:
        return _cached_chunks, _cached_embeddings

    if os.path.exists(EMBEDDINGS_FILE) and os.path.exists(CHUNKS_FILE):
        print(" Loading cached embeddings from disk")
        _cached_embeddings = np.load(EMBEDDINGS_FILE)

        with open(CHUNKS_FILE, 'rb') as f:
            _cached_chunks = pickle.load(f)

        print(f" Loaded {len(_cached_chunks)} chunks with embeddings")
        return _cached_chunks, _cached_embeddings

    print(" Computing embeddings for first time")
    _cached_chunks = chunk_docs()

    texts = [chunk.page_content for chunk in _cached_chunks]
    print(f"Encoding {len(texts)} text chunks")

    _cached_embeddings = model.encode(texts)
    _cached_embeddings = np.array(_cached_embeddings)

    os.makedirs('data', exist_ok=True)

    np.save(EMBEDDINGS_FILE, _cached_embeddings)

    with open(CHUNKS_FILE, 'wb') as f:
        pickle.dump(_cached_chunks, f)

    print(f" Saved {len(_cached_chunks)} chunks with embeddings")
    return _cached_chunks, _cached_embeddings
