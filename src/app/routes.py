from functools import lru_cache
from fastapi import APIRouter, HTTPException
from .schemas import AnswerResponse, QuestionRequest
from .utils import scrape_eora_content, generate_context
from .config import settings
from openai import OpenAI

router = APIRouter(prefix="/api/v1")
ai_client = OpenAI(api_key=settings.API_KEY, base_url=settings.API_BASE_URL)


@lru_cache(maxsize=1)
def get_cached_context():
    content_dict = scrape_eora_content()
    return generate_context(content_dict)


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Endpoint to ask questions about EORA projects"""
    context = get_cached_context()

    messages = [
        {
            "role": "system",
            "content": "Ты дружелюбный профессииональный помощник-консультант, предоставляющий "
            "информацию о компании EORA и ее проектах. В своих ответах всегда указываешь источники информации,"
            " ссылки и контент тебе предоставляется каждый раз. Формат: [1], [2] в тексте и нумерованный список"
            "ссылок в конце.",
        },
    ]
    if request.history:
        for message in request.history:
            messages.append(
                {
                    "role": "user",
                    "content": f"{message.question[:settings.OLD_MESSAGE_LIMIT]}...",
                }
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": f"{message.answer[:settings.OLD_MESSAGE_LIMIT]}...",
                }
            )
    messages.append(
        {
            "role": "user",
            "content": f"Данные для анализа: {context}. Вопрос: {request.question}",
        }
    )
    try:
        completion = ai_client.chat.completions.create(
            model=settings.MODEL, messages=messages
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating answer: {str(e)}"
        )
    answer = completion.choices[0].message.content
    return {"answer": answer}
