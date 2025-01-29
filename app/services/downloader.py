import os
import requests
from datetime import datetime, timedelta

BASE_URL = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc"
OUTPUT_DIR = "./dados_anp/"

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

    try:
        response = requests.get(url, timeout=10)
        print(f"Status da resposta: {response.status_code}")  # <-- Debug
        
        if response.status_code == 200:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            caminho_arquivo = os.path.join(OUTPUT_DIR, f"resumo_semanal_{data_inicio}_{data_fim}.xlsx")
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)
            return url, data_inicio, data_fim, caminho_arquivo
        else:
            print(f"Erro ao baixar: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")

    return url, data_inicio, data_fim, None
