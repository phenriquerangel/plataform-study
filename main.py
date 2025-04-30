from fastapi import FastAPI
from app.routes import questoes
from app.database import Base, engine

# Cria as tabelas no banco automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Questões de Provas")
app.include_router(questoes.router)
