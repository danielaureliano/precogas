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
