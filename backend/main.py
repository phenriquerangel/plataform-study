
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
from typing import List, Optional
from pydantic import BaseModel
import uuid
import boto3
from botocore.client import Config
import os
import tempfile
from fpdf import FPDF
from botocore.exceptions import BotoCoreError, NoCredentialsError



# Configurações MinIO
MINIO_ENDPOINT = "http://minio.minio.svc.cluster.local:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET = "questoes"

# Configuração DB
DB_HOST = os.getenv("POSTGRES_HOST", "postgres-postgresql.backend.svc.cluster.local")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "questoes")
DB_USER = os.getenv("POSTGRES_USER", "questuser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "questpass")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Inicializar app
app = FastAPI()

# CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão MinIO
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"
)

# Models SQLAlchemy
class QuestaoModel(Base):
    __tablename__ = "questoes"
    id = Column(String, primary_key=True, index=True)
    texto = Column(Text)
    resposta_correta = Column(Integer)
    origem = Column(String(7))
    imagem_url = Column(Text, nullable=True)
    opcoes = relationship("OpcaoModel", back_populates="questao", cascade="all, delete")

class OpcaoModel(Base):
    __tablename__ = "opcoes"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text)
    questao_id = Column(String, ForeignKey("questoes.id"))
    questao = relationship("QuestaoModel", back_populates="opcoes")

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Schemas Pydantic
class Opcao(BaseModel):
    texto: str

class QuestaoCreate(BaseModel):
    texto: str
    opcoes: List[Opcao]
    resposta_correta: int
    origem: str
    imagem_url: Optional[str] = None

class Questao(QuestaoCreate):
    id: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post("/upload-imagem/")
async def upload_imagem(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}-{file.filename}"
    content = await file.read()

    try:
        s3.create_bucket(Bucket=MINIO_BUCKET)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass

    s3.put_object(Bucket=MINIO_BUCKET, Key=filename, Body=content)

    return {"url": f"{MINIO_ENDPOINT}/{MINIO_BUCKET}/{filename}"}

@app.post("/questoes/", response_model=Questao)
def criar_questao(q: QuestaoCreate, db: Session = Depends(get_db)):
    q_id = str(uuid.uuid4())
    questao_db = QuestaoModel(
        id=q_id,
        texto=q.texto,
        resposta_correta=q.resposta_correta,
        origem=q.origem,
        imagem_url=q.imagem_url
    )
    for opcao in q.opcoes:
        questao_db.opcoes.append(OpcaoModel(texto=opcao.texto))
    db.add(questao_db)
    db.commit()
    db.refresh(questao_db)

    return Questao(
        id=q_id,
        texto=questao_db.texto,
        opcoes=[Opcao(texto=o.texto) for o in questao_db.opcoes],
        resposta_correta=questao_db.resposta_correta,
        origem=questao_db.origem,
        imagem_url=questao_db.imagem_url
    )

@app.get("/questoes/", response_model=List[Questao])
def listar_questoes(db: Session = Depends(get_db)):
    questoes = db.query(QuestaoModel).all()
    return [
        Questao(
            id=q.id,
            texto=q.texto,
            opcoes=[Opcao(texto=o.texto) for o in q.opcoes],
            resposta_correta=q.resposta_correta,
            origem=q.origem,
            imagem_url=q.imagem_url
        )
        for q in questoes
    ]

@app.delete("/questoes/{questao_id}")
def deletar_questao(questao_id: str, db: Session = Depends(get_db)):
    questao = db.query(QuestaoModel).filter(QuestaoModel.id == questao_id).first()
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    db.delete(questao)
    db.commit()
    return {"status": "removido"}

@app.post("/exportar-pdf/")
def exportar_pdf(ids: List[str], db: Session = Depends(get_db)):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for q_id in ids:
        questao = db.query(QuestaoModel).filter(QuestaoModel.id == q_id).first()
        if not questao:
            continue
        pdf.multi_cell(0, 10, f"Q: {questao.texto}")
        for idx, opcao in enumerate(questao.opcoes):
            pdf.multi_cell(0, 10, f"  {chr(65+idx)}. {opcao.texto}")
        pdf.ln()

    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, "lista_questoes.pdf")
    pdf.output(path)
    return FileResponse(path, media_type='application/pdf', filename="lista_questoes.pdf")

@app.get("/monitorar")
def monitorar():
    db_ok = False
    minio_ok = False

    # Testa banco de dados
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except:
        db_ok = False

    # Testa MinIO
    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        )
        s3_client.list_buckets()
        minio_ok = True
    except (BotoCoreError, NoCredentialsError, Exception):
        minio_ok = False

    return {
        "api": True,
        "db": db_ok,
        "minio": minio_ok
    }