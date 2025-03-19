from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    REACT_APP_API_KEY: str = "t"
    REACT_APP_BACKEND_URL: str = "http://localhost:8000/api/v1"
    FRONTEND_HOST: str = "http://localhost:3000"

    # LLM Configuration
    LLM_MODEL: str = "granite3.1-dense:2b"
    LLM_BASE_URL: str = "http://ollama:11434"
    LLM_TEMPERATURE: float = 0.0
    
    # Anthropic Configuration
    USE_ANTHROPIC: bool = False
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude 3.5 Haiku"

    # Vector Store Configuration
    COLLECTION_NAME: str = "general_docs"
    PERSIST_DIRECTORY: str = "./chroma"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    EMBEDDING_BASE_URL: str = "http://ollama:11434"

    # Document Processing Configuration
    DOCUMENTS_BASE_DIR: str = "app/doc_loader/data"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Debug Configuration
    DEBUG_MODE: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and v == "*":
            return v
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Environment
    ENVIRONMENT: str = "local"

    # GPU Configuration
    NVIDIA_VISIBLE_DEVICES: str = "all"
    CUDA_VISIBLE_DEVICES: str = "0"
    OLLAMA_GPU_LAYERS: int = 35

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()