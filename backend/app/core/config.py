from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"

    # LLM Configuration
    LLM_MODEL: str
    LLM_BASE_URL: str
    LLM_TEMPERATURE: int

    # Vector Store Configuration
    COLLECTION_NAME: str
    PERSIST_DIRECTORY: str
    EMBEDDING_MODEL: str
    EMBEDDING_BASE_URL: str

    # Document Processing Configuration
    DOCUMENTS_BASE_DIR: str
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int

    # Optional: Debug Configuration
    DEBUG_MODE: bool
    LOG_LEVEL: str

    # Frontend and backend config
    REACT_APP_API_KEY: str
    REACT_APP_BACKEND_URL: str


settings = Settings()
