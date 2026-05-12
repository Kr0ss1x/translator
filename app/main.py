import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import engine, Base, get_db
from app.schemas import HealthResponse
from app.routes import analyze, history

# СОЗДАНИЕ ТАБЛИЦ АВТОМАТИЧЕСКИ ПРИ ЗАПУСКЕ
Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Translator API",
    description="API для перевода текста EN↔RU",
    version="1.0.0"
)

# ПОДКЛЮЧАЕМ РОУТЕРЫ
app.include_router(analyze.router, tags=["Translation"])
app.include_router(history.router, tags=["History"])

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    logger.info("Health check requested")
    return HealthResponse(status="ok")

@app.get("/check-db")
async def check_db(db: Session = Depends(get_db)):
    from app.models import TranslationHistory
    count = db.query(TranslationHistory).count()
    return {"status": "connected", "record_count": count}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.on_event("startup")
async def startup_event():
    logger.info("AI Translator API started on http://localhost:8000")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Translator API shutting down")