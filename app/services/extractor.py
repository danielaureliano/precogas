import pandas as pd

def extrair_dados(caminho_arquivo):
    try:
        excel_data = pd.ExcelFile(caminho_arquivo)
        if "ESTADOS" not in excel_data.sheet_names:
            print("A aba 'ESTADOS' não foi encontrada na planilha.")
            return None
        
        df_estados = excel_data.parse("ESTADOS")
        df_filtrado = df_estados[
            (df_estados["ESTADO"].str.upper() == "DISTRITO FEDERAL") &
            (df_estados["PRODUTO"].str.upper() == "GASOLINA COMUM")
        ]
        
        if df_filtrado.empty:
            return None
        
        return df_filtrado[["DATA INICIAL", "DATA FINAL", "PREÇO MÉDIO REVENDA"]].iloc[0].to_dict()
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
    return None
