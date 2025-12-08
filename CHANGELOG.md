# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.10.0] - 2025-12-08

### ♻️ Refactor
- **Tipo:** `refactor`
- **Escopo:** `(etl)`
- **Descrição:** Implementação de validação estrita de schema e tipos na função `extrair_dados` (`extractor.py`). Agora verifica a existência de abas, colunas obrigatórias e tipos de dados (float) antes de processar, aumentando a resiliência contra mudanças no layout da planilha da ANP.

### 🔧 Chore
- **Tipo:** `chore`
- **Escopo:** `(deps)`
- **Descrição:** Atualização das dependências do projeto (`fastapi`, `pandas`, `pytest`, `ruff`, etc.) para as versões estáveis mais recentes.
- **Tipo:** `chore`
- **Escopo:** `(docs)`
- **Descrição:** Atualização do `GEMINI.md` com instruções de segurança para verificação de vulnerabilidades no contexto do projeto.

## [v1.9.0] - 2025-12-01

### ⚠ BREAKING CHANGE
- **Configuração:** A aplicação agora utiliza `pydantic-settings` para gerenciamento de configuração. As variáveis de ambiente (como `REDIS_URL`) devem ser definidas corretamente no ambiente ou em um arquivo `.env`. Constantes hardcoded foram removidas.

### ♻️ Refactor
- **Tipo:** `refactor`
- **Escopo:** `(core)`
- **Descrição:** Centralização das configurações da aplicação (URLs, caminhos, credenciais) no módulo `app.core.config`. Substituição de `os.getenv` e constantes espalhadas por acesso via objeto `settings` tipado.
- **Impacto:** Facilita a gestão de variáveis de ambiente, validação de configurações e testes.

## [v1.8.0] - 2025-11-28

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(startup)`
- **Descrição:** Implementação de Startup Checks na inicialização da aplicação para verificar a existência e permissões de escrita do diretório de dados (`dados_anp/`). A aplicação falha rápido se o diretório não puder ser criado ou não for gravável.
- **Impacto:** Garante a integridade e disponibilidade do sistema, evitando falhas em tempo de execução.

- **Tipo:** `feat`
- **Escopo:** `(dev-xp)`
- **Descrição:** Adição de script de verificação de dependências (`scripts/check_deps.py`) integrado ao `pre-commit` para garantir sincronia entre ambiente e `requirements.txt`.

### ♻️ Refactor
- **Tipo:** `refactor`
- **Escopo:** `(etl)`
- **Descrição:** Refatoração do `extractor.py` para usar um arquivo de configuração externo (`config/etl_rules.yaml`) para as regras de extração (nome da aba, linha do cabeçalho, filtros de estado/produto, colunas de saída).
- **Impacto:** Aumenta a flexibilidade e manutenibilidade da lógica de extração, desacoplando regras de negócio do código.

### 📝 Documentation
- **Tipo:** `docs`
- **Escopo:** `(process)`
- **Descrição:** Criação do `CONTRIBUTING.md` detalhando a estratégia de branches (Feature Branches) e fluxo de contribuição.

## [v1.7.0] - 2025-11-28

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(core)`
- **Descrição:** Refatoração do sistema de logs para utilizar **`structlog`** com output JSON estruturado, incluindo `timestamp`, `level`, `module`, `filename`, `lineno`, `func_name` e `trace_id`.
- **Impacto:** Melhora significativamente a observabilidade, depuração e integração com sistemas de monitoramento/logs centralizados.

- **Tipo:** `feat`
- **Escopo:** `(api)`
- **Descrição:** Implementação de métricas **Prometheus** (`requests_total` e `response_time_seconds`) via middleware, expostas no novo endpoint `/metrics`.
- **Impacto:** Permite monitoramento granular do desempenho e uso da API.

### 🐛 Bug Fixes
- **Tipo:** `fix`
- **Escopo:** `(api)`
- **Descrição:** Correção nos testes do `test_api.py` e `app/main.py` para compatibilidade com o novo comportamento do `structlog` e formato de `content-type` das métricas.

## [v1.6.0] - 2025-11-28

### ♻️ Refactor
- **Tipo:** `refactor`
- **Escopo:** `(core)`
- **Descrição:** Substituição de `os.path` e manipulações de string por `pathlib.Path` em todo o projeto (`downloader.py`, `extractor.py`), garantindo compatibilidade cross-platform e código mais moderno.

## [v1.5.0] - 2025-11-28

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(api)`
- **Descrição:** Implementação de um endpoint `/health` que verifica a conectividade com a internet e o status do Redis, retornando um JSON com o status de saúde da aplicação.
- **Impacto:** Melhora a monitorabilidade e confiabilidade da aplicação em ambientes de produção.

## [v1.4.0] - 2025-11-28

### ♻️ Refactor
- **Tipo:** `refactor`
- **Escopo:** `(core)`
- **Descrição:** Implementação de um módulo de log centralizado (`app/services/logger.py`) e substituição de todos os `print()` nos serviços `downloader`, `extractor` e `main` por chamadas de log padronizadas (INFO, WARNING, ERROR).
- **Impacto:** Melhora a observabilidade, depuração e auditoria da aplicação.

## [v1.3.1] - 2025-11-28

### 🔧 Chore
- **Tipo:** `chore`
- **Escopo:** `(git)`
- **Descrição:** Remoção do arquivo `.coverage` do controle de versão para evitar que artefatos de build sejam commitados.

## [v1.3.0] - 2025-11-28

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(dev-xp)`
- **Descrição:** Implementação de **Git Hooks** locais via `pre-commit`.
    *   Linting automático com **Ruff** antes de cada commit.
    *   Verificações de formatação (trailing whitespace, EOF, YAML).
- **Impacto:** Aumenta a produtividade ao detectar erros localmente e evita que código fora do padrão chegue ao CI.

### 🔧 Chore
- **Tipo:** `chore`
- **Escopo:** `(deps)`
- **Descrição:** Limpeza profunda do `requirements.txt` para remover dependências de ambiente Windows (`pywin32`) e bibliotecas não utilizadas, corrigindo falhas no CI Linux.

## [v1.2.2] - 2025-11-28

### 🔧 Chore
- **Tipo:** `chore`
- **Escopo:** `(ci)`
- **Descrição:** Integração do linter **Ruff** ao pipeline de GitHub Actions para garantir qualidade de código e estilo.
- **Tipo:** `chore`
- **Escopo:** `(deps)`
- **Descrição:** Adição de `ruff` às dependências de desenvolvimento (`requirements.txt`).

### 📝 Documentation
- **Tipo:** `docs`
- **Escopo:** `(ci)`
- **Descrição:** Atualização do `README.md` com detalhes sobre o pipeline de CI (Linting + Testes + Cobertura) e CD (Render).

## [v1.2.1] - 2025-11-28

### 🐛 Bug Fixes
- **Tipo:** `fix`
- **Escopo:** `(ci)`
- **Descrição:** Definição de permissões explícitas (`contents: read`) no workflow de CI para mitigar alerta de segurança do CodeQL (`actions/missing-workflow-permissions`).

### 📝 Documentation
- **Tipo:** `docs`
- **Escopo:** `(standards)`
- **Descrição:** Documentação detalhada das convenções de Conventional Commits, versionamento e regras de segurança (`git push` explícito) no `README.md` e `GEMINI.md`.
- **Tipo:** `docs`
- **Escopo:** `(quality)`
- **Descrição:** Inclusão de diretrizes de qualidade (SOLID, KISS, DRY, TDD) no contexto do projeto (`GEMINI.md`).

## [v1.2.0] - 2025-11-28

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(tests)`
- **Descrição:** Implementação de suíte completa de testes automatizados com `pytest` e `pytest-cov`. Cobertura de código elevada para 87%.
- **Impacto:** Garante a estabilidade e corretude das funcionalidades críticas (download, extração, API).

- **Tipo:** `feat`
- **Escopo:** `(ci)`
- **Descrição:** Configuração de Pipeline de CI no GitHub Actions. Executa testes e verifica cobertura em cada Push e PR.
- **Impacto:** Previne regressões e garante qualidade contínua.

### 🔒 Security
- **Tipo:** `fix`
- **Escopo:** `(deps)`
- **Descrição:** Atualização de dependências críticas (`starlette`, `urllib3`, `certifi`, etc.) para mitigar vulnerabilidades conhecidas.

### 📝 Documentation
- **Tipo:** `docs`
- **Escopo:** `(code)`
- **Descrição:** Adição de docstrings detalhadas aos arquivos de teste, explicando a finalidade de cada validação.

## [v1.1.0] - 2025-11-27

### 🐛 Bug Fixes
- **Tipo:** `fix`
- **Escopo:** `(core)`
- **Descrição:** Ajuste na lógica de geração de URLs da ANP para suportar o novo formato de datas (Segunda a Domingo) e nomenclatura de arquivos (`DDMMYYYY`).
- **Impacto:** Restaura o funcionamento do download de arquivos semanais.

### ✨ Features
- **Tipo:** `feat`
- **Escopo:** `(core)`
- **Descrição:** Implementação de `requests.Session` com política de retries automáticos e fallback de verificação SSL (aceita certificados inválidos se necessário).
- **Impacto:** Maior resiliência contra instabilidades do site `gov.br`.

- **Tipo:** `feat`
- **Escopo:** `(core)`
- **Descrição:** Tratamento de erro na conexão com Redis. Se o Redis estiver indisponível, a aplicação continua funcionando sem cache.

- **Tipo:** `feat`
- **Escopo:** `(tests)`
- **Descrição:** Adição de suíte de testes automatizados (`pytest`) cobrindo lógica de download e endpoints da API.

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
