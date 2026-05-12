import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/translator_db")
    MODEL_NAME = os.getenv("MODEL_NAME", "Helsinki-NLP/opus-mt-en-ru")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 8000))

config = Config()
