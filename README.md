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
          LLM (Ollama - Llama2)
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
Ask a question (or type 'quit' to exit): Define a bjt.
 Loading cached embeddings from disk
 Loaded 4953 chunks with embeddings
 Retrieving chunks for query: 'Define a bjt.'
Using similarity threshold: 0.3
Found 5 relevant chunks

 RETRIEVED CHUNKS 

[Chunk 1]
  Similarity: 0.5667
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 7 > 0.707 of midband gain. > None
  Content: s operation at a particular point on its characteristic curve. bipolar Type of device whose functioning involves both majority and minority charge car...

[Chunk 2]
  Similarity: 0.5219
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter i > 4.2 OPERATING POINT > None
  Content: BJTs Figure 4.1 Various operating points within the limits of operation of a transistor. 5 IC max Saturation IC (mA) VCE0 5 10 15 20 25 10 15 80 A 60 ...

[Chunk 3]
  Similarity: 0.4999
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 5 > 5.1 INTRODUCTION > None
  Content: the current I C in Fig. 5.1a is a direct function of the level of IB. For the FET the current I will be a function of the voltage VGS applied to the i...
[Chunk 4]
  Similarity: 0.4915
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 8 > 4.1 to present some basic ideas about the operating point > None       
  Content: changes result in minimum changes in the operating point. This maintenance of the operating point can be specified by a stability factor, S, which ind...

[Chunk 5]
  Similarity: 0.4909
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 6 > 5.2 CONSTRUCTION AND > None
  Content: arrangements will be covered in Chapter 6. The analysis performed in Chapter 4 using BJT transistors will prove helpful in the derivation of the impor...
 ===== END CHUNKS =====

Formatted 5 chunks for generation
 Sending prompt to LLM

Answer:

A bipolar junction transistor (BJT) is a type of semiconductor device whose functioning involves both majority and minority charge carriers. It is a 3-layer device containing both types of semiconductor material (either in p-n-p or np-n form).

==================================================

Ask a question (or type 'quit' to exit): what are the characteristics of bjt?
 Retrieving chunks for query: 'what are the characteristics of bjt?'
Using similarity threshold: 0.3
Found 5 relevant chunks

 RETRIEVED CHUNKS

[Chunk 1]
  Similarity: 0.5926
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 7 > 0.707 of midband gain. > None
  Content: s operation at a particular point on its characteristic curve. bipolar Type of device whose functioning involves both majority and minority charge car...

[Chunk 2]
  Similarity: 0.5174
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 8 > 4.1 to present some basic ideas about the operating point > None       
  Content: changes result in minimum changes in the operating point. This maintenance of the operating point can be specified by a stability factor, S, which ind...

[Chunk 3]
  Similarity: 0.5109
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter i > 4.2 OPERATING POINT > None
  Content: BJTs Figure 4.1 Various operating points within the limits of operation of a transistor. 5 IC max Saturation IC (mA) VCE0 5 10 15 20 25 10 15 80 A 60 ...

[Chunk 4]
  Similarity: 0.5022
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter 3 > 3.2 Transistor Construction > None
  Content: 3.2 Transistor Construction 1. What names are applied to the two types of BJT transistors? Sketch the basic construction of each and label the various...

[Chunk 5]
  Similarity: 0.4938
  Source: data/Analog Electronics\Electronic Devices and Circuit Theory 7th Edition.pdf        
  Location: Chapter i > 3.2 TRANSISTOR CONSTRUCTION > None
  Content: 0.150/0.001 /H11005150/H110181. The doping of the sandwiched layer is also considerably less than that of the outer layers (typically, 10/H110181 or l...
 ===== END CHUNKS =====

Formatted 5 chunks for generation
 Sending prompt to LLM
Formatted 5 chunks for generation
 Sending prompt to LLM

Answer:

The characteristics of a bipolar junction transistor (BJT) are:

1. Three-terminal device: A BJT has three terminals: Emitter (E), Collector (C), and Base (B). 
2. Majority and minority carriers: BJTs have both majority (holes) and minority (electrons) carriers.
3. Linear or active operating region: The BJT operates in a linear or active region where the current flows in proportion to the voltage applied between the emitter and collector.
4. Stability factor: The stability factor (S) indicates the degree of change in operating point due to a temperature variation. A highly stable circuit is desirable.
5. Biasing: The BJT must be biased in its linear or active operating region with the base voltage more positive than the emitter voltage, and the collector voltage more negative than the base voltage.
6. Forward-biased junction: The forward-biased junction (p-n) has a voltage of about 0.6 to 0.7 V.
7. Reverse-biased junction: The reverse-biased junction (n-p) has a voltage within the maximum limits of the device.
8. Carrier motion: In the forward-biased junction, majority carriers (holes) move from the emitter to the collector, while in the reverse-biased junction, minority carriers (electrons) move from the collector to the emitter.
9. Leakage current: The BJT has a leakage current due to the presence of minority carriers.    

These characteristics determine the behavior and performance of BJTs in electronic circuits.   

==================================================
Ask a question (or type 'quit' to exit): exit
Goodbye!
