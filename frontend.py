from sentence_transformers import SentenceTransformer
from chunking import chunk_docs
from embedding import embed
from retrieval import format_context_for_generation, retrieve
from generation import generate_answer
import streamlit as st
import os
st.set_page_config(page_title="Helping Hand", layout="wide")
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import embedding as emb_module

@st.cache_resource
def load_model():
    model= SentenceTransformer('all-MiniLM-L6-v2')
    return model
    pass

model = load_model()
st.sidebar.title("Document Management Panel ")
st.sidebar.markdown("Upload your documents here. The system will process them and make them available for querying.")

uploaded_files = st.sidebar.file_uploader("Upload Documents", type="pdf",accept_multiple_files=True)

if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} document(s) uploaded successfully!")
    if st.sidebar.button("Process Documents"):
        if os.path.exists('data/embeddings.npy'):
          os.remove('data/embeddings.npy')
        if os.path.exists('data/chunks.pkl'):
          os.remove('data/chunks.pkl')
        emb_module._cached_chunks = None    
        emb_module._cached_embeddings = None
    
        with st.spinner("Processing documents..."):
            target="data"
            os.makedirs(target, exist_ok=True)
            for uploaded_file in uploaded_files:
                file_path = os.path.join(target, uploaded_file.name)
                print(f"Attempting to save: {file_path}")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    f.flush()
                    os.fsync(f.fileno())
                print(f"File exists after save: {os.path.exists(file_path)}")
                print(f"File size: {os.path.getsize(file_path)} bytes")
            st.sidebar.success("Documents processed successfully!")
            chunks, embeddings = embed()
            emb_module._cached_chunks = chunks
            emb_module._cached_embeddings = embeddings
            st.sidebar.success(f"{len(chunks)} chunks created from the uploaded documents.")
            st.sidebar.success("Documents embedded successfully and ready for querying!")
            st.sidebar.balloons()
st.title("Helping Hand: Your Document Query Assistant")
st.markdown("Welcome to Helping Hand! This application allows you to upload your documents, which are then processed and made available for querying. Use the sidebar to manage your documents and start asking questions about their content.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citation" in message:
            st.caption(f"**Source:** {message['citation']}")

if query := st.chat_input("Ask a question about your documents..."):
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("assistant"):
        st.markdown("Let me find the relevant information...")
        results=retrieve(query)

    if not results:
        st.markdown("Sorry, I couldn't find any relevant information in the documents. Try rephrasing your question or check the uploaded documents.")
    else:
        with st.expander(f"View {len(results)} Retrieved Chunks"):
                for i, chunk in enumerate(results, 1):
                    st.markdown(f"**Chunk {i}** — Similarity: `{chunk['similarity']:.4f}`")
                    st.markdown(chunk['content'])
                    st.caption(
                        f"Source: {chunk['source']} | "
                        f"Page: {chunk['page']} | "
                        f"Chapter: {chunk['chapter']} | "
                        f"Section: {chunk['section']}"
                    )
                    st.divider()

        with st.spinner("Generating answer..."):
            context = format_context_for_generation(results)
            answer = generate_answer(query, context)

        st.markdown(answer)
        primary = results[0]
        citation_text = (
                f"{primary['source']} | "
                f"Page {primary['page']} | "
                f"Chapter: {primary['chapter']}"
            )
        st.info(f"**Primary Source:** {citation_text}")

        st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "citation": citation_text
            })               
            

