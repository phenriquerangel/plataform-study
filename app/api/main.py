from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo da questão
class Questao(BaseModel):
    id: int
    texto: str
    respostas: List[str]
    origem: str

# Banco de dados simulado em memória
banco_questoes = []

@app.get("/questoes")
def listar_questoes():
    return banco_questoes

@app.post("/questoes")
def adicionar_questao(questao: Questao):
    banco_questoes.append(questao)
    return questao

@app.delete("/questoes/{id}")
def deletar_questao(id: int):
    for index, questao in enumerate(banco_questoes):
        if questao.id == id:
            banco_questoes.pop(index)
            return {"mensagem": f"Questão com ID {id} deletada com sucesso."}
    raise HTTPException(status_code=404, detail=f"Questão com ID {id} não encontrada.")
