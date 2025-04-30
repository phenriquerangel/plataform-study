import pdfkit
import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def gerar_pdf(questoes):
    template = env.get_template("modelo.html")
    html = template.render(questoes=questoes)
    caminho_pdf = "/app/output/prova.pdf"
    os.makedirs("/app/output", exist_ok=True)
    pdfkit.from_string(html, caminho_pdf)
    return caminho_pdf
