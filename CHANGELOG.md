# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.13.0] - 2026-01-07

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(health)`
- **Descrição:** Adição da versão da aplicação na resposta do endpoint `/health`, facilitando o monitoramento de deploys e a verificação da versão ativa em produção.

### 🐛 Bug Fixes
- **Tipo:** `fix`
- **Escopo:** `(api)`
- **Descrição:** Ajuste rigoroso no formato das datas (`UNIX timestamp ms`) e fuso horário (`America/Sao_Paulo`) para total compatibilidade com a plataforma Bubble.io.
- **Descrição:** Implementação de validação de integridade cronológica (Data Inicial <= Data Final) no processamento ETL.

### 🧪 Tests
- **Tipo:** `test`
- **Escopo:** `(integration)`
- **Descrição:** Implementação de suíte de testes de integração (`tests/test_integration.py`) cobrindo o fluxo completo entre API, Downloader e Extrator com mocks de rede.
- **Descrição:** Aumento da cobertura de código global para 88%, garantindo robustez nas camadas de extração e tratamento de erros de scraper.

### ⚙️ Configuration
- **Tipo:** `chore`
- **Escopo:** `(config)`
- **Descrição:** Ajuste do `REDIS_URL` padrão para `127.0.0.1`, resolvendo conflitos de resolução de nome (`localhost`) observados em ambientes Windows durante o desenvolvimento local.

## [v1.12.2] - 2026-01-02

### 🐛 Bug Fixes
- **Tipo:** `fix`
- **Escopo:** `(api)`
- **Descrição:** Corrige `ResponseValidationError` ao garantir que a camada de extração de dados (`extractor`) retorne datas como `string` formatada (`dd/mm/aaaa`), em vez de objetos `Timestamp`, alinhando a saída ao schema Pydantic.

### 🧪 Tests
- **Tipo:** `test`
- **Escopo:** `(extractor)`
- **Descrição:** Adiciona teste unitário para validar que o tipo e o formato das datas retornadas pelo `extractor` são `string` no padrão `dd/mm/aaaa`.

## [v1.12.1] - 2026-01-02

### 🛡️ Security
- **Tipo:** `fix`
- **Escopo:** `(history)`
- **Descrição:** Reescrita completa do histórico Git para remoção de artefatos sensíveis e configurações inseguras antigas.
- **Tipo:** `fix`
- **Escopo:** `(config)`
- **Descrição:** Remoção de valores padrão inseguros (`:-`) no `docker-compose.yml`, forçando o uso de variáveis de ambiente seguras para o Redis.
- **Tipo:** `chore`
- **Escopo:** `(auth)`
- **Descrição:** Remoção da complexidade de `API_ACCESS_TOKEN` para manter a API pública e simplificada, focando a segurança na infraestrutura.

### 📝 Documentation
- **Tipo:** `docs`
- **Escopo:** `(openapi)`
- **Descrição:** Implementação de Schemas Pydantic (`PrecoGasolinaResponse`, `HealthCheckResponse`) para gerar exemplos de resposta ricos e precisos no Redoc/Swagger.
- **Tipo:** `docs`
- **Escopo:** `(readme)`
- **Descrição:** Atualização das instruções de segurança e remoção de referências obsoletas a tokens de API.

## [v1.12.0] - 2025-12-31

### 🛡️ Security
- **Tipo:** `feat`
- **Escopo:** `(rate-limit)`
- **Descrição:** Implementação de Rate Limiting com `slowapi` e Redis. Limites: 10 req/min (/precos) e 60 req/min (/health). Retorna HTTP 429 em caso de abuso.
- **Tipo:** `fix`
- **Escopo:** `(deps)`
- **Descrição:** Atualização crítica do `filelock` para v3.20.1 (CVE-2025-68146).
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

[v1.12.3]: https://github.com/danielaureliano/precogas/compare/v1.12.2...v1.12.3
[v1.12.2]: https://github.com/danielaureliano/precogas/compare/v1.12.1...v1.12.2
[v1.12.1]: https://github.com/danielaureliano/precogas/compare/v1.12.0...v1.12.1
[v1.12.0]: https://github.com/danielaureliano/precogas/compare/v1.11.1...v1.12.0
[v1.11.1]: https://github.com/danielaureliano/precogas/compare/v1.11.0...v1.11.1
[v1.11.0]: https://github.com/danielaureliano/precogas/compare/v1.10.1...v1.11.0
[v1.10.1]: https://github.com/danielaureliano/precogas/releases/tag/v1.10.1
