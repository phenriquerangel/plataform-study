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

html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <style>
    body { font-family: Georgia, serif; margin: 30px; line-height: 1.6; }
    .questao { margin-bottom: 40px; }
    .questao p { margin: 0 0 10px 0; }
    ol { padding-left: 20px; }
    ol li { margin-bottom: 5px; }
    .origem { font-style: italic; color: #666; font-size: 14px; }
  </style>
</head>
<body>
  <h1>Prova Gerada</h1>
  {% for q in questoes %}
  <div class='questao'>
    <p><strong>{{ q.texto }}</strong></p>
    <ol type='A'>
      <li>{{ q.a }}</li>
      <li>{{ q.b }}</li>
      <li>{{ q.c }}</li>
      <li>{{ q.d }}</li>
    </ol>
    <p class='origem'>Origem: {{ q.origem }}</p>
  </div>
  {% endfor %}
</body>
</html>
"""

html = Template(html_template).render(questoes=questoes)
pdf_path = f"/pdfs/prova_{ids[0]}.pdf"
pdfkit.from_string(html, pdf_path)
print(f"PDF salvo em {pdf_path}")
