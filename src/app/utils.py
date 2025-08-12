import json
from bs4 import BeautifulSoup
from .config import settings
import requests


def scrape_eora_content() -> dict[str, str]:
    """Scrape content from EORA website and cache it"""
    if settings.CACHE_FILE_PATH.exists():
        with open(settings.CACHE_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    content_dict = {}
    for url in settings.LINKS:
        try:
            responce = requests.get(url, timeout=10)
            soup = BeautifulSoup(responce.text, "html.parser")
            title = soup.find("h1").get_text() if soup.find("h1") else "Untitled"
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            content = f"{title}\n\n" + "\n".join(paragraphs)
            content_dict[url] = content
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            continue

    with open(settings.CACHE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(content_dict, f, ensure_ascii=False, indent=2)

    return content_dict


def generate_context(content_dict: dict[str, str]):
    """Generate context for LLM from scraped content"""
    context_parts = []
    for url, content in content_dict.items():
        context_parts.append(
            f"Контент из источника {url}: \n{content[:settings.PAGE_LIMIT]}..."
        )
        return "\n\n".join(context_parts)[: settings.TOTAL_LIMIT]
