import os

class Settings:
    DB_NAME: str = os.environ["DB_NAME"]
    DB_USER: str = os.environ["DB_USER"]
    DB_PASSWORD: str = os.environ["DB_PASSWORD"]
    DB_HOST: str = os.environ["DB_HOST"]

    DB_PORT: int = int(os.environ.get("DB_PORT") or 5432)

settings = Settings()