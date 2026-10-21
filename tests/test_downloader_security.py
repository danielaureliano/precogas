from unittest.mock import MagicMock, patch
from app.services.downloader import encontrar_url_mais_recente, baixar_arquivo

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

@patch("app.services.downloader.encontrar_url_mais_recente")
@patch("app.services.downloader.criar_sessao")
def test_path_traversal_prevention(mock_criar_sessao, mock_encontrar_url):
    """
    SECURITY TEST: Prevent Path Traversal during file download.
    Checks if `baixar_arquivo` rejects a URL containing malicious path traversal sequences (`../`).
    """
    mock_session = MagicMock()
    mock_criar_sessao.return_value = mock_session

    # Simulate a malicious URL attempting to escape the intended output directory
    malicious_url = "https://www.gov.br/anp/pt-br/assuntos/precos/2025/..%2f..%2f..%2f..%2fetc%2fpasswd.xlsx"
    mock_encontrar_url.return_value = malicious_url

    url, data_inicio, data_fim, caminho = baixar_arquivo()

    # Assert that the function detected the path traversal and aborted
    assert url is None
    assert data_inicio is None
    assert data_fim is None
    assert caminho is None
