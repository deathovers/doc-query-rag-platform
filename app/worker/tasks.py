from celery import Celery
from app.core.config import settings
import os
from app.models.db import SessionLocal, DocumentMetadata, DocumentStatus
from app.services.vector_store import vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf
import docx
import uuid

celery_app = Celery("worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

def extract_text(file_path, filename):
    ext = filename.split(".")[-1].lower()
    text = ""
    if ext == "pdf":
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    elif ext == "docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif ext == "txt":
        with open(file_path, "r") as f:
            text = f.read()
    return text

@celery_app.task(name="process_document")
def process_document(document_id: str, file_path: str, user_id: str):
    db = SessionLocal()
    doc_record = db.query(DocumentMetadata).filter(DocumentMetadata.id == document_id).first()
    if not doc_record:
        return

    try:
        doc_record.status = DocumentStatus.PROCESSING
        db.commit()

        text = extract_text(file_path, doc_record.filename)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(text)
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"document_id": str(document_id), "user_id": str(user_id)} for _ in chunks]
        
        vector_store.add_documents(ids, chunks, metadatas)

        doc_record.status = DocumentStatus.COMPLETED
        db.commit()
    except Exception as e:
        print(f"Error processing document: {e}")
        doc_record.status = DocumentStatus.FAILED
        db.commit()
    finally:
        db.close()
