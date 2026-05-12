import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db import get_db
from app.models import TranslationHistory
from app.schemas import HistoryItem

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/history", response_model=list[HistoryItem])
async def get_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Получение истории запросов с пагинацией
    - limit: количество записей (от 1 до 100, по умолчанию 20)
    - offset: сдвиг (пропустить первые N записей)
    """
    try:
        history = db.query(TranslationHistory)\
            .order_by(desc(TranslationHistory.created_at))\
            .offset(offset)\
            .limit(limit)\
            .all()
        return history
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/history/{history_id}", response_model=HistoryItem)
async def get_history_item(history_id: int, db: Session = Depends(get_db)):
    """
    Получение конкретного запроса по ID
    """
    try:
        item = db.query(TranslationHistory).filter(TranslationHistory.id == history_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"History item with id {history_id} not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get history item {history_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")