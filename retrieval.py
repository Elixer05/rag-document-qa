from embedding import embed, cosine_similarity, model

DEFAULT_SIMILARITY_THRESHOLD = 0.3


def retrieve(query, top_k=5, similarity_threshold=DEFAULT_SIMILARITY_THRESHOLD):

    chunks, embeddings = embed()

    print(f"[DEBUG] Retrieving chunks for query: '{query}'")
    print(f"[DEBUG] Using similarity threshold: {similarity_threshold}")

    query_embedding = model.encode(query, normalize_embeddings=True)

    similarities = cosine_similarity(query_embedding, embeddings)

    scored_chunks = [
        (chunk, sim)
        for chunk, sim in zip(chunks, similarities)
    ]

    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    filtered_chunks = [
        (chunk, sim)
        for chunk, sim in scored_chunks
        if sim >= similarity_threshold
    ][:top_k]

    if not filtered_chunks:
        print("[DEBUG] No chunks passed the similarity threshold")

    print(f"[DEBUG] Found {len(filtered_chunks)} relevant chunks")

    results = [
        {
            "content": chunk.page_content,
            "similarity": float(sim),
            "source": chunk.metadata.get("source", "unknown"),
            "page": chunk.metadata.get("page", "unknown"),
            "chapter": chunk.metadata.get("chapter", "unknown"),
            "section": chunk.metadata.get("section", "unknown"),
            "subsection": chunk.metadata.get("subsection", "unknown")
        }
        for chunk, sim in filtered_chunks
    ]

    print("\n[DEBUG] RETRIEVED CHUNKS ")
    for i, result in enumerate(results, 1):
        print(f"\n[Chunk {i}]")
        print(f"  Similarity: {result['similarity']:.4f}")
        print(f"  Source: {result['source']}")
        print(f"  Location: {result['chapter']} > {result['section']} > {result['subsection']}")
        print(f"  Content: {result['content'][:150]}...")
    print("[DEBUG] ===== END CHUNKS =====\n")

    return results

def format_context_for_generation(retrieved_chunks):

    if not retrieved_chunks:
        return "No relevant context found."

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, 1):

        citation = f"[{chunk['source']} | p{chunk['page']}]"

        if chunk.get("chapter") and chunk["chapter"] != "unknown":
            citation += f" | Chapter: {chunk['chapter']}"

        context_parts.append(
            f"{i}. {chunk['content']}\n   Source: {citation}"
        )

    context = "\n\n".join(context_parts)

    print(f"[DEBUG] Formatted {len(retrieved_chunks)} chunks for generation")

    return context