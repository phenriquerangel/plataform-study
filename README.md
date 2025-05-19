# 🧠 Plataforma de Geração de Listas de Questões

Esta é uma plataforma completa para professores do ensino fundamental e médio criarem, armazenarem e exportarem listas de questões em PDF. A aplicação é dividida em **frontend React**, **backend FastAPI**, **banco de dados PostgreSQL** e **armazenamento de imagens no MinIO**, tudo orquestrado com **Kubernetes**, **Helm** e **Terraform**.

---

## 📦 Tecnologias Utilizadas

- **Frontend:** React + Vite + TailwindCSS
- **Backend:** FastAPI (Python 3.11)
- **Banco de Dados:** PostgreSQL
- **Armazenamento de Imagens:** MinIO
- **Infraestrutura:** Kubernetes com Helm Charts e Terraform
- **CI/CD:** GitHub Actions + DockerHub
- **Monitoramento:** Prometheus + Grafana
- **Logs:** Elasticsearch + Kibana + Fluent Bit

---

## 🚀 Funcionalidades Principais

- Cadastro de questões com:
  - Texto da pergunta
  - 4 alternativas
  - Marcação da correta
  - Origem (campo identificador)
  - Upload de imagem (opcional)
- Listagem de questões com:
  - Seleção para geração de PDF
  - Exclusão de itens
- Exportação para PDF
- Tela de **Monitoramento** (verifica conexão com backend, banco e MinIO)

---

## 🛠️ Instalação - Passo a Passo

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd plataforma
```

---

### 2. Suba o cluster Kubernetes local (se necessário)

Recomenda-se usar `kind`, `minikube` ou `k3d`.

---

### 3. Instale as dependências com Terraform

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

Isso irá provisionar:
- Namespaces
- PostgreSQL com PVC
- Backend FastAPI com Helm
- Frontend React com Helm
- MinIO
- Prometheus + Grafana + ELK stack

---

### 4. Verifique os serviços

```bash
kubectl get all -A
```

Garanta que todos os pods estão em estado `Running`.

---

### 5. Acesse o Frontend

Se estiver rodando localmente:

```bash
kubectl port-forward svc/frontend -n frontend 8080:80
```

Abra no navegador: [http://localhost:8080](http://localhost:8080)

---

### 6. Acesse o Backend (API Docs)

```bash
kubectl port-forward svc/backend -n backend 8000:8000
```

Abra: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 7. Acesse o Grafana

```bash
kubectl port-forward svc/grafana -n monitoring 3000:3000
```

Login padrão:
- **Usuário:** admin
- **Senha:** admin

---

## 📁 Estrutura de Pastas

```
plataforma/
├── frontend/          # Aplicação React
├── backend/           # API FastAPI
├── charts/            # Helm Charts de cada componente
├── terraform/         # Infraestrutura declarada em Terraform
```

---

## 🔄 Deploy automático

1. Todo `git push` em `main`:
   - Gera imagem Docker do backend e frontend
   - Publica no DockerHub
2. Basta aplicar com Helm:

```bash
helm upgrade --install backend charts/backend -n backend
helm upgrade --install frontend charts/frontend -n frontend
```

---

## 👨‍🏫 Painel de Monitoramento

Na aba "Monitoramento" do frontend, você pode verificar:
- Conexão com a API
- Status do Banco de Dados
- Status do MinIO

---

## 🙋 Dúvidas?

Abra uma issue ou envie sugestões via Pull Request. Este projeto é modular e pode ser estendido para:

- Autenticação de usuários
- Banco externo (RDS, Cloud SQL)
- Geração de relatórios estatísticos por turma