# Roadmap e Tarefas (TODO)

## 🚀 Em Andamento
- (nenhuma)

## 📋 Pendentes
- (nenhuma)

## ✅ Concluído
- [x] **Startup Check:** Implementar verificação de existência e permissões de escrita no diretório de dados na inicialização da API.
- [x] **Dependências:** Melhorar sincronização de dependências.
- [x] **Processo:** Documentar estratégia de branches.
- [x] **Configuração:** Implementar configuração externa para regras de ETL (YAML).
- [x] **Segurança:** Monitoramento e correção de vulnerabilidades de dependências (realizado via limpeza e atualização do `requirements.txt`).
- [x] **Funcionalidade:** Adicionar suporte a outros estados na API (cancelado).
- [x] **Performance:** Garantir que a extração e transformação de dados em `extractor.py` utilizem estritamente funções vetorizadas do Pandas.
- [x] **Logs:** Revisão e implementação de logs estruturados (JSON) com `structlog` e integração de métricas Prometheus.
- [x] **Refatoração:** Usar `pathlib` para manipulação de arquivos (substituir `os.path.join`).
- [x] **Health Check:** Implementação da rota `/health` na API para verificar conexão com Redis e internet.
- [x] **Testes:** Suíte completa (Unitários, Integração) com cobertura de **92%**.
- [x] **CI/CD:** Workflow do GitHub Actions configurado para testes automatizados (`pytest`) e linting (`ruff`).
- [x] **Qualidade:** Cobertura de código > 80% garantida via `pytest-cov`.
- [x] **Cache:** Implementação de sistema de cache (Redis).
- [x] **Deploy:** Configuração para deploy automatizado no Render.com.
- [x] **Correção:** Ajuste na extração de dados e URLs da ANP.
- [x] **Infra:** Configuração de Docker Compose.
- [x] **Docs:** Atualização do `GEMINI.md` com diretrizes avançadas de desenvolvimento.
