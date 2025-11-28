from fastapi import FastAPI
from app.services.downloader import baixar_arquivo
from app.services.extractor import extrair_dados
from app.services.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI()

@app.get("/precos")
async def obter_precos():
    """
    Endpoint para obter o preço médio de gasolina no Distrito Federal.
    Retorna: DATA INICIAL, DATA FINAL e PREÇO MÉDIO REVENDA.
    """
    logger.info("Requisição recebida para /precos")
    # Baixa o arquivo mais recente
    url, data_inicio, data_fim, caminho_arquivo = baixar_arquivo()
    if not caminho_arquivo:
        logger.error("Arquivo da ANP não encontrado após tentativas de download.")
        return {"erro": "Arquivo não encontrado no site da ANP"}

    # Extrai os dados da planilha
    resultado = extrair_dados(caminho_arquivo)
    if not resultado:
        logger.error("Não foi possível extrair os dados para o Distrito Federal do arquivo baixado.")
        return {"erro": "Não foi possível extrair os dados para o Distrito Federal"}

    logger.info("Dados extraídos com sucesso para o Distrito Federal.")
    return resultado
