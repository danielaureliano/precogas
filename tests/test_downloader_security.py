from unittest.mock import MagicMock
from app.services.downloader import encontrar_url_mais_recente

def test_ssrf_malicious_domain():
    """
    SECURITY TEST: Reproduce SSRF/Malicious Download vulnerability.
    Checks if the scraper rejects a URL from a malicious domain.
    """
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200

    # Simulate a compromised ANP page or a page with an external link
    malicious_url = "http://attacker.com/malicious_resumo_semanal.xlsx"
    mock_response.text = f"""
    <html>
        <body>
            <a href="{malicious_url}">Planilha Semanal (Hacked)</a>
        </body>
    </html>
    """
    mock_session.get.return_value = mock_response

    # Call the function
    url = encontrar_url_mais_recente(mock_session)

    # NOW: This should return None because attacker.com != gov.br
    assert url is None

def test_ssrf_bypass_domain():
    """
    SECURITY TEST: Check if the scraper rejects a URL with a bypass domain.
    Specifically checks for attacker-gov.br which bypasses `.endswith("gov.br")` check.
    """
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200

    malicious_url = "http://attacker-gov.br/malicious_resumo_semanal.xlsx"
    mock_response.text = f"""
    <html>
        <body>
            <a href="{malicious_url}">Planilha Semanal (Hacked)</a>
        </body>
    </html>
    """
    mock_session.get.return_value = mock_response

    url = encontrar_url_mais_recente(mock_session)

    # Should return None because attacker-gov.br is not gov.br or a subdomain of gov.br
    assert url is None

def test_valid_gov_br_domain():
    """
    Ensure valid gov.br URLs are still accepted.
    """
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200

    valid_url = "https://www.gov.br/anp/pt-br/assuntos/precos/2025/resumo_semanal_lpc-5.xlsx"
    mock_response.text = f"""
    <html>
        <body>
            <a href="{valid_url}">Planilha Semanal</a>
        </body>
    </html>
    """
    mock_session.get.return_value = mock_response

    # Call the function
    url = encontrar_url_mais_recente(mock_session)

    # This should return the valid URL
    assert url == valid_url

from unittest.mock import patch
from app.services.downloader import baixar_arquivo

@patch("app.services.downloader.encontrar_url_mais_recente")
@patch("app.services.downloader.requests.Session")
@patch("app.services.downloader.redis_client")
def test_path_traversal_prevention(mock_redis, mock_session, mock_encontrar_url, tmp_path):
    """
    Verifica se a tentativa de Path Traversal no nome do arquivo baixado é mitigada.
    """
    malicious_url = "https://www.gov.br/anp/pt-br/assuntos/precos/2025/..%2f..%2f..%2f..%2fetc%2fpasswd"
    mock_encontrar_url.return_value = malicious_url

    mock_output_dir = tmp_path / "dados_anp"
    mock_output_dir.mkdir()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake data"
    mock_session.return_value.get.return_value = mock_response

    with patch("app.services.downloader.OUTPUT_DIR", mock_output_dir):
        url, data_inicio, data_fim, caminho = baixar_arquivo()

        assert caminho is not None
        assert caminho.name == "passwd"
        assert str(caminho.parent) == str(mock_output_dir.resolve())
