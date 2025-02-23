# simple_config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "granite3.1-dense:2b")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))

# Vector Store Configuration
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "general_docs")
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "./chroma")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "http://localhost:11434")

# Document Processing Configuration
DOCUMENTS_BASE_DIR = os.getenv("DOCUMENTS_BASE_DIR", "app/doc_loader/data")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Debug Configuration
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")