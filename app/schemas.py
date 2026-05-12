from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TranslateRequest(BaseModel):
    text: str
    source_lang: Optional[str] = "auto"
    target_lang: str = "ru"

class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    model_name: str

class HistoryItem(BaseModel):
    id: int
    input_text: str
    source_lang: str
    target_lang: str
    result_text: str
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str