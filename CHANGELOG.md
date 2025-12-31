# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🛡️ Security
- **Tipo:** `feat`
- **Escopo:** `(logging)`
- **Descrição:** Implementação de filtro de segurança (`mask_sensitive_data`) no `structlog`. Chaves sensíveis como `token`, `password` ou `key` são automaticamente substituídas por `***MASKED***` nos logs, prevenindo vazamentos acidentais de credenciais de CI/CD.
- **Tipo:** `feat`
- **Escopo:** `(http)`
- **Descrição:** Adição de `SecurityHeadersMiddleware` para injetar headers de proteção: HSTS (Strict-Transport-Security), X-Frame-Options (Anti-Clickjacking) e X-Content-Type-Options.

### 🏗️ Infrastructure
- **Tipo:** `chore`
- **Escopo:** `(docker)`
- **Descrição:** Atualização da imagem base para `python:3.12-slim`. Implementação de usuário não-root (`appuser`) para execução segura. Adição de healthchecks, volumes persistentes e limites de recursos (CPU/RAM) no `docker-compose.yml`.

### 📦 Dependencies
- **Tipo:** `chore`
- **Escopo:** `(deps)`
- **Descrição:** Atualização de bibliotecas principais: `fastapi` (0.128.0), `uvicorn` (0.40.0), `ruff` (0.14.10) e `pre-commit` (4.5.1).

### ⚙️ Configuration
- **Tipo:** `feat`
- **Escopo:** `(env)`
- **Descrição:** Adição de suporte a novas variáveis de ambiente para CI/CD e integrações: `GH_TOKEN`, `GEMINI_API_KEY`, `RENDER_DEPLOY_HOOK_URL`. Configuração do Pydantic para ignorar variáveis extras do sistema.
- **Tipo:** `chore`
- **Escopo:** `(vscode)`
- **Descrição:** Otimização do arquivo `precogas.code-workspace` para desenvolvimento em Windows com suporte nativo a Pytest e Ruff.

### 🚀 CI/CD
- **Tipo:** `ci`
- **Escopo:** `(github-actions)`
- **Descrição:** Integração de pipeline de CD para deploy automático no Render após sucesso dos testes na branch `main`.

## [v1.11.1] - 2025-12-09

### 🐛 Bug Fixes
- **Tipo:** `fix`
- **Escopo:** `(api)`
- **Descrição:** Adição de redirecionamento automático da rota raiz (`/`) para a documentação Redoc (`/redoc`). Isso corrige o erro 404 ao acessar a URL base da aplicação no Render.com.

## [v1.11.0] - 2025-12-09

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(core)`
- **Descrição:** Integração com **NTP (Network Time Protocol)** via `ntplib`. O sistema agora obtém a hora exata de `pool.ntp.org` para cálculos de TTL do cache, evitando inconsistências causadas pelo relógio local do servidor.
- **Impacto:** Maior precisão na expiração do cache e agendamento de tarefas.

- **Tipo:** `feat`
- **Escopo:** `(downloader)`
- **Descrição:** Refatoração da lógica de busca de arquivos da ANP. Substituição do cálculo de datas hardcoded por um **Scraper dinâmico** que acessa a página da ANP e identifica automaticamente o link da planilha semanal mais recente.
- **Impacto:** Resiliência total contra mudanças na nomenclatura dos arquivos (datas vs sequenciais) e datas de publicação irregulares.

### 🔒 Security
- **Tipo:** `chore`
- **Escopo:** `(audit)`
- **Descrição:** Execução de auditoria de dependências com `pip-audit`. Nenhuma vulnerabilidade conhecida encontrada.

### 📝 Documentation
- **Tipo:** `docs`
- **Escopo:** `(code)`
- **Descrição:** Atualização massiva de docstrings em todos os módulos principais (`main.py`, `downloader.py`, `extractor.py`) seguindo o padrão **Google Style** (PEP 257).
- **Tipo:** `docs`
- **Escopo:** `(readme)`
- **Descrição:** Revisão completa do `README.md` incluindo diagrama de fluxo, detalhamento de arquitetura, instalação e uso.

## [v1.10.1] - 2025-12-08
... (versões anteriores mantidas)
