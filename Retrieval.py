from embedding import cosine_similarity, embed
from sentence_transformers import SentenceTransformer
from ingestion import loadPages
import requests
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant(query, chunks, doc_embeddings, top_k=3):
    query_embed = model.encode(query)
    distances = cosine_similarity(query_embed, doc_embeddings)
    vals = []
    for doc, dist in zip(chunks, distances):
        vals.append((doc, dist))
    vals.sort(key=lambda x: x[1], reverse=True)
    return vals[:top_k]
    
if __name__ == "__main__":
        chunks, doc_embeddings = embed()
        query="Explain MUX and DEMUX with examples."
        results=retrieve_relevant(query, chunks, doc_embeddings,top_k=3)
        for res in results:
            print(f"Score: {res[1]}")
            print(f"Content: {res[0].page_content}")
    
        cont = "\n\n".join(
        [chunk.page_content for chunk, score in results])

        response=[]
        prompt = """
        Answer the question using ONLY the context below.
        You MUST include a Sources section at the end.

        Context:
        {context}

        Question:
        {query}

        Sources:
       {sources}

     Answer:
    """

url='http://localhost:11434/api/generate'

data={
     "model": "llama2",  
    "prompt":prompt.format(context=cont, query=query,sources=context),
     "stream":True
}

headers={'Content-Type': 'application/json'}
response=requests.post(url,data=json.dumps(data), headers=headers, stream=True)

try:
    for line in response.iter_lines():
        if line:
            decoded_line=json.loads(line.decode('utf-8'))
            if "response" in decoded_line:
                response.append(decoded_line['response'])

finally:
    response.close()
    print(' '.join(response))