from sqlalchemy import Column, Integer, String
from .database import Base

class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(1000))
    a = Column(String(100))
    b = Column(String(100))
    c = Column(String(100))
    d = Column(String(100))
    resposta = Column(String(1))
    origem = Column(String(7))
