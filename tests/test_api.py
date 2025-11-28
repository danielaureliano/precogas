from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from fastapi import status # Importar status

client = TestClient(app)

@patch("app.main.baixar_arquivo")
@patch("app.main.extrair_dados")
def test_obter_precos_sucesso(mock_extrair, mock_baixar):
    """
    Testa o endpoint /precos com sucesso.
    Verifica se a API retorna o JSON formatado corretamente quando
    os serviços de download e extração funcionam.
    """
    # Configura mocks
    mock_baixar.return_value = (
        "http://fake.url/file.xlsx",
        "2025-01-01",
        "2025-01-07",
        "./dados_anp/file.xlsx"
    )

    mock_extrair.return_value = {
        "dataInicial": "01/01/2025",
        "dataFinal": "07/01/2025",
        "precoMedioRevenda": 5.99
    }

    response = client.get("/precos")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["precoMedioRevenda"] == 5.99
    assert data["dataInicial"] == "01/01/2025"

@patch("app.main.baixar_arquivo")
def test_obter_precos_falha_download(mock_baixar):
    """
    Testa o comportamento da API quando o download falha.
    Deve retornar um JSON com chave 'erro' e status 503.
    """
    # Simula falha no download (retorna None no caminho)
    mock_baixar.return_value = (None, None, None, None)

    response = client.get("/precos")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE # A API agora retorna 503
    assert "erro" in response.json()
    assert response.json()["erro"] == "Arquivo não encontrado no site da ANP"

def test_metrics_endpoint():
    """
    Testa o endpoint /metrics.
    Verifica se retorna 200 OK e se o conteúdo é texto puro com métricas Prometheus.
    """
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "charset=utf-8" in response.headers["content-type"]
    assert "# HELP http_requests_total Total HTTP Requests" in response.text
    assert "# TYPE http_requests_total counter" in response.text
    assert "# HELP http_response_time_seconds HTTP Response Time" in response.text
    assert "# TYPE http_response_time_seconds histogram" in response.text
