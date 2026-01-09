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
