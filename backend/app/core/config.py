from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "sweng2025group23"
    REACT_APP_API_KEY: str

    USE_HUGGINGFACE: str = "yes"
    HUGGINGFACE_API_TOKEN: str
    REASONING_MODEL_ID: str = "deepseek-r1:7b-8k"
    TOOL_MODEL_ID: str = "qwen2.5:14b-instruct-q4_K_M"


settings = Settings()
