from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from typing import List, Dict, Optional, Any, Tuple
from langchain_core.documents import Document
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self,
                 collection_name: str = "general_docs",
                 embedding_model: str = "nomic-embed-text",
                 persist_directory: str = "./chroma",
                 batch_size: int = 100):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.batch_size = batch_size

        # Always use Ollama for embeddings even if using Claude for LLM
        self.embeddings = OllamaEmbeddings(
            base_url=settings.EMBEDDING_BASE_URL,
            model=embedding_model
        )

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
            collection_metadata={
                "hnsw:space": "cosine",  # Similarity metric
                # Higher values create more connections (addresses "M is too small" error)
                "hnsw:M": 64,
                "hnsw:ef_construction": 800,  # Higher values create more accurate indexes
                # Higher values improve search recall (addresses "ef is too small" error)
                "hnsw:ef": 240
            }
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
        }

    def search_documents(self,
                         query: str,
                         k: int = 1,
                         filter: Optional[Dict] = None,
                         with_score: bool = False) -> List[Document]:
        """
        Search for documents similar to the query with robust error handling.

        Args:
            query: The query string
            k: Number of documents to retrieve
            filter: Optional metadata filter
            with_score: Whether to include similarity scores

        Returns:
            List of retrieved documents or empty list if retrieval fails
        """
        try:
            logger.info(f"Searching for documents with query: {query[:50]}...")
            search_kwargs = {
                "k": k,
                "fetch_k": k * 4,  # Fetch more candidates to improve recall
                "score_threshold": 0.5,  # Only return relevant results
                "ef": 100  # Higher values improve recall at the cost of speed
            }
            if with_score:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k,
                    filter=filter,
                    search_kwargs=search_kwargs
                )
            else:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter=filter,
                    search_kwargs=search_kwargs
                )
            logger.info(f"Successfully retrieved {len(results)} documents")
            return results

        except Exception as e:
            logger.error(f"Error in vector search: {str(e)}")

            try:
                logger.info(
                    "Attempting fallback retrieval with direct collection access...")
                query_embedding = self.embeddings.embed_query(query)
                collection_results = self._collection.query(
                    query_embeddings=[query_embedding],
                    n_results=k,
                    where=filter,
                    include=["documents", "metadatas", "distances"]
                )
                docs = []
                if collection_results and len(collection_results.get('documents', [[]])[0]) > 0:
                    for i, text in enumerate(collection_results['documents'][0]):
                        if text:  # Only add non-empty documents
                            metadata = {}
                            if 'metadatas' in collection_results and collection_results['metadatas'][0]:
                                metadata = collection_results['metadatas'][0][i] or {
                                }
                            doc = Document(page_content=text,
                                           metadata=metadata)
                            if with_score and 'distances' in collection_results:
                                distance = collection_results['distances'][0][i]
                                similarity = 1.0 - distance
                                docs.append((doc, similarity))
                            else:
                                docs.append(doc)

                    logger.info(
                        f"Fallback retrieval successful, found {len(docs)} documents")
                    return docs

                logger.warning("Fallback retrieval returned no documents")
                return []

            except Exception as fallback_error:
                # If all attempts fail, log and return empty list
                logger.error(
                    f"Fallback retrieval also failed: {str(fallback_error)}")
                return []

    def add_documents(self, documents: List[Document], ids: Optional[List[str]] = None) -> dict:
        try:
            logger.info(f"Adding {len(documents)} documents to vector store")
            self.vector_store.add_documents(documents=documents, ids=ids)
            logger.info(f"Successfully added {len(documents)} documents")
            return {"status": "success", "added_count": len(documents)}
        except Exception as e:
            error_msg = f"Error adding documents: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def update_documents(self, documents: List[Document], ids: List[str]) -> dict:
        try:
            logger.info(f"Updating {len(documents)} documents in vector store")
            self.vector_store.update_documents(ids=ids, documents=documents)
            logger.info(f"Successfully updated {len(documents)} documents")
            return {"status": "success", "updated_count": len(documents)}
        except Exception as e:
            error_msg = f"Error updating documents: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def delete_documents(self, ids: List[str]) -> dict:
        try:
            logger.info(f"Deleting {len(ids)} documents from vector store")
            self.vector_store.delete(ids=ids)
            logger.info(f"Successfully deleted {len(ids)} documents")
            return {"status": "success", "deleted_count": len(ids)}
        except Exception as e:
            error_msg = f"Error deleting documents: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def create_retriever(self,
                         search_type: str = "mmr",
                         search_kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Create a retriever with improved search parameters.
        """
        if search_kwargs is None:
            search_kwargs = {
                "k": 1,
                "fetch_k": 4,
                "lambda_mult": 0.5,
                "ef": 100
            }

        logger.info(
            f"Creating retriever with search_type={search_type}, params={search_kwargs}")
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
