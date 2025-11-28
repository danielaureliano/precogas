# PrecoGas

**PrecoGas** é uma API desenvolvida em Python com **FastAPI**, projetada para monitorar e fornecer informações sobre o preço médio de combustíveis no Distrito Federal, com base nos dados publicados pela ANP (Agência Nacional do Petróleo).

## Funcionalidades

- **Monitoramento Automático:** Baixa automaticamente os arquivos semanais de levantamento de preços da ANP (formato XLSX).
- **Resiliência:**
  - Suporta o novo padrão de URL da ANP (períodos de Segunda a Domingo).
  - Implementa tentativas automáticas (retries) em caso de falhas de rede.
  - Possui *fallback* automático para verificação SSL (tenta HTTPS padrão, mas aceita certificados inválidos se necessário, contornando problemas comuns em sites governamentais).
- **Cache:** Utiliza Redis para armazenar os arquivos baixados até a próxima atualização (domingo), economizando recursos.
- **API JSON:** Fornece um endpoint simples para integração.

## Estrutura do Projeto

```
precogas/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação (Definição da API)
│   ├── services/
│   │   ├── downloader.py       # Lógica de download, retry, SSL fallback e cache
│   │   └── extractor.py        # Processamento da planilha Excel (Pandas)
│   └── __init__.py
├── dados_anp/                  # Armazenamento temporário das planilhas
├── tests/                      # Testes automatizados
├── docker-compose.yml          # Orquestração (API + Redis)
├── requirements.txt            # Dependências
├── README.md                   # Documentação
└── TODO.md                     # Roadmap
```

## Endpoints

### `/precos` [GET]

Retorna as informações mais recentes do preço médio de gasolina comum no Distrito Federal.

#### Exemplo de Resposta

```json
{
  "dataInicial": "2025-01-19",
  "dataFinal": "2025-01-25",
  "precoMedioRevenda": 5.659
}
```

## Como Executar

### Via Docker (Recomendado)

A forma mais simples, pois gerencia a API e o Redis automaticamente.

1.  **Certifique-se de ter Docker e Docker Compose instalados.**
2.  **Na raiz do projeto, execute:**
    ```bash
    docker-compose up --build
    ```

A API estará disponível em: `http://localhost:8000/precos`

### Execução Local

1.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure o Redis:**
    O projeto espera um Redis rodando em `localhost:6379` (padrão).
    *Se o Redis não estiver disponível, o sistema funcionará, mas sem cache, baixando o arquivo a cada requisição.*
4.  **Execute a aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Testes

O projeto utiliza `pytest` para testes unitários e de integração.

Para executar os testes:

```bash
pytest
```

Isso irá executar:
- Testes da lógica de datas e URLs (mockando o tempo).
- Testes de download (mockando requisições HTTP e sistema de arquivos).
- Testes do endpoint `/precos` (simulando chamadas à API).

## Configuração de Desenvolvimento

Para garantir a qualidade do código localmente antes de enviar para o repositório, utilizamos **pre-commit hooks**.

### Instalação

1.  Instale as dependências de desenvolvimento:
    ```bash
    pip install -r requirements.txt
    ```
2.  Instale os hooks do git:
    ```bash
    pre-commit install
    ```

Agora, toda vez que você executar `git commit`, as verificações (Ruff, Pytest, etc.) rodarão automaticamente.

## CI/CD

Este projeto utiliza **GitHub Actions** para automação de CI. O workflow (`.github/workflows/ci.yml`) é acionado em todo *push* e *pull request* para a branch `main` e executa:

1.  **Linting:** Verificação de estilo e erros estáticos com **Ruff**.
2.  **Testes:** Execução de testes unitários e de integração com **Pytest**.
3.  **Cobertura:** Verificação se a cobertura de código é de pelo menos **80%**.

### Deploy Contínuo

O deploy é gerenciado pelo **Render.com** via Blueprint (`render.yaml`).
*   O Render monitora a branch `main`.
*   Após um push bem-sucedido (e idealmente após a aprovação do CI), o Render constrói o container Docker e atualiza o serviço.

## Convenções de Commit

Este projeto adota estritamente o padrão **Conventional Commits**. Todo commit deve seguir a estrutura:

```
<tipo>(<escopo opcional>): <descrição curta>

[corpo opcional]

[rodapé opcional - ex: BREAKING CHANGE, Closes #123]
```

### Tipos Permitidos:
*   `feat`: Nova funcionalidade.
*   `fix`: Correção de bug.
*   `docs`: Alterações apenas em documentação.
*   `style`: Formatação, ponto e vírgula faltando, etc. (não altera lógica).
*   `refactor`: Refatoração de código (sem nova funcionalidade ou correção de bug).
*   `test`: Adição ou correção de testes.
*   `chore`: Atualização de tarefas de build, configs de pacote, etc.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
