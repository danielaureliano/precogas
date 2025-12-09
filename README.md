# PrecoGas API

[![CI Pipeline](https://github.com/DanAureliano/precogas/actions/workflows/ci.yml/badge.svg)](https://github.com/DanAureliano/precogas/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

API RESTful de alta performance desenvolvida com **FastAPI** para monitoramento automatizado do preço médio da gasolina comum no Distrito Federal. O sistema extrai dados diretamente das planilhas semanais públicas da **ANP** (Agência Nacional do Petróleo).

---

## 🚀 Funcionalidades Principais

*   **Extração Automatizada (ETL):** Monitora o site da ANP, identifica e baixa a planilha semanal mais recente.
*   **API Rápida e Documentada:** Endpoints REST documentados automaticamente (Swagger UI/ReDoc).
*   **Cache Inteligente:** Utiliza **Redis** para cachear arquivos e respostas, reduzindo latência e tráfego na fonte (ANP).
*   **Sincronização de Tempo (NTP):** Garante precisão temporal via `pool.ntp.org` para expiração de cache.
*   **Observabilidade Completa:**
    *   Logs estruturados em JSON (`structlog`) com Trace ID distribuído.
    *   Métricas Prometheus nativas (`requests_total`, `response_time`).
    *   Health checks para dependências (Internet, Redis).
*   **Resiliência:** Políticas de *Retry* automáticos, Fallbacks de SSL e tratamento robusto de erros.

---

## 🏗️ Arquitetura

O sistema opera em um fluxo contínuo de ETL On-Demand:

1.  **Requisição:** O cliente chama `GET /precos`.
2.  **Scraper (Downloader):** O serviço acessa a página da ANP, varre o HTML em busca do link `.xlsx` mais recente (dinamicamente).
3.  **Cache Check (Redis):** Verifica se este arquivo já foi baixado e processado.
    *   *Miss:* Baixa o arquivo, salva em disco e atualiza o cache com TTL calculado via NTP (até o próximo domingo).
    *   *Hit:* Serve o arquivo local.
4.  **Extractor (Pandas):** Lê o arquivo Excel, valida o schema (abas e colunas esperadas via configuração YAML), filtra por "DISTRITO FEDERAL" e "GASOLINA COMUM".
5.  **Response:** Retorna o JSON com datas e preço médio.

---

## 🛠️ Tecnologias

*   **Core:** Python 3.11+, FastAPI, Uvicorn.
*   **Dados:** Pandas, OpenPyXL, NumPy.
*   **Infra:** Docker, Docker Compose, Redis.
*   **Qualidade:** Pytest (Testes), Ruff (Linting), Pre-Commit.
*   **Utils:** HTTPX, Requests, Tenacity, Structlog, Prometheus Client, NTPlib.

---

## 📦 Instalação e Execução

### Pré-requisitos
*   Docker & Docker Compose (Recomendado)
*   Ou Python 3.11+ instalado localmente

### Opção 1: Via Docker (Produção/Simples)

Esta é a maneira mais rápida de rodar a aplicação completa (API + Redis).

```bash
# Clone o repositório
git clone https://github.com/DanAureliano/precogas.git
cd precogas

# Suba os containers
docker-compose up --build -d

# Acompanhe os logs
docker-compose logs -f app
```

A API estará disponível em: `http://localhost:8000`

### Opção 2: Desenvolvimento Local

1.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Suba o Redis (Opcional, mas recomendado):**
    ```bash
    docker run -d -p 6379:6379 redis
    ```
    *Nota: Se não houver Redis, a aplicação funcionará, mas sem cache.*

4.  **Configure o ambiente (.env):**
    Copie o exemplo (se houver) ou defina as variáveis. O padrão já funciona localmente.

5.  **Execute a API:**
    ```bash
    uvicorn app.main:app --reload
    ```

---

## 📚 Documentação da API

Com a aplicação rodando, acesse a documentação interativa:

*   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Principais Endpoints

*   `GET /precos`: Retorna o preço atual da gasolina no DF.
*   `GET /health`: Status de saúde (Redis, Internet).
*   `GET /metrics`: Métricas para Prometheus.

---

## 🧪 Testes e Qualidade

O projeto segue rigorosos padrões de qualidade.

**Executar Testes Unitários:**
```bash
pytest
```

**Verificar Cobertura:**
```bash
pytest --cov=app tests/
```

**Rodar Linter (Ruff):**
```bash
ruff check .
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre o nosso código de conduta e o processo de envio de pull requests.

1.  Faça um Fork do projeto.
2.  Crie sua Feature Branch (`git checkout -b feat/nova-feature`).
3.  Commit suas mudanças seguindo **Conventional Commits** (`git commit -m 'feat: adiciona nova feature'`).
4.  Push para a Branch (`git push origin feat/nova-feature`).
5.  Abra um Pull Request.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.
