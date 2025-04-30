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


@router.delete("/{questao_id}")
def deletar_questao(questao_id: int, db: Session = Depends(get_db)):
    questao = db.query(models.Questao).filter(models.Questao.id == questao_id).first()
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    db.delete(questao)
    db.commit()
    return {"ok": True}
