from chunking import chunk_docs
import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(v1, array_of_vectors): 
    v1 = np.array(v1)
    similarities = []
    if len(np.shape(array_of_vectors)) == 1:
        array_of_vectors = [array_of_vectors]
    for v2 in array_of_vectors:
        v2 = np.array(v2)
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        similarity = dot_product / (norm_v1 * norm_v2)
        similarities.append(similarity)
    return [float(x) for x in similarities]

def embed():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chunks = chunk_docs()
    embeddings = []
    for chunk in chunks :
        embedding = model.encode(chunk.page_content)
        embeddings.append(embedding)
    
    embeddings= np.array(embeddings)
    return chunks, embeddings

