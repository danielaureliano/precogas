# PrecoGas

**PrecoGas** é uma API desenvolvida em Python com **FastAPI**, projetada para monitorar e fornecer informações sobre o preço médio de combustíveis no Distrito Federal, com base nos dados publicados pela ANP (Agência Nacional do Petróleo).

## Funcionalidades

- Faz o download automático dos arquivos de levantamento de preços disponibilizados pela ANP.
- Extrai informações específicas da planilha, como **preço médio de revenda** para gasolina comum no Distrito Federal.
- Fornece um endpoint para consulta via API.

## Estrutura do Projeto

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

## Endpoints

### `/precos` [GET]

Retorna as informações mais recentes do preço médio de gasolina comum no Distrito Federal:

- **DATA INICIAL**
- **DATA FINAL**
- **PREÇO MÉDIO REVENDA**

### Exemplo de Resposta

```json
{
  "DATA INICIAL": "2025-01-19",
  "DATA FINAL": "2025-01-25",
  "PREÇO MÉDIO REVENDA": 5.659
}

#### Exemplo de Requisição com `curl`
```bash
curl http://localhost:8000/precos
```


## Como Executar

O projeto pode ser executado localmente ou utilizando Docker/Docker Compose para facilitar o gerenciamento de dependências.

### 1. Clone o repositório:
```bash
git clone https://github.com/danielaureliano/precogas/
cd precogas
```

### Via Docker (Recomendado)

Esta é a forma recomendada de executar o PrecoGas, pois gerencia automaticamente a API e a instância do Redis.

1.  **Certifique-se de ter Docker e Docker Compose instalados.**
2.  **Na raiz do projeto, execute:**
    ```bash
    docker-compose up --build
    ```
    Isso irá construir as imagens e iniciar os serviços da API e do Redis.

A API estará disponível em: `http://localhost:8000/precos`
Para ver a documentação interativa, acesse: `http://localhost:8000/docs`

### Execução Local

Para executar a aplicação diretamente em seu ambiente local:

1.  **Crie e ative um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Inicie uma instância do Redis:**
    Certifique-se de ter o Redis instalado e rodando em `localhost:6379`, ou inicie-o via Docker:
    ```bash
    docker run -d --name redis-local -p 6379:6379 redis
    ```
4.  **Execute a aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```

A API estará disponível em: `http://localhost:8000/precos`
Para ver a documentação interativa, acesse: `http://localhost:8000/docs`

---

## CI/CD

Este projeto utiliza **GitHub Actions** para automação de CI/CD. Os workflows são configurados para:

*   Executar testes automatizados em cada *push* e *pull request*.
*   Realizar *deploy* automático para o Render.com na branch `main`.

Para mais detalhes, consulte os arquivos em `.github/workflows/`.

## Testes

No momento, o projeto **não possui testes automatizados** implementados. Esta é uma das próximas melhorias planejadas, conforme indicado no `TODO.md`.

## Contribuição

Agradecemos o seu interesse em contribuir com o PrecoGas! Siga os passos abaixo para começar:

1.  **Faça um Fork** do repositório.
2.  **Clone** o seu fork: `git clone https://github.com/SEU_USUARIO/precogas.git`
3.  Crie uma **branch** para a sua funcionalidade ou correção: `git checkout -b feature/minha-nova-funcionalidade`
4.  Certifique-se de que o seu ambiente de desenvolvimento esteja configurado e que todos os **testes** estejam passando.
5.  Faça suas alterações e **commit** com uma mensagem clara e descritiva (utilizando o padrão Conventional Commits).
6.  Envie suas alterações para o seu fork: `git push origin feature/minha-nova-funcionalidade`
7.  Abra um **Pull Request** para a branch `main` deste repositório, descrevendo suas alterações.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
