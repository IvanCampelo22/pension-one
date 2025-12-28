import os

class Settings:
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")

    DB_PORT: int = int(os.getenv("DB_PORT") or 5432)

settings = Settings()