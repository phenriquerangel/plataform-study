import streamlit as st
import requests

API_URL = "http://backend.backend.svc.cluster.local:8000"

st.set_page_config(page_title="Cadastro de Questões", layout="wide")
st.title("Cadastro de Questão")

texto = st.text_area("Texto da Questão")
origem = st.text_input("Origem (ex: MAT2024)")
opcoes = [st.text_input(f"Opção {chr(65+i)}") for i in range(4)]
correta = st.selectbox("Alternativa correta", options=list(range(4)), format_func=lambda i: chr(65+i))
imagem = st.file_uploader("Imagem (opcional)")

if st.button("Salvar"):
    data = {
        "texto": texto,
        "origem": origem,
        "resposta_correta": correta,
        "opcoes": [{"texto": o} for o in opcoes],
        "imagem_url": None,
    }
    # Envio da imagem (se houver)
    if imagem:
        files = {"file": (imagem.name, imagem, imagem.type)}
        res_img = requests.post(f"{API_URL}/upload-imagem/", files=files)
        if res_img.ok:
            data["imagem_url"] = res_img.json()["url"]
        else:
            st.error("Erro ao enviar imagem: " + res_img.text)
    # Cadastro da questão
    res = requests.post(f"{API_URL}/questoes/", json=data)
    if res.ok:
        st.success("Questão cadastrada com sucesso!")
    else:
        st.error(f"Erro ao cadastrar: {res.text}")