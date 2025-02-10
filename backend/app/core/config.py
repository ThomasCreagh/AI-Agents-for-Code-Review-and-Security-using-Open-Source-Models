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

    # Test user for paramaters, for testing purposes
    EMAIL_TEST_USER: str = "exampleEmail@gmail.com"
    PASSWORD_TEST_USER: str = "123456"

    # Arbitrary value to get frontend host (Need to get from front end team)
    FRONTEND_HOST: str = "http://localhost:7755"


settings = Settings()
