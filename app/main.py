import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import HealthResponse

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаём приложение
app = FastAPI(
    title="AI Translator API",
    description="API для перевода текста EN↔RU",
    version="1.0.0"
)

# Эндпоинт для проверки здоровья сервиса
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    logger.info("Health check requested")
    return HealthResponse(status="ok")

# Обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Событие при запуске
@app.on_event("startup")
async def startup_event():
    logger.info("AI Translator API started on http://localhost:8000")

# Событие при остановке
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Translator API shutting down")