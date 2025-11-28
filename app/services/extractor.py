import pandas as pd
from app.services.logger import setup_logger

logger = setup_logger(__name__)

def extrair_dados(caminho_arquivo):
    try:
        excel_data = pd.ExcelFile(caminho_arquivo)

        if "ESTADOS" not in excel_data.sheet_names:
            logger.error("A aba 'ESTADOS' não foi encontrada na planilha.")
            return None

        # Ajuste: Ignorar as 9 primeiras linhas e definir a linha 10 como cabeçalho
        df_estados = excel_data.parse("ESTADOS", skiprows=9)  # <-- Pula as 9 primeiras linhas


        # Ajuste para garantir que os nomes das colunas estejam corretos
        df_estados.rename(columns=lambda x: str(x).strip(), inplace=True)

        # Filtrar pelo Estado e Produto
        df_filtrado = df_estados[
            (df_estados["ESTADOS"].str.upper() == "DISTRITO FEDERAL") &
            (df_estados["PRODUTO"].str.upper() == "GASOLINA COMUM")
        ]

        if df_filtrado.empty:
            logger.warning("Nenhum dado encontrado para GASOLINA COMUM no DISTRITO FEDERAL.")
            return None

        # 🔹 Mapeando os nomes das chaves para o novo formato
        dados = df_filtrado.iloc[0][["DATA INICIAL", "DATA FINAL", "PREÇO MÉDIO REVENDA"]].to_dict()
        dados_formatados = {
            "dataInicial": dados["DATA INICIAL"],
            "dataFinal": dados["DATA FINAL"],
            "precoMedioRevenda": dados["PREÇO MÉDIO REVENDA"]
        }

        return dados_formatados

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo: {e}")
    return None
