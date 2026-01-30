# 📄 Document Q&A with RAG (Django + Mistral + Qdrant)

This project is a Retrieval-Augmented Generation (RAG) system that allows users to:

- Upload PDF documents
- Index them into a vector database (Qdrant)
- Ask natural language questions
- Get answers strictly grounded in the uploaded documents

## Tech Stack

- **Backend:** Django + Django REST Framework
- **LLM:** Mistral-7B-Instruct
- **Embeddings:** Sentence-Transformers (MiniLM)
- **Vector DB:** Qdrant
- **Frontend:** Simple Django templates
- **Deployment:** Docker

## How it works

1. PDFs are uploaded and split into chunks
2. Each chunk is embedded and stored in Qdrant
3. User questions are embedded and matched via semantic search
4. Relevant chunks are sent to the LLM as context
5. The LLM generates a grounded answer

## Running locally

```bash
docker compose up --build
