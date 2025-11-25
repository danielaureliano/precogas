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
*   **Requisições HTTP:** Requests (com tratamento de SSL)
*   **Infraestrutura:** Docker & Docker Compose
*   **Cache:** Redis (Configurado no Docker, implementação no código listada como TODO)

## 📂 Estrutura do Projeto
```
precogas/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação (Definição da API)
│   ├── services/
│   │   ├── downloader.py       # Lógica de raspagem e download dos arquivos da ANP
│   │   └── extractor.py        # Lógica de processamento da planilha Excel (Pandas)
│   └── __init__.py
├── dados_anp/                  # Diretório para armazenamento temporário das planilhas baixadas
├── docker-compose.yml          # Orquestração dos serviços (API + Redis)
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação geral
└── TODO.md                     # Lista de tarefas e melhorias futuras
```

## 🚀 Como Executar

### Via Docker (Recomendado)
O projeto possui um `docker-compose.yml` que sobe a API e um contêiner Redis.
```bash
docker-compose up --build
```
A API estará disponível em: `http://localhost:8000/precos`

### Deploy no Render.com
O projeto já está configurado com um arquivo `render.yaml` (Blueprint) para deploy automatizado.

1.  No painel do Render, clique em **New +** e selecione **Blueprint**.
2.  Conecte este repositório.
3.  O Render detectará automaticamente os serviços definidos em `render.yaml`:
    *   **precogas-api:** Serviço Web (Python/FastAPI).
    *   **redis-cache:** Instância Redis gerenciada.
4.  Clique em **Apply** para iniciar o deploy.

### Execução Local
1.  **Instalar dependências:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Iniciar Redis (Opcional/Dependência):**
    Necessário ter uma instância Redis rodando (padrão: localhost:6379) se o código estiver configurado para usá-lo.
3.  **Rodar o servidor:**
    ```bash
    uvicorn app.main:app --reload
    ```

## 🧩 Convenções de Desenvolvimento
*   **Idioma:** Código, comentários e commits em **Português**.
*   **Estrutura de Código:** Separação clara de responsabilidades em `services/` (download vs extração).
*   **Tratamento de Erros:** A aplicação deve ser resiliente a falhas no site da ANP (ex: arquivo indisponível), tentando semanas anteriores automaticamente.
*   **Parsing de Dados:** As planilhas da ANP possuem cabeçalhos na linha 10 (índice 9 do Pandas).

## 📝 Roadmap (TODO)
Conforme `TODO.md`:
*   [ ] 🚀 Adicionar suporte a outros estados (parâmetro na URL).
*   [ ] ⚡ Implementar sistema de cache (Redis) para evitar downloads repetidos do mesmo arquivo.
*   [ ] 🛠️ Criar testes automatizados.
