import os
from dotenv import load_dotenv
from .links import EORA_LINKS
from pathlib import Path


load_dotenv()


class Settings:

    API_KEY = os.getenv("API_KEY")
    API_BASE_URL = "https://openrouter.ai/api/v1"
    CACHE_FILE_PATH = Path("eora_content_cache.json")
    LINKS = EORA_LINKS
    PAGE_LIMIT = 5_000  # Лимит текста одной страницы
    TOTAL_LIMIT = 200_000  # Общий лимит контента всех страниц
    OLD_MESSAGE_LIMIT = 500  # Лимит текста старых сообщений
    MODEL = "tngtech/deepseek-r1t2-chimera:free"

    def __init__(self):
        if not self.API_KEY:
            raise EnvironmentError("API_KEY environment variable not set")


settings = Settings()
