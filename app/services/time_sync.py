import ntplib
from datetime import datetime, timezone
import socket
from app.services.logger import setup_logger

logger = setup_logger(__name__)

def get_current_time(server: str = "pool.ntp.org") -> datetime:
    """
    Obtém a hora atual de um servidor NTP.
    Em caso de falha, retorna a hora local do sistema com log de aviso.
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
