import pandas as pd
import yaml
from pathlib import Path
from app.services.logger import setup_logger
from app.core.config import settings

logger = setup_logger(__name__)

# Carregar configurações de ETL
CONFIG_PATH = settings.ETL_CONFIG_PATH
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
        excel_data = pd.ExcelFile(caminho_arquivo, engine="openpyxl")
        sheet = anp_conf.get("sheet_name", "ESTADOS")

        if sheet not in excel_data.sheet_names:
            logger.error(f"Schema Error: A aba '{sheet}' não foi encontrada na planilha. Abas disponíveis: {excel_data.sheet_names}")
            return None

        # Ajuste: Ignorar as 9 primeiras linhas e definir a linha 10 como cabeçalho
        header_row = anp_conf.get("header_row", 9)

        # Validação básica do header_row
        if not isinstance(header_row, int) or header_row < 0:
             logger.error(f"Schema Error: 'header_row' inválido: {header_row}")
             return None

        df_estados = excel_data.parse(sheet, skiprows=header_row)

        # Ajuste para garantir que os nomes das colunas estejam corretos
        df_estados.rename(columns=lambda x: str(x).strip(), inplace=True)

        # Configurações de colunas
        filters = anp_conf.get("filters", {})
        est_col = filters.get("estado_col", "ESTADOS")
        prod_col = filters.get("produto_col", "PRODUTO")

        cols = anp_conf.get("output_columns", {})
        col_ini = cols.get("data_inicial", "DATA INICIAL")
        col_fim = cols.get("data_final", "DATA FINAL")
        col_preco = cols.get("preco_medio", "PREÇO MÉDIO REVENDA")

        # Validação de Schema: Verificar se colunas existem
        required_cols = {est_col, prod_col, col_ini, col_fim, col_preco}
        missing_cols = required_cols - set(df_estados.columns)
        if missing_cols:
            logger.error(f"Schema Error: Colunas obrigatórias ausentes na planilha: {missing_cols}")
            return None

        est_val = filters.get("estado_val", "DISTRITO FEDERAL")
        prod_val = filters.get("produto_val", "GASOLINA COMUM")

        df_filtrado = df_estados[
            (df_estados[est_col].astype(str).str.upper() == est_val) &
            (df_estados[prod_col].astype(str).str.upper() == prod_val)
        ]

        if df_filtrado.empty:
            logger.warning(f"Data Integrity: Nenhum dado encontrado para {prod_val} no {est_val}.")
            return None

        # Extração e validação de tipos
        row = df_filtrado.iloc[0]

        try:
            # Tentar converter preço para float, tratando vírgula se necessário (padrão PT-BR)
            preco_raw = row[col_preco]
            if isinstance(preco_raw, str):
                preco_raw = preco_raw.replace(',', '.')
            preco_float = float(preco_raw)
        except (ValueError, TypeError):
            logger.error(f"Data Integrity: Valor inválido para preço médio: {row[col_preco]}")
            return None

        dados_formatados = {
            "dataInicial": row[col_ini],
            "dataFinal": row[col_fim],
            "precoMedioRevenda": preco_float
        }

        return dados_formatados

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo: {e}")
    return None
