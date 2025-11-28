from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.services.downloader import baixar_arquivo, redis_client
from app.services.extractor import extrair_dados
from app.services.logger import setup_logger
import requests
import redis # Adicionando importação de redis

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
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"erro": "Arquivo não encontrado no site da ANP"})

    # Extrai os dados da planilha
    resultado = extrair_dados(caminho_arquivo)
    if not resultado:
        logger.error("Não foi possível extrair os dados para o Distrito Federal do arquivo baixado.")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"erro": "Não foi possível extrair os dados para o Distrito Federal"})

    logger.info("Dados extraídos com sucesso para o Distrito Federal.")
    return resultado

@app.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da aplicação.
    Verifica a conectividade com a internet e com o Redis.
    """
    logger.info("Requisição recebida para /health")
    status_checks = {}
    overall_status = status.HTTP_200_OK

    # 1. Verificar conectividade com a internet
    try:
        requests.head("https://www.google.com", timeout=5)
        status_checks["internet_connection"] = "OK"
        logger.info("Verificação de conectividade com a internet: OK")
    except requests.exceptions.RequestException as e:
        status_checks["internet_connection"] = f"FAIL: {e}"
        overall_status = status.HTTP_503_SERVICE_UNAVAILABLE
        logger.error(f"Verificação de conectividade com a internet: FALHA - {e}")

    # 2. Verificar conexão com Redis
    if redis_client:
        try:
            redis_client.ping()
            status_checks["redis_connection"] = "OK"
            logger.info("Verificação de conexão com Redis: OK")
        except redis.exceptions.ConnectionError as e:
            status_checks["redis_connection"] = f"FAIL: {e}"
            overall_status = status.HTTP_503_SERVICE_UNAVAILABLE
            logger.error(f"Verificação de conexão com Redis: FALHA - {e}")
    else:
        status_checks["redis_connection"] = "WARNING: Redis client not initialized (connection failed at startup)"
        logger.warning("Verificação de conexão com Redis: Cliente Redis não inicializado.")

    # 3. Status do serviço principal (a API está de pé)
    status_checks["api_service"] = "OK"
    logger.info("Verificação do serviço da API: OK")

    return JSONResponse(status_code=overall_status, content={"status": "UP" if overall_status == status.HTTP_200_OK else "DOWN", "checks": status_checks})
