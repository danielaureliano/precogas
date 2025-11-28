import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.services.downloader import gerar_dados_semana, baixar_arquivo

def test_gerar_dados_semana():
    """
    Testa a lógica de cálculo de datas semanais (Segunda a Domingo).
    Mocka a data atual para garantir determinismo nos testes.
    """
    # Mock datetime.now() para uma data fixa: Quinta-feira, 27/11/2025
    with patch("app.services.downloader.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 11, 27)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        mock_datetime.strptime = datetime.strptime # Mantém strptime original

        # Semana 0 (atras):
        # Hoje: 27/11 (Qui) -> Semana anterior (base): Domingo 16/11
        # Intervalo esperado: 17/11 (Seg) a 23/11 (Dom)
        inicio, fim = gerar_dados_semana(0)
        assert inicio.strftime("%d%m%Y") == "17112025"
        assert fim.strftime("%d%m%Y") == "23112025"

        # Semana 1 (atras):
        # Intervalo esperado: 10/11 (Seg) a 16/11 (Dom)
        inicio, fim = gerar_dados_semana(1)
        assert inicio.strftime("%d%m%Y") == "10112025"
        assert fim.strftime("%d%m%Y") == "16112025"

@patch("app.services.downloader.requests.Session")
@patch("app.services.downloader.os.makedirs")
@patch("app.services.downloader.open")
@patch("app.services.downloader.os.path.exists")
@patch("app.services.downloader.redis_client")
def test_baixar_arquivo_sucesso(mock_redis, mock_exists, mock_open, mock_makedirs, mock_session):
    """
    Testa o fluxo completo de download com sucesso (HTTP 200).
    Verifica se o arquivo é salvo e se os diretórios são criados.
    Ignora cache e disco real.
    """
    # Garante que não acha nada no cache nem no disco, forçando o download
    mock_exists.return_value = False
    if mock_redis:
        mock_redis.get.return_value = None

    # Configura o Mock da Sessão
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"conteudo_falso_excel"
    
    session_instance = mock_session.return_value
    session_instance.get.return_value = mock_response

    # Executa
    url, data_inicio, data_fim, caminho = baixar_arquivo()

    # Verificações
    assert url is not None
    assert "resumo_semanal_lpc" in url
    assert caminho is not None
    
    # Garante que tentou criar o diretório
    mock_makedirs.assert_called()
    # Garante que tentou escrever o arquivo
    mock_open.assert_called()

@patch("app.services.downloader.requests.Session")
@patch("app.services.downloader.os.path.exists")
@patch("app.services.downloader.redis_client") # Mock do objeto redis global
def test_baixar_arquivo_falha_404(mock_redis, mock_exists, mock_session):
    """
    Testa o comportamento quando todas as tentativas de download retornam 404.
    Deve retornar None para todos os valores.
    """
    # Garante que não acha nada no cache nem no disco
    mock_exists.return_value = False
    if mock_redis:
        mock_redis.get.return_value = None

    # Simula erro 404 em todas as tentativas
    mock_response = MagicMock()
    mock_response.status_code = 404
    
    session_instance = mock_session.return_value
    session_instance.get.return_value = mock_response

    url, data_inicio, data_fim, caminho = baixar_arquivo()

    assert caminho is None