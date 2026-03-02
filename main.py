from fastapi import FastAPI, UploadFile, File, Header, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from db import get_db, init_db
from models import DocumentMetadata, StatusEnum
from document_processor import process_document
from chat import get_chat_response
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Document RAG API")

# Initialize database tables
init_db()

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    filters: Optional[dict] = None

@app.post("/v1/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), # Fixed syntax: UploadFile = File(...)
    x_user_id: str = Header(...), # Consistent user_id from header
    db: Session = Depends(get_db)
):
    doc_id = str(uuid.uuid4())
    try:
        content = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read file")
    
    # Save metadata to relational DB
    new_doc = DocumentMetadata(
        id=doc_id,
        user_id=x_user_id,
        filename=file.filename,
        status=StatusEnum.PENDING
    )
    db.add(new_doc)
    db.commit()

    # Trigger background processing to avoid timeout
    background_tasks.add_task(process_document, doc_id, content, file.filename, x_user_id)

    return {"document_id": doc_id}

@app.post("/v1/chat/query")
async def chat_query(
    request: QueryRequest,
    x_user_id: str = Header(...), # Consistent user_id from header
    db: Session = Depends(get_db)
):
    doc_ids = None
    if request.filters and "document_ids" in request.filters:
        doc_ids = request.filters["document_ids"]
    
    response = get_chat_response(request.query, x_user_id, doc_ids)
    return response

@app.get("/v1/documents")
async def list_documents(x_user_id: str = Header(...), db: Session = Depends(get_db)):
    docs = db.query(DocumentMetadata).filter(DocumentMetadata.user_id == x_user_id).all()
    return docs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
