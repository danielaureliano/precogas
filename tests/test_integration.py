import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import pandas as pd
from app.main import app
from app.core.config import settings

client = TestClient(app)


# Fixture para criar um arquivo Excel de teste temporário
@pytest.fixture
def mock_anp_excel(tmp_path):
    # Dados simulados válidos
    data = {
        "ESTADOS": ["DISTRITO FEDERAL", "SAO PAULO"],
        "PRODUTO": ["GASOLINA COMUM", "ETANOL"],
        "DATA INICIAL": ["2025-01-01", "2025-01-01"],
        "DATA FINAL": ["2025-01-07", "2025-01-07"],
        "PREÇO MÉDIO REVENDA": [5.50, 3.40],
    }
    df = pd.DataFrame(data)

    # Criar diretório temporário
    d = tmp_path / "dados_anp"
    d.mkdir()
    file_path = d / "resumo_teste.xlsx"

    # Salvar como Excel com o nome da aba correto
    df.to_excel(file_path, index=False, sheet_name="ESTADOS")
    return file_path


@patch("app.services.downloader.requests.Session")
@patch("app.services.downloader.redis_client")
def test_fluxo_integrado_download_extracao(mock_redis, mock_session, mock_anp_excel):
    """
    Teste de Integração (Component):
    Simula o fluxo completo API -> Downloader -> Extractor -> API.

    Verifica se o arquivo baixado é corretamente processado e transformado no JSON final.
    """
    # 1. Mock do Scraper para retornar uma URL fictícia e evitar chamada real à página da ANP
    with patch("app.services.downloader.encontrar_url_mais_recente") as mock_find_url:
        mock_find_url.return_value = "http://anp.gov.br/resumo_semanal_teste.xlsx"

        # 2. Mock da Resposta do Download do Excel
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"  # Fallback para o scraper se chamado
        with open(mock_anp_excel, "rb") as f:
            mock_response.content = f.read()

        # Configura a sessão mockada para retornar nossa resposta fake
        mock_session.return_value.get.return_value = mock_response

        # 3. Configurações de ETL temporárias para o teste (header na linha 0)
        mock_config = {
            "anp": {
                "sheet_name": "ESTADOS",
                "header_row": 0,
                "filters": {
                    "estado_col": "ESTADOS",
                    "produto_col": "PRODUTO",
                    "estado_val": "DISTRITO FEDERAL",
                    "produto_val": "GASOLINA COMUM",
                },
                "output_columns": {
                    "data_inicial": "DATA INICIAL",
                    "data_final": "DATA FINAL",
                    "preco_medio": "PREÇO MÉDIO REVENDA",
                },
            }
        }

        # 4. Execução do teste sobrescrevendo diretórios e configurações
        with patch.object(settings, "OUTPUT_DIR", mock_anp_excel.parent):
            with patch("app.services.extractor.ETL_CONFIG", mock_config):
                response = client.get("/precos")

                assert response.status_code == 200
                data = response.json()

                # Verificações de integridade dos dados retornados pela API
                assert data["precoMedioRevenda"] == 5.50
                # Validar timestamps (2025-01-01 00:00 BRT -> 1735700400000 UTC)
                assert data["dataInicial"] == 1735700400000
                assert data["dataFinal"] == 1736218800000
