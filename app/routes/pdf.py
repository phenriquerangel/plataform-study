from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/questoes", tags=["PDF"])

@router.get("/pdf/{id}")
def baixar_pdf(id: int):
    pdf_path = f"/pdfs/prova_{id}.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type='application/pdf', filename=f"prova_{id}.pdf")
    return {"erro": "Arquivo não encontrado"}
