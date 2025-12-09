import time
import uuid
import structlog.contextvars
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from app.services.downloader import baixar_arquivo, redis_client
from app.services.extractor import extrair_dados
from app.services.logger import setup_logger
from app.core.config import settings
import requests
import redis
from prometheus_client import Counter, Histogram, generate_latest

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de contexto para o ciclo de vida da aplicação (Startup/Shutdown).

    Executa verificações de inicialização críticas:
    1. Verifica se o diretório de saída para arquivos baixados existe ou pode ser criado.
    2. Verifica permissões de escrita nesse diretório.

    Se alguma verificação falhar, a aplicação não inicia (RuntimeError).

    Args:
        app (FastAPI): A instância da aplicação FastAPI.
    """
    # Startup Check
    logger.info("Iniciando verificações de startup...", status="startup_check_start")

    # Verificar diretório de dados
    if not settings.OUTPUT_DIR.exists():
        logger.info(f"Diretório {settings.OUTPUT_DIR} não existe. Tentando criar...", status="dir_creation")
        try:
            settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório {settings.OUTPUT_DIR} criado com sucesso.", status="dir_created")
        except Exception as e:
            logger.error(f"Falha crítica ao criar diretório {settings.OUTPUT_DIR}: {e}", status="dir_creation_failed")
            raise RuntimeError(f"Falha no startup: Não foi possível criar diretório de dados: {e}")

    # Verificar permissão de escrita
    try:
        test_file = settings.OUTPUT_DIR / ".write_test"
        test_file.touch()
        test_file.unlink()
        logger.info(f"Permissões de escrita em {settings.OUTPUT_DIR} verificadas: OK", status="write_permission_ok")
    except Exception as e:
        logger.error(f"Sem permissão de escrita em {settings.OUTPUT_DIR}: {e}", status="write_permission_failed")
        raise RuntimeError(f"Falha no startup: Sem permissão de escrita em {settings.OUTPUT_DIR}")

    logger.info("Verificações de startup concluídas com sucesso.", status="startup_check_success")
    yield
    # Shutdown logic
    logger.info("Encerrando aplicação...", status="shutdown")

app = FastAPI(lifespan=lifespan)

# Métricas Prometheus
REQUESTS_TOTAL = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "status_code"])
RESPONSE_TIME_SECONDS = Histogram("http_response_time_seconds", "HTTP Response Time", ["method", "endpoint"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware global para observabilidade.

    1. Gera um `trace_id` único para cada requisição.
    2. Calcula o tempo de processamento.
    3. Registra logs estruturados (Início/Fim).
    4. Coleta métricas para o Prometheus.

    Args:
        request (Request): Objeto da requisição HTTP.
        call_next (Callable): Função que processa a requisição e retorna a resposta.

    Returns:
        Response: A resposta HTTP processada.
    """
    start_time = time.time()

    # Gerar e vincular um trace_id para a requisição
    trace_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(trace_id=trace_id)
    logger.info("Iniciando requisição", method=request.method, endpoint=request.url.path, trace_id=trace_id)

    response = await call_next(request)
    process_time = time.time() - start_time

    # Registrar métricas
    REQUESTS_TOTAL.labels(method=request.method, endpoint=request.url.path, status_code=response.status_code).inc()
    RESPONSE_TIME_SECONDS.labels(method=request.method, endpoint=request.url.path).observe(process_time)

    logger.info("Finalizando requisição", method=request.method, endpoint=request.url.path, status_code=response.status_code, response_time_sec=process_time, trace_id=trace_id)

    return response

@app.get("/", include_in_schema=False)
async def root():
    """
    Redireciona a raiz para a documentação Redoc.
    """
    return RedirectResponse(url="/redoc")

@app.get("/precos")
async def obter_precos():
    """
    Endpoint principal para consulta de preços.

    Processo:
    1. Aciona o `baixar_arquivo` para obter a planilha mais recente (com cache).
    2. Aciona o `extrair_dados` para ler e filtrar as informações do DF.

    Returns:
        JSONResponse: Dados formatados ou erro 503 se indisponível.
    """
    logger.info("Processando requisição para /precos")
    # Baixa o arquivo mais recente
    url, data_inicio, data_fim, caminho_arquivo = baixar_arquivo()
    if not caminho_arquivo:
        logger.error("Arquivo da ANP não encontrado após tentativas de download.", status="download_failed")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"erro": "Arquivo não encontrado no site da ANP"})

    # Extrai os dados da planilha
    resultado = extrair_dados(caminho_arquivo)
    if not resultado:
        logger.error("Não foi possível extrair os dados para o Distrito Federal do arquivo baixado.", status="extraction_failed")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"erro": "Não foi possível extrair os dados para o Distrito Federal"})

    logger.info("Dados extraídos com sucesso para o Distrito Federal.", status="data_extracted")
    return resultado

@app.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da aplicação.
    Verifica a conectividade com a internet e com o Redis.
    """
    logger.info("Processando requisição para /health")
    status_checks = {}
    overall_status = status.HTTP_200_OK

    # 1. Verificar conectividade com a internet
    try:
        requests.head("https://www.google.com", timeout=5)
        status_checks["internet_connection"] = "OK"
        logger.info("Verificação de conectividade com a internet: OK", check="internet")
    except requests.exceptions.RequestException as e:
        status_checks["internet_connection"] = f"FAIL: {e}"
        overall_status = status.HTTP_503_SERVICE_UNAVAILABLE
        logger.error(f"Verificação de conectividade com a internet: FALHA - {e}", check="internet")

    # 2. Verificar conexão com Redis
    if redis_client:
        try:
            redis_client.ping()
            status_checks["redis_connection"] = "OK"
            logger.info("Verificação de conexão com Redis: OK", check="redis")
        except redis.exceptions.ConnectionError as e:
            status_checks["redis_connection"] = f"FAIL: {e}"
            overall_status = status.HTTP_503_SERVICE_UNAVAILABLE
            logger.error(f"Verificação de conexão com Redis: FALHA - {e}", check="redis")
    else:
        status_checks["redis_connection"] = "WARNING: Redis client not initialized (connection failed at startup)"
        logger.warning("Verificação de conexão com Redis: Cliente Redis não inicializado.", check="redis")

    # 3. Status do serviço principal (a API está de pé)
    status_checks["api_service"] = "OK"
    logger.info("Verificação do serviço da API: OK", check="api_service")

    return JSONResponse(status_code=overall_status, content={"status": "UP" if overall_status == status.HTTP_200_OK else "DOWN", "checks": status_checks})

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """
    Endpoint para expor métricas no formato Prometheus.
    """
    logger.info("Requisição recebida para /metrics", status="metrics_scrape")
    return PlainTextResponse(generate_latest().decode("utf-8"))
