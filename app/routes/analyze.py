import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import TranslationHistory
from app.schemas import TranslateRequest, TranslateResponse
from app.ml_service import translation_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest, db: Session = Depends(get_db)):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
    
    supported_langs = ["en", "ru"]
    if request.source_lang != "auto" and request.source_lang not in supported_langs:
        raise HTTPException(status_code=400, detail=f"Unsupported source_lang. Use: {supported_langs} or 'auto'")
    
    if request.target_lang not in supported_langs:
        raise HTTPException(status_code=400, detail=f"Unsupported target_lang. Use: {supported_langs}")
    
    try:
        logger.info(f"Translating: {request.text[:50]}...")
        
        translated_text = translation_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        if request.source_lang == "auto":
            source_lang = translation_service.detect_language(request.text)
        else:
            source_lang = request.source_lang
        
        history = TranslationHistory(
            input_text=request.text,
            source_lang=source_lang,
            target_lang=request.target_lang,
            result_text=translated_text,
            model_name=translation_service.get_model_name(source_lang, request.target_lang)
        )
        db.add(history)
        db.commit()
        
        logger.info(f"Translation saved with id: {history.id}")
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=request.target_lang,
            model_name=history.model_name
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Translation service error: {str(e)}")