from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/questoes", tags=["Questoes"])


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
