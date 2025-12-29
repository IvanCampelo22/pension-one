import os
from urllib.parse import quote_plus

class Settings:
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    _DB_PASSWORD_RAW = os.environ["DB_PASSWORD"]
    DB_PASSWORD = quote_plus(_DB_PASSWORD_RAW)
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = int(os.environ.get("DB_PORT") or 5432)

settings = Settings()