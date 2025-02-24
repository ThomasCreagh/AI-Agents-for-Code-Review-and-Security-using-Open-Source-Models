from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from typing import List, Dict, Optional, Any, Tuple
from langchain_core.documents import Document


class DatabaseManager:
    def __init__(self,
                 collection_name: str = "general_docs",
                 embedding_model: str = "nomic-embed-text",
                 persist_directory: str = "./chroma",
                 batch_size: int = 100):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.batch_size = batch_size

        self.embeddings = OllamaEmbeddings(
            base_url="http://ollama:11434",
            model=embedding_model
        )

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

        self._collection = self.vector_store._collection

    def clear_collection(self) -> dict:
        ids = self._collection.get()['ids']
        if not ids:
            return {"deleted_count": 0}

        total_deleted = 0
        for i in range(0, len(ids), self.batch_size):
            batch_ids = ids[i:i + self.batch_size]
            self._collection.delete(ids=batch_ids)
            total_deleted += len(batch_ids)

        return {"deleted_count": total_deleted}

    def get_stats(self) -> dict:
        return {
            "total_documents": self._collection.count(),
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory,
            "last_updated": self._collection.get()["metadatas"][-1]["timestamp"] if self._collection.count() > 0 else None
        }

    def search_documents(self,
                         query: str,
                         k: int = 1,
                         filter: Optional[Dict] = None,
                         with_score: bool = False) -> List[Document]:
        if with_score:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
        else:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
        return results

    def add_documents(self, documents: List[Document], ids: Optional[List[str]] = None) -> dict:
        try:
            self.vector_store.add_documents(documents=documents, ids=ids)
            return {"status": "success", "added_count": len(documents)}
        except Exception as e:
            raise Exception(f"Error adding documents: {str(e)}")

    def update_documents(self, documents: List[Document], ids: List[str]) -> dict:
        try:
            self.vector_store.update_documents(ids=ids, documents=documents)
            return {"status": "success", "updated_count": len(documents)}
        except Exception as e:
            raise Exception(f"Error updating documents: {str(e)}")

    def delete_documents(self, ids: List[str]) -> dict:
        try:
            self.vector_store.delete(ids=ids)
            return {"status": "success", "deleted_count": len(ids)}
        except Exception as e:
            raise Exception(f"Error deleting documents: {str(e)}")

    def create_retriever(self,
                         search_type: str = "mmr",
                         search_kwargs: Optional[Dict[str, Any]] = None) -> Any:
        if search_kwargs is None:
            search_kwargs = {"k": 1, "fetch_k": 2, "lambda_mult": 0.5}
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
