# PrecoGas

**PrecoGas** é uma API desenvolvida em Python com **FastAPI**, projetada para monitorar e fornecer informações sobre o preço médio de combustíveis no Distrito Federal, com base nos dados publicados pela ANP (Agência Nacional do Petróleo).

## Funcionalidades

- Faz o download automático dos arquivos de levantamento de preços disponibilizados pela ANP.
- Extrai informações específicas da planilha, como **preço médio de revenda** para gasolina comum no Distrito Federal.
- Fornece um endpoint para consulta via API.

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

## Próximos Passos

Agora que tudo está funcionando, algumas melhorias podem ser feitas:

- 🚀 **Adicionar suporte a outros estados** (permitir que o usuário informe qual estado consultar).
- ⚡ **Implementar um sistema de cache** para evitar downloads repetitivos.
- 🛠️ **Criar testes automatizados** para garantir que o código continue funcionando mesmo se a ANP mudar o formato do arquivo.

## Como executar

### 1. Clone o repositório:
```bash
git clone https://github.com/danielaureliano/precogas/
cd precogas
```

### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Execute o Redis via Docker:
Certifique-se de que o Docker está instalado e rodando. Em seguida, execute:
```bash
docker run -d --name redis-local -p 6379:6379 redis
```

### 4. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

### 5. Acesse a API em `http://localhost:8000/precos`

### 6. Para ver a documentação interativa, acesse `http://localhost:8000/docs`

---

## Melhorias recentes

- 🔄 **Implementação de fallback automático:** Agora, caso o arquivo da semana mais recente ainda não esteja disponível no site da ANP, a aplicação tenta baixar arquivos das semanas anteriores automaticamente.
- 🐳 **Suporte ao Redis via Docker:** Adicionadas instruções e suporte para rodar o Redis em container Docker, facilitando o uso do cache localmente.
- ⚠️ **Tratamento de SSL:** Adicionada opção para ignorar verificação SSL em ambiente de desenvolvimento, evitando erros de certificado ao baixar arquivos da ANP.
