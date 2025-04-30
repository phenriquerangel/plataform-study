from sqlalchemy import Column, Integer, String
from app.database import Base

class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(1000), nullable=False)
    a = Column(String(100), nullable=False)
    b = Column(String(100), nullable=False)
    c = Column(String(100), nullable=False)
    d = Column(String(100), nullable=False)
    resposta = Column(String(1), nullable=False)
    origem = Column(String(7), nullable=False)
