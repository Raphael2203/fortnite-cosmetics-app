import os
from dotenv import load_dotenv
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]

APP_ENV = os.getenv("APP_ENV", "development")

if APP_ENV == "production":
    ENV_PATH = BACKEND_DIR / ".env"
else:
    ENV_PATH = BACKEND_DIR / ".env.locaL"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH, override=True)
else:
    print(f"Aviso: {ENV_PATH} não encontrado. Usando variáveis de sistema")

BASE_FORTNITE_URL = "https://fortnite-api.com/v2"
FORTNITE_HEADERS = {"User-Agent": "FortniteApp/1.0"}

class Settings:
    def __init__(self):
        self.DATABASE_URL = self._require("DATABASE_URL")
        self.REDIS_URL = self._require("REDIS_URL")
        self.CELERY_BROKER_URL = self._require("CELERY_BROKER_URL")
        self.CELERY_RESULT_BACKEND = self._require("CELERY_RESULT_BACKEND")
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.APP_PORT = int(os.getenv("PORT", "8000"))

    def _require(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"{key} não definido no ambiente")
        return value

settings = Settings()