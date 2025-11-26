# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2025-11-26

### ✨ Features (Novas Funcionalidades)
- **deploy:** Adiciona configuração (`render.yaml`) para deploy automatizado no Render.com (1aff834)
- **cache:** Implementação de cache com Redis e Docker para otimizar performance (40d8aa8)
- **api:** Definição de endpoints e formato de resposta JSON (860f6b6)

### 🐛 Bug Fixes (Correções de Bugs)
- **deploy:** Corrigida string de conexão com Redis no ambiente Render (83a6cef)
- **etl:** Correção da extração de dados da planilha ANP (c2f50a0)

### ♻️ Refactor (Refatoração)
- **downloader:** Refatoração da lógica de download com fallback para semanas anteriores (7558213)

### 📝 Documentation (Documentação)
- **geral:** Padronização completa (README, LICENSE, SECURITY) e guias de contribuição (b5fec8a)
- **docs:** Criação de CHANGELOG, TODO e SECURITY.md

### 🔧 Chore (Manutenção)
- **ci:** Configuração de Workflows do GitHub Actions e templates de issue.
- **init:** Estrutura inicial e configurações do projeto.

---
*Release inicial do projeto PrecoGas.*