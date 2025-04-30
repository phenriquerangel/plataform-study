from pydantic import BaseModel

class QuestaoCreate(BaseModel):
    texto: str
    a: str
    b: str
    c: str
    d: str
    resposta: str
    origem: str

class QuestaoOut(QuestaoCreate):
    id: int

    class Config:
        orm_mode = True
