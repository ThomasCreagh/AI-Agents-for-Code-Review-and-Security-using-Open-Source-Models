from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from app.core.config import settings
import os


def initialize_vector_store(
    embedding_model: str = None,
    collection_name: str = None,
    persist_directory: str = None
):
    """Initialize and return a Chroma vector store with OllamaEmbeddings."""
    
    # Use provided values or fall back to settings
    model = embedding_model or settings.EMBEDDING_MODEL
    collection = collection_name or settings.COLLECTION_NAME
    persist_dir = persist_directory or settings.PERSIST_DIRECTORY
    
    # Ensure the persist directory exists
    os.makedirs(persist_dir, exist_ok=True)
    
    print(f"Initializing vector store with {model} embeddings in collection {collection}")
    
    # Initialize embeddings with Ollama (even if using Claude for LLM)
    embeddings = OllamaEmbeddings(
        base_url=settings.EMBEDDING_BASE_URL,
        model=model
    )
    
    # Create and return the vector store
    return Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )