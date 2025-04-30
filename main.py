from fastapi import FastAPI, Request
from app.routes import questoes, pdf
from app.database import Base, engine
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

Base.metadata.create_all(bind=engine)
app = FastAPI(title="API de Questões de Provas")

total_requests = Counter("api_requests_total", "Total de requisições na API")

@app.middleware("http")
async def count_requests(request: Request, call_next):
    total_requests.inc()
    return await call_next(request)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(questoes.router)
app.include_router(pdf.router)
