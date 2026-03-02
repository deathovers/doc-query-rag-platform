from fastapi import FastAPI
from app.api.v1.endpoints import documents, chat
from app.models.db import init_db

app = FastAPI(title="Document RAG System")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(documents.router, prefix="/v1/documents", tags=["documents"])
app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
