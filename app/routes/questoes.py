from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.services import pdf_generator

router = APIRouter(prefix="/questoes", tags=["Questões"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.QuestaoOut)
def criar_questao(questao: schemas.QuestaoCreate, db: Session = Depends(get_db)):
    db_questao = models.Questao(**questao.dict())
    db.add(db_questao)
    db.commit()
    db.refresh(db_questao)
    return db_questao

@router.get("/", response_model=list[schemas.QuestaoOut])
def listar_questoes(db: Session = Depends(get_db)):
    return db.query(models.Questao).all()

@router.get("/gerar-pdf")
def gerar_pdf(db: Session = Depends(get_db)):
    questoes = db.query(models.Questao).all()
    caminho_pdf = pdf_generator.gerar_pdf(questoes)
    return {"pdf": caminho_pdf}
