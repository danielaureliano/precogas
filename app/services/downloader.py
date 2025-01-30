import os
import redis  # Adicionando a importação do Redis
import requests
from datetime import datetime, timedelta

# Conexão com Redis (container rodando no Docker)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

BASE_URL = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc"
OUTPUT_DIR = "./dados_anp/"

def calcular_tempo_ate_proximo_domingo():
    """Calcula quantos segundos faltam até o próximo domingo à meia-noite."""
    hoje = datetime.now()
    proximo_domingo = hoje + timedelta(days=7 - hoje.weekday())
    proximo_domingo = proximo_domingo.replace(hour=0, minute=0, second=0, microsecond=0)
    return int((proximo_domingo - hoje).total_seconds())

def gerar_url_data():
    hoje = datetime.now()

    # Encontrar o domingo da semana passada
    ultimo_domingo = hoje - timedelta(days=hoje.weekday() + 8)  # Retrocede para o domingo anterior
    ultimo_sabado = ultimo_domingo + timedelta(days=6)  # Adiciona 6 dias para chegar no sábado

    # Formatar as datas no padrão esperado
    data_inicio = ultimo_domingo.strftime("%Y-%m-%d")
    data_fim = ultimo_sabado.strftime("%Y-%m-%d")

    # Criar a URL correta
    url = f"{BASE_URL}/{ultimo_domingo.year}/resumo_semanal_lpc_{data_inicio}_{data_fim}.xlsx"
    
    print(f"URL gerada: {url}")  # Debug: Verificar a URL no terminal
    return url, data_inicio, data_fim

def baixar_arquivo():
    url, data_inicio, data_fim = gerar_url_data()
    print(f"Baixando: {url}")  # <-- Debug
    nome_arquivo = f"resumo_semanal_{data_inicio}_{data_fim}.xlsx"
    caminho_arquivo = os.path.join(OUTPUT_DIR, nome_arquivo)
    
    # 🔹 Verifica no Redis se o arquivo já foi baixado recentemente
    cache_key = f"arquivo_precos:{data_inicio}_{data_fim}"
    cached_path = redis_client.get(cache_key)
    
    if cached_path and os.path.exists(cached_path):
        print(f"📌 Usando cache do Redis até domingo: {cached_path}")
        return url, data_inicio, data_fim, cached_path
    
    print(f"🔽 Baixando novo arquivo: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)

            # 🔹 Armazena o caminho do arquivo no Redis até o próximo domingo
            cache_ttl = calcular_tempo_ate_proximo_domingo()
            redis_client.setex(cache_key, cache_ttl, caminho_arquivo)
            print(f"✅ Arquivo salvo e armazenado no Redis até domingo: {caminho_arquivo}")
            return url, data_inicio, data_fim, caminho_arquivo
        else:
            print(f"❌ Erro ao baixar: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Erro na requisição: {e}")

    return url, data_inicio, data_fim, None  # Corrigido o return dentro da função
