# Document-Based RAG System

## Overview
The Document-Based RAG (Retrieval-Augmented Generation) System is a high-performance, multi-tenant platform that allows users to upload documents (PDF, DOCX, TXT) and interact with their content through a conversational AI interface. By combining vector similarity search with large language models, the system provides context-aware answers with precise source attribution.

## Key Features
- **Multi-Tenant Isolation**: Secure data handling using `X-User-ID` headers to ensure users only access their own documents.
- **Asynchronous Processing**: Background workers handle document parsing and indexing to maintain API responsiveness.
- **Robust Parsing**: Support for PDF, DOCX, and TXT files with recursive character chunking.
- **Vector Search**: Powered by ChromaDB for efficient similarity retrieval.
- **Source Attribution**: Responses include references to specific documents and pages.

## Tech Stack
- **Backend**: FastAPI
- **Vector Database**: ChromaDB
- **Metadata Storage**: SQLite
- **Document Processing**: LangChain (RecursiveCharacterTextSplitter), PyMuPDF/python-docx
- **Task Management**: FastAPI BackgroundTasks

## Installation

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Environment Variables:
   Create a `.env` file (if applicable) or ensure your environment has access to necessary LLM API keys (e.g., `OPENAI_API_KEY`).

## Usage

### Running the Server
Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### Quick Start
1. **Upload a Document**: Send a POST request to `/v1/documents/upload` with your file and a unique `X-User-ID` header.
2. **Query the System**: Send a POST request to `/v1/chat/query` with your question and the same `X-User-ID`.

## Architecture
The system follows a standard RAG pipeline:
1. **Ingestion**: Files are uploaded and processed in the background.
2. **Chunking**: Text is split into manageable segments (1000 tokens with 200 overlap).
3. **Embedding**: Segments are converted into vectors.
4. **Retrieval**: At query time, the system finds the most relevant chunks based on user ID and optional document filters.
5. **Generation**: An LLM synthesizes the final answer using the retrieved context.
