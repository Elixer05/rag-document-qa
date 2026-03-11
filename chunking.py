import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingestion import loadPages

def clean_text(text):
    text = re.sub(r'-\s+', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    lines = text.split('\n')
    lines = [line for line in lines if len(line.strip()) > 30]
    text = ' '.join(lines)
    return text.strip()

def chunk_docs():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150)
    chunks=[]
    docs=loadPages('data/')
    for doc in docs:
        text = clean_text(doc.page_content)
        doc.page_content = text
        doc_chunks = splitter.split_documents([doc])
        chunks.extend(doc_chunks)
    return chunks



