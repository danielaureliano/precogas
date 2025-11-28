import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.services.extractor import extrair_dados

# Mock do objeto ExcelFile e do DataFrame
@patch("pandas.ExcelFile")
def test_extrair_dados_sucesso(mock_excel_file):
    """
    Testa a extração bem-sucedida de dados quando o arquivo Excel é válido
    e contém os dados esperados (DF, Gasolina Comum).
    """
    # Mock da leitura do Excel
    mock_instance = mock_excel_file.return_value
    mock_instance.sheet_names = ["ESTADOS"]
    
    # Mock do DataFrame retornado pelo parse
    data = {
        "ESTADOS": ["DISTRITO FEDERAL", "SAO PAULO"],
        "PRODUTO": ["GASOLINA COMUM", "ETANOL"],
        "DATA INICIAL": ["2025-01-01", "2025-01-01"],
        "DATA FINAL": ["2025-01-07", "2025-01-07"],
        "PREÇO MÉDIO REVENDA": [5.50, 3.40]
    }
    df = pd.DataFrame(data)
    mock_instance.parse.return_value = df

    resultado = extrair_dados("caminho/fake.xlsx")

    assert resultado is not None
    assert resultado["precoMedioRevenda"] == 5.50
    assert resultado["dataInicial"] == "2025-01-01"

@patch("pandas.ExcelFile")
def test_extrair_dados_aba_inexistente(mock_excel_file):
    """
    Testa a falha quando a aba 'ESTADOS' não existe na planilha.
    """
    mock_instance = mock_excel_file.return_value
    mock_instance.sheet_names = ["OUTRA_ABA"] # Não tem ESTADOS

    resultado = extrair_dados("caminho/fake.xlsx")
    assert resultado is None

@patch("pandas.ExcelFile")
def test_extrair_dados_produto_nao_encontrado(mock_excel_file):
    """
    Testa o caso onde a aba existe, mas não há dados para o filtro
    específico (DF + Gasolina Comum).
    """
    mock_instance = mock_excel_file.return_value
    mock_instance.sheet_names = ["ESTADOS"]
    
    data = {
        "ESTADOS": ["SAO PAULO"], # Sem DF
        "PRODUTO": ["GASOLINA COMUM"],
        "DATA INICIAL": ["2025-01-01"],
        "DATA FINAL": ["2025-01-07"],
        "PREÇO MÉDIO REVENDA": [5.50]
    }
    df = pd.DataFrame(data)
    mock_instance.parse.return_value = df

    resultado = extrair_dados("caminho/fake.xlsx")
    assert resultado is None

def test_extrair_dados_arquivo_invalido():
    """
    Testa a resiliência quando o arquivo não existe ou está corrompido
    (Pandas levanta exceção).
    """
    # Sem mock, passando um caminho que não existe, o pandas deve lançar erro
    # A função captura Exception e retorna None
    resultado = extrair_dados("caminho/nao_existe.xlsx")
    assert resultado is None