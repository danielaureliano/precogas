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

## CI/CD

Este projeto está preparado para integração contínua. A estrutura de testes garante que alterações na lógica de datas ou processamento sejam validadas antes do deploy.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.