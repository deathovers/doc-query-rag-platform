from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.services.vector_store import vector_store
from openai import OpenAI
from app.core.config import settings

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    filters: Optional[dict] = None

@router.post("/query")
async def query_rag(request: QueryRequest):
    # Mock user_id
    user_id = uuid.uuid4() 
    
    document_ids = request.filters.get("document_ids") if request.filters else None
    
    results = vector_store.query(
        query_text=request.query,
        user_id=user_id,
        document_ids=document_ids
    )
    
    context = "\n\n".join(results['documents'][0])
    sources = results['metadatas'][0]

    prompt = f"""Use the following context to answer the user's question. 
    If you don't know the answer, just say you don't know.
    
    Context:
    {context}
    
    Question: {request.query}
    """

    def generate():
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")
