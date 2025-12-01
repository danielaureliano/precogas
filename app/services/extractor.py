import pandas as pd
import yaml
from pathlib import Path
from app.services.logger import setup_logger

logger = setup_logger(__name__)

# Carregar configurações de ETL
CONFIG_PATH = Path("config/etl_rules.yaml")
ETL_CONFIG = {}

try:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            ETL_CONFIG = yaml.safe_load(f)
        logger.info(f"Configurações de ETL carregadas de {CONFIG_PATH}")
    else:
        logger.warning(f"Arquivo de configuração {CONFIG_PATH} não encontrado. Usando defaults seria arriscado, a extração pode falhar.")
except Exception as e:
    logger.error(f"Erro crítico ao carregar configuração ETL: {e}")

def extrair_dados(caminho_arquivo: str | Path):
    if not ETL_CONFIG:
        logger.error("Configuração ETL inválida ou não carregada.")
        return None

    anp_conf = ETL_CONFIG.get("anp", {})

    try:
        excel_data = pd.ExcelFile(caminho_arquivo)
        sheet = anp_conf.get("sheet_name", "ESTADOS")

        if sheet not in excel_data.sheet_names:
            logger.error(f"A aba '{sheet}' não foi encontrada na planilha.")
            return None

        # Ajuste: Ignorar as 9 primeiras linhas e definir a linha 10 como cabeçalho
        header_row = anp_conf.get("header_row", 9)
        df_estados = excel_data.parse(sheet, skiprows=header_row)

        # Ajuste para garantir que os nomes das colunas estejam corretos
        df_estados.rename(columns=lambda x: str(x).strip(), inplace=True)

        # Filtrar pelo Estado e Produto
        filters = anp_conf.get("filters", {})
        est_col = filters.get("estado_col", "ESTADOS")
        est_val = filters.get("estado_val", "DISTRITO FEDERAL")
        prod_col = filters.get("produto_col", "PRODUTO")
        prod_val = filters.get("produto_val", "GASOLINA COMUM")

        df_filtrado = df_estados[
            (df_estados[est_col].str.upper() == est_val) &
            (df_estados[prod_col].str.upper() == prod_val)
        ]

        if df_filtrado.empty:
            logger.warning(f"Nenhum dado encontrado para {prod_val} no {est_val}.")
            return None

        # 🔹 Mapeando os nomes das chaves para o novo formato
        cols = anp_conf.get("output_columns", {})
        col_ini = cols.get("data_inicial", "DATA INICIAL")
        col_fim = cols.get("data_final", "DATA FINAL")
        col_preco = cols.get("preco_medio", "PREÇO MÉDIO REVENDA")

        dados = df_filtrado.iloc[0][[col_ini, col_fim, col_preco]].to_dict()
        dados_formatados = {
            "dataInicial": dados[col_ini],
            "dataFinal": dados[col_fim],
            "precoMedioRevenda": dados[col_preco]
        }

        return dados_formatados

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo: {e}")
    return None
