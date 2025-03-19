from pydantic import BaseModel, Field
from typing import Any, Optional, List
from langchain_core.language_models import BaseLLM
from langchain_chroma import Chroma

from app.ai.llm.llm import initialise_llm
from app.ai.database.init_chroma import initialize_vector_store
from app.ai.database.database_manager import DatabaseManager
import os

class AIDependencies(BaseModel):
    # Core components
    vector_store: Any
    llm: Any
    
    # LLM parameters
    token_limit: int = Field(default=500, description="Maximum tokens for queries")
    response_token_limit: int = Field(default=1000, description="Maximum tokens for LLM responses")
    llm_temperature: float = Field(default=0.0, description="Temperature for LLM sampling (0-1)")
    
    # RAG parameters
    max_documents: int = Field(default=1, description="Maximum documents to retrieve per query")
    similarity_threshold: float = Field(default=0.7, description="Minimum similarity score for document retrieval")
    
    # Code analysis parameters
    max_code_length: int = Field(default=2000, description="Maximum length of code to analyze")
    max_functions: int = Field(default=5, description="Maximum number of functions to analyze")
    sensitive_param_patterns: List[str] = Field(
        default=["user", "input", "data", "request", "file", "path", "password", "key", "secret", "token", "auth"],
        description="Patterns to look for in parameter names to identify potential security issues"
    )
    
    # Security analysis parameters
    security_focus_areas: List[str] = Field(
        default=["input_validation", "authentication", "authorization", "data_exposure", "injection", "xss"],
        description="Security areas to focus on during analysis"
    )
    
    # Performance parameters
    enable_throttling: bool = Field(default=True, description="Enable throttling between LLM calls")
    throttling_delay: float = Field(default=0.5, description="Delay in seconds between LLM calls if throttling is enabled")
    debug_mode: bool = Field(default=False, description="Enable detailed debugging output")

_instance: Optional[AIDependencies] = None

def get_ai_dependencies() -> AIDependencies:
    global _instance
    
    if _instance is None:
        llm = initialise_llm()
        
        db_manager = DatabaseManager(
            collection_name=os.getenv("COLLECTION_NAME", "general_docs"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
            persist_directory=os.getenv("PERSIST_DIRECTORY", "./chroma")
        )
        
        _instance = AIDependencies(
            vector_store=db_manager.vector_store,
            llm=llm,
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            token_limit=int(os.getenv("TOKEN_LIMIT", "500")),
            max_documents=int(os.getenv("MAX_DOCUMENTS", "1")),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
            throttling_delay=float(os.getenv("THROTTLING_DELAY", "0.5"))
        )
    
    return _instance

def get_vector_store():
    return get_ai_dependencies().vector_store

def get_llm():
    return get_ai_dependencies().llm