from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, BeforeValidator, computed_field
from typing import Annotated, Literal, Any


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


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
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [
            str(origin).rstrip("/")
            for origin in self.BACKEND_CORS_ORIGINS
        ] + [self.FRONTEND_HOST]


settings = Settings()
