from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    GCS_BUCKET_NAME: str
    GCS_CREDENTIALS_PATH: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE: int
    JWT_REFRESH_TOKEN_EXPIRE: int

    class Config:
        env_file = ".env"

settings = Settings()