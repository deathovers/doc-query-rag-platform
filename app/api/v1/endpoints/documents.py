from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.models.db import SessionLocal, DocumentMetadata, DocumentStatus
from app.worker.tasks import process_document
import uuid
import os
from app.core.config import settings

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_document(file: File(UploadFile), db=Depends(get_db)):
    # Mock user_id for now, in real app get from auth
    user_id = uuid.uuid4() 
    
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
        
    file_id = uuid.uuid4()
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    doc_metadata = DocumentMetadata(
        id=file_id,
        user_id=user_id,
        filename=file.filename,
        status=DocumentStatus.PENDING
    )
    db.add(doc_metadata)
    db.commit()
    
    process_document.delay(str(file_id), file_path, str(user_id))
    
    return {"document_id": file_id, "status": "Accepted"}
