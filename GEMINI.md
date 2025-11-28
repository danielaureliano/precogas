# Contexto do Projeto: PrecoGas

## 📋 Visão Geral
O **PrecoGas** é uma API RESTful desenvolvida em **Python** com **FastAPI**. Seu objetivo principal é monitorar e fornecer o preço médio de revenda da gasolina comum no Distrito Federal (DF), utilizando dados públicos disponibilizados pelas planilhas semanais da ANP (Agência Nacional do Petróleo).

O sistema automatiza o processo de:
1.  Identificar e baixar a planilha mais recente do site da ANP (com fallback para semanas anteriores).
2.  Processar o arquivo Excel (XLSX) para extrair dados específicos.
3.  Expor esses dados através de um endpoint JSON.

## 🛠️ Tecnologias e Ferramentas
*   **Linguagem:** Python 3.x
*   **Framework Web:** FastAPI
*   **Servidor:** Uvicorn
*   **Processamento de Dados:** Pandas, OpenPyXL
*   **Requisições HTTP:** Requests (com tratamento de SSL e retries)
*   **Infraestrutura:** Docker & Docker Compose
*   **Cache:** Redis
*   **Testes:** Pytest (Unitários e Integração)
*   **CI/CD:** GitHub Actions

## 📂 Estrutura do Projeto
```
precogas/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação (Definição da API)
│   ├── services/
│   │   ├── downloader.py       # Lógica de download, cache e resiliência
│   │   └── extractor.py        # Lógica de processamento ETL
│   └── __init__.py
├── tests/                      # Suíte de testes automatizados
├── dados_anp/                  # Armazenamento temporário
├── docker-compose.yml          # Orquestração
├── requirements.txt            # Dependências
├── README.md                   # Documentação
└── TODO.md                     # Roadmap
```

## 🚀 Como Executar

### Via Docker (Recomendado)
O projeto possui um `docker-compose.yml` que sobe a API e um contêiner Redis.
```bash
docker-compose up --build
```
A API estará disponível em: `http://localhost:8000/precos`

### Execução Local
1.  **Instalar dependências:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Iniciar Redis (Opcional):**
    O sistema tentará conectar em `localhost:6379`. Se falhar, funcionará sem cache.
3.  **Rodar o servidor:**
    ```bash
    uvicorn app.main:app --reload
    ```

## 🛡️ Diretrizes de Qualidade e Desenvolvimento

Todo código gerado, refatorado ou revisado deve seguir estritamente estas regras:

### 1. Arquitetura e Design
*   **Princípios:** Seguir **SOLID**, **KISS** (Simplicidade) e **DRY** (Não repetir código).
*   **Código Idiomático:** Escrever código Pythonico (PEP 8), priorizando legibilidade.
*   **Tipagem:** Utilizar **Tipagem Estática** (`type hints`) em todas as assinaturas de função e classe.

### 2. Robustez e Segurança
*   **Validação:** Implementar validações robustas de dados (entrada/saída).
*   **Exceções:** Tratamento explícito de exceções (`try/except` específicos). Evitar `except Exception` genérico silencioso.
*   **Segredos:** **JAMAIS** commitar credenciais, chaves ou senhas. Usar variáveis de ambiente.

### 3. Testes e Documentação
*   **Testes:** Todo código novo deve ter testes unitários e/ou de integração (Pytest). Manter cobertura >= 80%.
*   **Docstrings:** Documentar todas as funções, classes e módulos com docstrings claras (Google ou NumPy style).
*   **Linting:** O código deve passar por verificação de estilo e qualidade.

### 4. Ciclo de Vida e Versionamento
*   **Commits:** Usar **Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
*   **CI/CD:** O código deve passar pelo pipeline de integração contínua (testes automatizados) antes de ser integrado à branch principal.
*   **Push:** Qualquer comando `git push` requer **autorização explícita** do usuário antes de ser executado.

## 📝 Roadmap (TODO)
Conforme `TODO.md`:
*   [ ] 🚀 Adicionar suporte a outros estados (parâmetro na URL).
*   [ ] 🔒 Monitorar vulnerabilidades de dependências (Dependabot).
*   [x] ⚡ Implementar sistema de cache (Redis).
*   [x] 🛠️ Criar testes automatizados.