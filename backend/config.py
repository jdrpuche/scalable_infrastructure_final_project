from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    tavily_api_key: str
    firebase_credentials_path: str = "firebase-service-account.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
