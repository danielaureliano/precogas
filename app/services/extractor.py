import pandas as pd

def extrair_dados(caminho_arquivo):
    try:
        excel_data = pd.ExcelFile(caminho_arquivo)

        if "ESTADOS" not in excel_data.sheet_names:
            print("A aba 'ESTADOS' não foi encontrada na planilha.")
            return None

        # Ajuste: Ignorar as 9 primeiras linhas e definir a linha 10 como cabeçalho
        df_estados = excel_data.parse("ESTADOS", skiprows=9)  # <-- Pula as 9 primeiras linhas
        
        # Debug: Mostrar todas as colunas disponíveis
        print("Colunas encontradas na aba 'ESTADOS':", df_estados.columns.tolist())

        # Ajuste para garantir que os nomes das colunas estejam corretos
        df_estados.rename(columns=lambda x: str(x).strip(), inplace=True)

        # Filtrar pelo Estado e Produto
        df_filtrado = df_estados[
            (df_estados["ESTADOS"].str.upper() == "DISTRITO FEDERAL") &
            (df_estados["PRODUTO"].str.upper() == "GASOLINA COMUM")
        ]

        if df_filtrado.empty:
            print("Nenhum dado encontrado para GASOLINA COMUM no DISTRITO FEDERAL.")
            return None

        return df_filtrado[["DATA INICIAL", "DATA FINAL", "PREÇO MÉDIO REVENDA"]].iloc[0].to_dict()

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
    return None
