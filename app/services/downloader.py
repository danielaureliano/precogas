import os
import redis
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta

#Pegamos a URL do Redis da variável de ambiente
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Conexão com Redis (container rodando no Docker)
redis_client = None
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    # Testa a conexão
    redis_client.ping()
    print("Conectado ao Redis com sucesso!")
except redis.exceptions.ConnectionError as e:
    print(f"Não foi possível conectar ao Redis: {e}. O caching será desabilitado.")
    redis_client = None # Desabilita o cliente Redis se a conexão falhar

BASE_URL = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc"
OUTPUT_DIR = "./dados_anp/"

def calcular_tempo_ate_proximo_domingo():
    """Calcula quantos segundos faltam até o próximo domingo à meia-noite."""
    hoje = datetime.now()
    proximo_domingo = hoje + timedelta(days=7 - hoje.weekday())
    proximo_domingo = proximo_domingo.replace(hour=0, minute=0, second=0, microsecond=0)
    return int((proximo_domingo - hoje).total_seconds())

def gerar_dados_semana(semanas_atras=0):
    """
    Gera os dados da semana (datas de início e fim) baseados no deslocamento.
    A ANP usa períodos de Segunda a Domingo.
    """
    hoje = datetime.now()
    # Lógica para encontrar o domingo da semana retrasada (base de cálculo)
    # Se hoje é quinta (27), weekday=3. 8+3=11. 27-11=16 (Domingo da semana anterior).
    # Queremos a Segunda (17) até Domingo (23).
    
    ultimo_domingo_base = hoje - timedelta(days=hoje.weekday() + 8 + 7*semanas_atras)
    
    data_inicio = ultimo_domingo_base + timedelta(days=1) # Segunda-feira
    data_fim = ultimo_domingo_base + timedelta(days=7)    # Domingo seguinte
    
    return data_inicio, data_fim

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

def baixar_arquivo():
    session = criar_sessao()
    
    for semanas_atras in range(0, 4):  # Tenta as 4 últimas semanas para garantir
        data_inicio, data_fim = gerar_dados_semana(semanas_atras)
        
        # Formatos
        # URL: resumo_semanal_lpc-DDMMYYYY-a-DDMMYYYY.xlsx
        fmt_url = "%d%m%Y"
        # Cache/ISO: YYYY-MM-DD
        fmt_iso = "%Y-%m-%d"
        
        str_inicio_url = data_inicio.strftime(fmt_url)
        str_fim_url = data_fim.strftime(fmt_url)
        
        str_inicio_iso = data_inicio.strftime(fmt_iso)
        str_fim_iso = data_fim.strftime(fmt_iso)

        url = f"{BASE_URL}/{data_inicio.year}/resumo_semanal_lpc-{str_inicio_url}-a-{str_fim_url}.xlsx"
        
        nome_arquivo = f"resumo_semanal_lpc-{str_inicio_url}-a-{str_fim_url}.xlsx"
        caminho_arquivo = os.path.join(OUTPUT_DIR, nome_arquivo)
        
        cache_key = f"arquivo_precos:{str_inicio_iso}:{str_fim_iso}"
        
        # Verifica Cache
        if redis_client:
            cached_path = redis_client.get(cache_key)
            if cached_path and os.path.exists(cached_path):
                print(f"📌 [Cache] Usando arquivo em cache: {cached_path}")
                return url, str_inicio_iso, str_fim_iso, cached_path
        else:
            # Se sem redis, verifica se arquivo existe localmente
            if os.path.exists(caminho_arquivo):
                 print(f"📂 [Local] Arquivo já existe no disco: {caminho_arquivo}")
                 return url, str_inicio_iso, str_fim_iso, caminho_arquivo

        print(f"🌍 [Download] Tentando: {url}")
        
        try:
            # Tenta com verificação SSL
            try:
                response = session.get(url, timeout=15, verify=True)
            except requests.exceptions.SSLError:
                print(f"⚠️ [SSL] Falha na verificação de certificado para {url}. Tentando sem verificação...")
                response = session.get(url, timeout=15, verify=False)

            if response.status_code == 200:
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                with open(caminho_arquivo, "wb") as f:
                    f.write(response.content)
                
                if redis_client:
                    cache_ttl = calcular_tempo_ate_proximo_domingo()
                    redis_client.setex(cache_key, cache_ttl, caminho_arquivo)
                    print(f"✅ [Sucesso] Arquivo baixado e cacheado: {caminho_arquivo}")
                else:
                    print(f"✅ [Sucesso] Arquivo baixado: {caminho_arquivo}")
                
                return url, str_inicio_iso, str_fim_iso, caminho_arquivo
            else:
                print(f"❌ [Erro] Falha ao baixar (Status {response.status_code})")
                
        except requests.RequestException as e:
            print(f"❌ [Exceção] Erro na requisição: {e}")

    print("🚨 [Falha] Não foi possível baixar arquivos das últimas semanas.")
    return None, None, None, None
