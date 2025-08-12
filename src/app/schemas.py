from pydantic import BaseModel, Field


class Message(BaseModel):
    question: str = Field(..., example="Привет, можно вопрос?")
    answer: str = Field(..., example="Привет, конечно!")


class AnswerResponse(BaseModel):
    answer: str = Field(
        ...,
        example="Например, мы делали бота для HR для Магнита, а ещё поиск по картинкам для KazanExpress",
    )


class QuestionRequest(BaseModel):
    question: str = Field(..., example="Что вы можете сделать для ритейлеров?")
    history: list[Message] = Field(default_factory=list)  # предыдущие вопросы и ответы
