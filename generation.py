import requests
from retrieval import retrieve, format_context_for_generation


API_URL = "http://localhost:11434/api/generate"  
MODEL_NAME = "phi3"


def build_prompt(query, context):
    
    prompt = f"""
You are a helpful textbook assistant.

Answer the question using ONLY the information from the context below.
If the answer is not in the context, say: "The information is not available in the provided material."

Formatting rules:
- Use markdown tables for truth tables, comparisons, or structured data
- Use bullet points for lists
- Use bold for key terms
- Keep answers clear and concise
Context:
{context}

Question:
{query}

Provide a clear and concise answer or explain when told so.
Provide a clear and well-formatted answer using markdown where appropriate.
"""

    return prompt


def generate_answer(query, context=None):
    if context is None:
        retrieved_chunks = retrieve(query)
        if not retrieved_chunks:
            return "No relevant information found."
        context = format_context_for_generation(retrieved_chunks)
    
    prompt = build_prompt(query, context)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
        return f"Error from LLM API: {response.text}"
    return response.json().get("response", "No response generated.")