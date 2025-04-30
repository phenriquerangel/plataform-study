import sys
import pdfkit
from jinja2 import Template
from sqlalchemy import create_engine, text
import os

ids = sys.argv[1].split(",")
db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)
with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM questoes WHERE id IN ({','.join(ids)})"))
    questoes = result.fetchall()

html = Template("""<h1>Prova Gerada</h1>{% for q in questoes %}<div><p><strong>{{ q.texto }}</strong></p><ul><li>A) {{ q.a }}</li><li>B) {{ q.b }}</li><li>C) {{ q.c }}</li><li>D) {{ q.d }}</li></ul><br></div>{% endfor %}""").render(questoes=questoes)

pdf_path = f"/pdfs/prova_{ids[0]}.pdf"
pdfkit.from_string(html, pdf_path)
print(f"PDF salvo em {pdf_path}")
