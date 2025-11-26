# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2025-11-26

### 📝 Documentation (Documentação)
- **geral:** Padronização completa da documentação (README, LICENSE, SECURITY) e guias de contribuição.
- **docs:** Criação oficial do CHANGELOG.md e TODO.md revisado.
- **license:** Adição da licença MIT.

### 🔧 Chore (Manutenção)
- **ci:** Configuração completa de Workflows do GitHub Actions (Issues, PRs, CI).

## [v0.4.0] - 2025-11-25

### ✨ Features
- **deploy:** Adiciona configuração (`render.yaml`) para deploy automatizado no Render.com, incluindo orquestração do serviço web e Redis.

## [v0.3.0] - 2025-01-30

### ✨ Features
- **cache:** Implementação de sistema de cache utilizando Redis e Docker para evitar downloads repetidos e melhorar a performance da API.

### 🐛 Bug Fixes
- **deploy:** Ajuste na string de conexão com Redis (`REDIS_URL`) para compatibilidade com ambiente de produção.

## [v0.2.0] - 2025-01-29

### 🐛 Bug Fixes
- **etl:** Correção crítica na extração de dados da planilha da ANP. Ajuste do parâmetro `skiprows` para considerar o cabeçalho na linha 10 e correção do nome da coluna "ESTADOS".

### ♻️ Refactor
- **downloader:** Refatoração da função de geração de URL para implementar fallback resiliente, buscando arquivos de até 3 semanas anteriores caso o atual não esteja disponível.

## [v0.1.0] - 2025-01-28

### 🎉 Initial
- **project:** Estrutura inicial do projeto PrecoGas (FastAPI, Uvicorn).
- **api:** Definição básica dos endpoints e serviços de download.
