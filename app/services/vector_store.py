import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name="text-embedding-3-small"
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.openai_ef
        )

    def add_documents(self, ids, documents, metadatas):
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, query_text, user_id, n_results=5, document_ids=None):
        where_clause = {"user_id": str(user_id)}
        if document_ids:
            where_clause["document_id"] = {"$in": [str(d) for d in document_ids]}
        
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_clause
        )

vector_store = VectorStore()
