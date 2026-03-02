import io
from pypdf import PdfReader
from docx import Document as DocxDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vector_store import vector_store
from models import StatusEnum, DocumentMetadata
from db import SessionLocal
import uuid

def process_document(doc_id: str, file_content: bytes, filename: str, user_id: str):
    db = SessionLocal()
    try:
        # Update status to PROCESSING
        doc_meta = db.query(DocumentMetadata).filter(DocumentMetadata.id == doc_id).first()
        if not doc_meta:
            return
        doc_meta.status = StatusEnum.PROCESSING
        db.commit()

        text = ""
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        elif filename.lower().endswith(".docx"):
            doc = DocxDocument(io.BytesIO(file_content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else: # Default to text
            text = file_content.decode("utf-8", errors="ignore")

        # Chunking strategy
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text)

        if chunks:
            # Indexing with metadata for isolation
            metadatas = [{"document_id": doc_id, "user_id": user_id} for _ in range(len(chunks))]
            ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
            vector_store.add_chunks(chunks, metadatas, ids)

        # Update status to COMPLETED
        doc_meta.status = StatusEnum.COMPLETED
        db.commit()
    except Exception as e:
        print(f"Error processing document {doc_id}: {e}")
        doc_meta = db.query(DocumentMetadata).filter(DocumentMetadata.id == doc_id).first()
        if doc_meta:
            doc_meta.status = StatusEnum.FAILED
            db.commit()
    finally:
        db.close()
