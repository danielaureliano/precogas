# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
