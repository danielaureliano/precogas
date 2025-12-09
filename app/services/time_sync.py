import ntplib
from datetime import datetime, timezone
import socket
from app.services.logger import setup_logger

logger = setup_logger(__name__)

def get_current_time(server: str = "pool.ntp.org") -> datetime:
    """
    Obtém a hora atual precisa a partir de um servidor NTP.

    Tenta conectar ao servidor NTP especificado para obter o timestamp.
    Em caso de falha (timeout, erro de rede), realiza fallback para o relógio local do sistema.

    Args:
        server (str): Endereço do servidor NTP (padrão: "pool.ntp.org").

    Returns:
        datetime: Objeto datetime representando a hora atual (local naive).
    """
    try:
        client = ntplib.NTPClient()
        # Timeout de 5 segundos para não travar a aplicação
        response = client.request(server, version=3, timeout=5)

        # Converte timestamp NTP para datetime com timezone UTC
        ntp_time = datetime.fromtimestamp(response.tx_time, timezone.utc)

        # Converte para local time (naive) se necessário, ou mantém offset-aware
        # Para compatibilidade com datetime.now(), vamos retornar local naive por enquanto,
        # mas idealmente deveríamos usar UTC em todo o sistema.
        # O projeto usa datetime.now() que é naive system time.
        # Vamos converter para local naive para manter consistência.
        local_time = ntp_time.astimezone().replace(tzinfo=None)

        return local_time

    except (ntplib.NTPException, socket.gaierror, socket.timeout, Exception) as e:
        logger.warning(f"Falha ao obter hora via NTP ({server}): {e}. Usando relógio local.")
        return datetime.now()
