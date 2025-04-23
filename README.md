# API Questions Platform

Este repositório contém a configuração Kubernetes/Helm para a API de Questões, uma plataforma para gerenciamento de perguntas e respostas.

## Pré-requisitos

- Kubernetes 1.19+
- Helm 3.2.0+
- ArgoCD (opcional, para CD)

## Estrutura do Repositório

```
api-questions/
├── Chart.yaml          # Metadados do Helm chart
├── values.yaml         # Valores configuráveis
├── templates/          # Templates Kubernetes
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── networkpolicy.yaml
│   ├── backup-cronjob.yaml
│   └── backup-pvc.yaml
└── README.md           # Esta documentação
```

## Instalação

### Usando Helm diretamente

```bash
# Adicionar repositório de dependências
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Instalar o chart
helm install api-questions ./
```

### Usando ArgoCD

```bash
kubectl apply -f argo-app.yaml
```

## Configuração

### Valores Padrão

Veja abaixo os valores padrão que podem ser sobrescritos:

| Parâmetro | Descrição | Valor Padrão |
|-----------|-----------|--------------|
| `api.replicaCount` | Número de réplicas da API | `2` |
| `api.image.repository` | Repositório da imagem Docker | `yourdockerhub/api-questions` |
| `api.image.tag` | Tag da imagem Docker | `1.0.0` |
| `api.service.type` | Tipo do serviço Kubernetes | `ClusterIP` |
| `api.service.port` | Porta do serviço | `80` |
| `postgresql.enabled` | Habilitar PostgreSQL interno | `true` |
| `postgresql.auth.username` | Usuário do PostgreSQL | `app_user` |
| `postgresql.auth.database` | Nome do banco de dados | `questions` |
| `postgresql.primary.persistence.size` | Tamanho do volume para PostgreSQL | `1Gi` |
| `ingress.enabled` | Habilitar Ingress | `false` |
| `backup.enabled` | Habilitar backup automático | `true` |
| `backup.schedule` | Cronograma de backup (formato cron) | `0 1 * * *` |

## Segurança

Este chart implementa várias medidas de segurança:

1. **Gerenciamento de Segredos**: Credenciais são armazenadas em Kubernetes Secrets
2. **Network Policies**: Restringe o tráfego de rede entre componentes
3. **Backup Automático**: Protege contra perda de dados
4. **Recursos Limitados**: Previne consumo excessivo de recursos

### Gerenciamento de Credenciais

Para maior segurança em ambientes de produção, recomenda-se:

1. Criar secrets manualmente antes da instalação:

```bash
kubectl create secret generic db-credentials \
  --from-literal=username=app_user \
  --from-literal=postgres-password=sua-senha-segura \
  --from-literal=user-password=sua-senha-segura
```

2. Referenciar o secret existente no values.yaml:

```yaml
postgresql:
  auth:
    existingSecret: "db-credentials"
```

## Monitoramento e Escalabilidade

O chart inclui:

- **Horizontal Pod Autoscaler**: Escala automaticamente baseado no uso de CPU
- **Liveness/Readiness Probes**: Monitora a saúde da aplicação
- **Resource Limits**: Previne consumo excessivo de recursos

## Backup e Recuperação

O sistema de backup automático:

- Executa backups diários do banco de dados
- Armazena backups compactados em um volume persistente
- Mantém um histórico configurável de backups
- Limpa automaticamente backups antigos

Para restaurar um backup:

```bash
# Listar backups disponíveis
kubectl exec -it <pod-do-postgresql> -- ls -la /backups

# Restaurar um backup específico
kubectl exec -it <pod-do-postgresql> -- bash -c "gunzip -c /backups/questions-20250423.sql.gz | psql -U app_user -d questions"
```

## Contribuição

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add some amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
