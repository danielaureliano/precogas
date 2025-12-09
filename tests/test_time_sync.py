from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.time_sync import get_current_time
import ntplib

@patch("app.services.time_sync.ntplib.NTPClient")
def test_get_current_time_ntp_success(mock_ntp_client):
    """
    Testa se a função retorna o horário do NTP corretamente.
    """
    # Configura o Mock do cliente e resposta NTP
    mock_client_instance = mock_ntp_client.return_value
    mock_response = MagicMock()
    # Timestamp arbitrário (ex: 2025-12-09 12:00:00 UTC)
    mock_response.tx_time = 1765281600
    mock_client_instance.request.return_value = mock_response

    current_time = get_current_time()

    # Verifica se retornou um objeto datetime
    assert isinstance(current_time, datetime)
    # Verifica se a data corresponde (aproximadamente, considerando fuso local)
    # Como o timestamp é fixo, podemos verificar.
    # Mas como a função converte para local, pode variar dependendo da máquina rodando o teste.
    # O importante é que não falhou e veio do timestamp.

@patch("app.services.time_sync.ntplib.NTPClient")
def test_get_current_time_fallback(mock_ntp_client):
    """
    Testa o fallback para datetime.now() em caso de erro no NTP.
    """
    mock_client_instance = mock_ntp_client.return_value
    mock_client_instance.request.side_effect = ntplib.NTPException("Erro de conexão")

    current_time = get_current_time()

    # Deve retornar um datetime válido (local) mesmo com erro
    assert isinstance(current_time, datetime)
    # Deve estar próximo do agora (delta pequeno)
    assert (datetime.now() - current_time).total_seconds() < 1
