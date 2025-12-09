from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from app.services.downloader import baixar_arquivo

@patch("app.services.downloader.get_current_time")
@patch("app.services.downloader.requests.Session")
@patch("app.services.downloader.OUTPUT_DIR") # Mocka a variável global OUTPUT_DIR diretamente
@patch("app.services.downloader.redis_client")
def test_baixar_arquivo_sucesso(mock_redis, mock_output_dir, mock_session, mock_get_time):
    """
    Testa o fluxo completo de download com sucesso (HTTP 200).
    Verifica se o arquivo é salvo usando pathlib e se a lógica de scraping é chamada.
    """
    # Mock do tempo
    mock_get_time.return_value = datetime(2025, 12, 9, 12, 0, 0)

    # Quando fazemos OUTPUT_DIR / "nome", ele chama __truediv__
    mock_file_path = MagicMock()
    mock_output_dir.__truediv__.return_value = mock_file_path

    # Garante que não acha nada no cache nem no disco
    mock_file_path.exists.return_value = False

    if mock_redis:
        mock_redis.get.return_value = None

    # Configura o Mock da Sessão
    session_instance = mock_session.return_value

    # Precisamos simular duas chamadas ao session.get:
    # 1. A chamada ao scraper (retorna HTML com link)
    # 2. A chamada de download do arquivo (retorna binário)

    mock_response_html = MagicMock()
    mock_response_html.status_code = 200
    mock_response_html.text = """
    <html>
        <body>
            <a href="https://www.gov.br/anp/pt-br/assuntos/precos/2025/resumo_semanal_lpc-5.xlsx">Planilha Semanal</a>
        </body>
    </html>
    """

    mock_response_file = MagicMock()
    mock_response_file.status_code = 200
    mock_response_file.content = b"conteudo_falso_excel"

    # Define o side_effect para retornar sequencialmente
    session_instance.get.side_effect = [mock_response_html, mock_response_file]

    # Mock do open() chamado no objeto Path do arquivo
    m = mock_open()
    mock_file_path.open = m

    # Executa
    url, data_inicio, data_fim, caminho = baixar_arquivo()

    # Verificações
    assert url == "https://www.gov.br/anp/pt-br/assuntos/precos/2025/resumo_semanal_lpc-5.xlsx"
    # As datas agora são None porque vêm do extractor
    assert data_inicio is None
    assert data_fim is None
    assert caminho is not None

    # Garante que tentou criar o diretório no OUTPUT_DIR
    mock_output_dir.mkdir.assert_called()
    # Garante que tentou escrever o arquivo
    m.assert_called()
    m().write.assert_called_with(b"conteudo_falso_excel")

@patch("app.services.downloader.requests.Session")
@patch("app.services.downloader.OUTPUT_DIR")
@patch("app.services.downloader.redis_client")
def test_baixar_arquivo_falha_scraper(mock_redis, mock_output_dir, mock_session):
    """
    Testa o comportamento quando o scraper não encontra nenhum link válido.
    """
    mock_file_path = MagicMock()
    mock_output_dir.__truediv__.return_value = mock_file_path

    session_instance = mock_session.return_value

    # Retorna HTML sem links .xlsx
    mock_response_html = MagicMock()
    mock_response_html.status_code = 200
    mock_response_html.text = "<html><body>Nenhum link aqui</body></html>"

    session_instance.get.return_value = mock_response_html

    url, data_inicio, data_fim, caminho = baixar_arquivo()

    assert url is None
    assert caminho is None
