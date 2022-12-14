from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str

    class Config:
        env_file = ".env"

settings = Settings()