from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config

# SQLite не требует отдельного сервера — база будет в файле
engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False}  # нужно только для SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()