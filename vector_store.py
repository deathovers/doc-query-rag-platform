import chromadb
import os

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_chunks(self, chunks, metadatas, ids):
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text, user_id, document_ids=None, n_results=5):
        # Multi-tenant isolation logic
        if document_ids and len(document_ids) > 0:
            # Fix: Explicit $and operator for multiple filters in ChromaDB
            where_clause = {
                "$and": [
                    {"user_id": {"$eq": user_id}},
                    {"document_id": {"$in": document_ids}}
                ]
            }
        else:
            where_clause = {"user_id": {"$eq": user_id}}
        
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_clause
        )

vector_store = VectorStore()
