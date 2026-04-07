from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    GCS_BUCKET_NAME: str
    GCS_CREDENTIALS_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()