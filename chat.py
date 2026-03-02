from vector_store import vector_store
from openai import OpenAI
import os

# Initialize OpenAI client (requires OPENAI_API_KEY env var)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-placeholder"))

def get_chat_response(query: str, user_id: str, document_ids: list = None):
    results = vector_store.query(query, user_id, document_ids)
    
    # Fix: IndexError Risk - check if results contain data
    if not results or not results.get('documents') or len(results['documents'][0]) == 0:
        return {
            "answer": "I couldn't find any relevant information in your documents to answer that question.",
            "sources": []
        }

    context = "\n".join(results['documents'][0])
    
    prompt = f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error generating response: {str(e)}"
    
    sources = []
    if results.get('metadatas'):
        seen_docs = set()
        for meta in results['metadatas'][0]:
            doc_id = meta.get("document_id")
            if doc_id and doc_id not in seen_docs:
                sources.append({"document_id": doc_id})
                seen_docs.add(doc_id)

    return {
        "answer": answer,
        "sources": sources
    }
