from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="EORA LLM Q&A Service",
    description="API for answering questions about EORA projects using LLM",
    version="1.0.0"
)

app.include_router(router)