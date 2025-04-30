from fastapi import FastAPI
from app.routes import questoes

app = FastAPI(title="API de Questões de Provas")
app.include_router(questoes.router)
