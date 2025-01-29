import os
import requests
from datetime import datetime, timedelta

BASE_URL = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc"
OUTPUT_DIR = "./dados_anp/"

def gerar_url_data():
    hoje = datetime.now()
    inicio_ultima_semana = hoje - timedelta(days=hoje.weekday() + 7)
    fim_ultima_semana = inicio_ultima_semana + timedelta(days=6)

    data_inicio = inicio_ultima_semana.strftime("%Y-%m-%d")
    data_fim = fim_ultima_semana.strftime("%Y-%m-%d")

    url = f"{BASE_URL}/{inicio_ultima_semana.year}/resumo_semanal_lpc_{data_inicio}_{data_fim}.xlsx"
    return url, data_inicio, data_fim

def baixar_arquivo():
    url, data_inicio, data_fim = gerar_url_data()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            caminho_arquivo = os.path.join(OUTPUT_DIR, f"resumo_semanal_{data_inicio}_{data_fim}.xlsx")
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)
            return url, data_inicio, data_fim, caminho_arquivo
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
    return url, data_inicio, data_fim, None
