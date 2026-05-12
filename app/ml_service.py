import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        logger.info("Translation service initialized")
    
    def detect_language(self, text: str) -> str:
        if not text:
            return "unknown"
        cyrillic_count = sum(1 for c in text[:100] if 1040 <= ord(c) <= 1103)
        if cyrillic_count > 10:
            return "ru"
        return "en"
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        # Пока просто возвращаем текст (заглушка)
        return f"[Перевод] {text}"
    
    def get_model_name(self, source_lang: str, target_lang: str) -> str:
        return "demo-model"

translation_service = TranslationService()