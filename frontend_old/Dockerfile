# Etapa de build
FROM node:20 AS builder
WORKDIR /app

# Copia todos os arquivos para dentro do container
COPY . .

# Garante que o .env está presente e dependências estejam instaladas antes do build
RUN npm install
RUN npm run build

# Etapa de produção
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]