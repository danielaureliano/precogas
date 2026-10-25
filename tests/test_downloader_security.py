from unittest.mock import MagicMock
from app.services.downloader import encontrar_url_mais_recente

from unittest.mock import patch, MagicMock
from app.services.downloader import encontrar_url_mais_recente, baixar_arquivo

@patch("app.services.downloader.redis_client", None)
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

@patch("app.services.downloader.redis_client", None)
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

@patch("app.services.downloader.redis_client", None)
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

@patch("app.services.downloader.redis_client", None)
@patch("app.services.downloader.encontrar_url_mais_recente")
@patch("app.services.downloader.OUTPUT_DIR")
def test_path_traversal_malicious_url(mock_output_dir, mock_encontrar):
    """
    SECURITY TEST: Check if the downloader rejects a URL containing a path traversal payload.
    """
    # Simulate a malicious URL with path traversal
    mock_encontrar.return_value = "https://www.gov.br/anp/pt-br/assuntos/precos/../../../etc/passwd.xlsx"

    # When output_dir / "passwd.xlsx" is evaluated, we want to mock it.
    mock_file_path = MagicMock()
    # If the logic in downloader properly uses os.path.basename, it will extract "passwd.xlsx"
    # But if it tries to resolve, we just need to ensure the relative check fails
    # Let's mock the resolve().is_relative_to() to return False as it would for a traversal attempt
    mock_file_path.resolve.return_value.is_relative_to.return_value = False

    # We also mock the concatenation OUTPUT_DIR / ...
    mock_output_dir.__truediv__.return_value = mock_file_path
    mock_output_dir.resolve.return_value = MagicMock()

    url, data_ini, data_fim, caminho = baixar_arquivo()

    # The function should detect the invalid path and return None for all values
    assert url is None
    assert caminho is None
