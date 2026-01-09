import redis
import requests
import re
from pathlib import Path
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import timedelta
from app.services.logger import setup_logger
from app.core.config import settings
from app.services.time_sync import get_current_time

logger = setup_logger(__name__)

# Conexão com Redis (container rodando no Docker)
redis_client = None
try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    # Testa a conexão
    redis_client.ping()
    logger.info("Conectado ao Redis com sucesso!")
except redis.exceptions.ConnectionError as e:
    logger.warning(f"Não foi possível conectar ao Redis: {e}. O caching será desabilitado.")
    redis_client = None # Desabilita o cliente Redis se a conexão falhar

BASE_URL = settings.ANP_BASE_URL
OUTPUT_DIR = settings.OUTPUT_DIR
SEARCH_URL = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas"

def calcular_tempo_ate_proximo_domingo():
    """
    Calcula o tempo restante (em segundos) até o próximo domingo à meia-noite.

    Utiliza o serviço de sincronização de tempo (NTP) para obter a hora atual.
    O valor calculado é utilizado como TTL (Time To Live) para o cache no Redis.

    Returns:
        int: Número de segundos até o próximo domingo às 00:00:00.
    """
    hoje = get_current_time()
    proximo_domingo = hoje + timedelta(days=7 - hoje.weekday())
    proximo_domingo = proximo_domingo.replace(hour=0, minute=0, second=0, microsecond=0)
    return int((proximo_domingo - hoje).total_seconds())

def criar_sessao():
    """Cria uma sessão HTTP com política de retries."""
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    return session

def encontrar_url_mais_recente(session):
    """
    Realiza o scraping da página da ANP para encontrar a URL da planilha mais recente.

    Busca por links que terminam em '.xlsx' e contenham 'resumo_semanal' no href.

    Args:
        session (requests.Session): Sessão HTTP configurada para realizar a requisição.

    Returns:
        str | None: A URL completa do arquivo .xlsx se encontrado, ou None caso contrário.
    """
    logger.info(f"[Scraper] Buscando URL mais recente em: {SEARCH_URL}")
    try:
        response = session.get(SEARCH_URL, timeout=15)
        response.raise_for_status()

        # Encontrar todos os links que terminam em .xlsx
        # Regex captura o conteúdo do href
        links = re.findall(r'href=["\'](.*?\.xlsx)["\']', response.text, re.IGNORECASE)

        # Filtrar links que parecem ser o resumo semanal e validacao de dominio
        links_validos = []
        for link in links:
            if "resumo_semanal" in link.lower():
                # Validação de Segurança: Domínio deve ser gov.br
                parsed = urlparse(link)
                if parsed.netloc.endswith("gov.br"):
                    links_validos.append(link)
                else:
                    logger.warning(f"[Security] Link suspeito ignorado (domínio não confiável): {link}")

        if links_validos:
            # Assume que o primeiro link da página é o mais recente
            url_recente = links_validos[0]
            logger.info(f"[Scraper] URL encontrada: {url_recente}")
            return url_recente
        else:
            logger.warning("[Scraper] Nenhum link válido de planilha semanal encontrado na página.")
            return None

    except requests.RequestException as e:
        logger.error(f"[Scraper] Erro ao acessar a página da ANP: {e}")
        return None

def baixar_arquivo():
    """
    Orquestra o processo de download da planilha da ANP.

    1. Busca a URL mais recente via scraping.
    2. Verifica se o arquivo já existe no cache (Redis) ou disco local.
    3. Se não existir, realiza o download e salva no disco.
    4. Atualiza o cache com TTL até o próximo domingo.

    Returns:
        tuple: Uma tupla contendo:
            - url (str): URL do arquivo baixado.
            - data_inicio (None): Placeholder mantido para compatibilidade, sempre None.
            - data_fim (None): Placeholder mantido para compatibilidade, sempre None.
            - caminho_arquivo (Path): Caminho local onde o arquivo foi salvo.
            Retorna (None, None, None, None) em caso de falha.
    """
    session = criar_sessao()

    # 1. Obter URL dinâmica via scraping
    url = encontrar_url_mais_recente(session)

    if not url:
        logger.error("🚨 [Falha] Não foi possível obter a URL do arquivo.")
        return None, None, None, None

    # Extrair nome do arquivo da URL
    nome_arquivo = url.split('/')[-1]
    caminho_arquivo = OUTPUT_DIR / nome_arquivo

    # Cache key baseada no nome do arquivo (que deve ser único para cada semana)
    cache_key = f"arquivo_precos:{nome_arquivo}"

    # 2. Verificar Cache
    if redis_client:
        cached_path = redis_client.get(cache_key)
        if cached_path and Path(cached_path).exists():
            logger.info(f"[Cache] Usando arquivo em cache: {cached_path}")
            # Retornamos None para as datas pois elas serão extraídas do arquivo posteriormente
            return url, None, None, Path(cached_path)
    else:
        # Se sem redis, verifica se arquivo existe localmente
        if caminho_arquivo.exists():
             logger.info(f"[Local] Arquivo já existe no disco: {caminho_arquivo}")
             return url, None, None, caminho_arquivo

    logger.info(f"[Download] Iniciando download de: {url}")

    try:
        # Tenta com verificação SSL
        try:
            response = session.get(url, timeout=15, verify=True)
        except requests.exceptions.SSLError:
            logger.warning(f"[SSL] Falha na verificação de certificado para {url}. Tentando sem verificação...")
            response = session.get(url, timeout=15, verify=False)

        if response.status_code == 200:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with caminho_arquivo.open("wb") as f:
                f.write(response.content)

            if redis_client:
                cache_ttl = calcular_tempo_ate_proximo_domingo()
                redis_client.setex(cache_key, cache_ttl, str(caminho_arquivo))
                logger.info(f"[Sucesso] Arquivo baixado e cacheado: {caminho_arquivo}")
            else:
                logger.info(f"[Sucesso] Arquivo baixado: {caminho_arquivo}")

            return url, None, None, caminho_arquivo
        else:
            logger.error(f"[Erro] Falha ao baixar (Status {response.status_code}). URL: {url}")

    except requests.RequestException as e:
        logger.error(f"[Exceção] Erro na requisição: {e}. URL: {url}")

    return None, None, None, None
