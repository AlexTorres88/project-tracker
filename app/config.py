from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    jwt_refresh_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
