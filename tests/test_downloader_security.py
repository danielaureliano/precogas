from unittest.mock import MagicMock, patch
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

@patch("app.services.downloader.encontrar_url_mais_recente")
@patch("app.services.downloader.criar_sessao")
@patch("app.services.downloader.redis_client", None)
def test_path_traversal_prevention(mock_criar_sessao, mock_encontrar_url):
    """
    SECURITY TEST: Check if the downloader prevents path traversal vulnerabilities.
    Simulates finding a URL that attempts to escape the output directory.
    """
    from unittest.mock import MagicMock
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake content"
    mock_session.get.return_value = mock_response
    mock_criar_sessao.return_value = mock_session

    # URL with encoded path traversal attempting to overwrite an important file
    # and a query string to simulate a complex URL
    malicious_url = "https://www.gov.br/anp/pt-br/%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd?query=1"
    mock_encontrar_url.return_value = malicious_url

    # Run the function
    url, data_inicio, data_fim, caminho_arquivo = baixar_arquivo()

    # Because of the fix, `os.path.basename` will extract just "passwd",
    # and `resolve()` will resolve it against `OUTPUT_DIR`.
    # It will never reach `/etc/passwd`.
    # It will also successfully download the mock content to `OUTPUT_DIR/passwd`.
    assert url == malicious_url
    assert data_inicio is None
    assert data_fim is None
    assert caminho_arquivo is not None
    assert caminho_arquivo.name == "passwd"
    assert "etc" not in str(caminho_arquivo)

    # Verify that the session get was called (which would be blocked or throw an error if the traversal actually occurred and failed the relative path check)
    mock_session.get.assert_called_with(malicious_url, timeout=15, verify=True)
