from fastapi import FastAPI
from app.services.downloader import baixar_arquivo
from app.services.extractor import extrair_dados

app = FastAPI()

@app.get("/precos")
async def obter_precos():
    """
    Endpoint para obter o preço médio de gasolina no Distrito Federal.
    Retorna: DATA INICIAL, DATA FINAL e PREÇO MÉDIO REVENDA.
    """
    # Baixa o arquivo mais recente
    url, data_inicio, data_fim, caminho_arquivo = baixar_arquivo()
    if not caminho_arquivo:
        return {"erro": "Arquivo não encontrado no site da ANP"}
    
    # Extrai os dados da planilha
    resultado = extrair_dados(caminho_arquivo)
    if not resultado:
        return {"erro": "Não foi possível extrair os dados para o Distrito Federal"}
    
    return resultado