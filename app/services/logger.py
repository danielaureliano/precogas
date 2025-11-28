import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger padronizado.
    Formato: DATA HORA - NOME_DO_MODULO - NIVEL - MENSAGEM
    """
    logger = logging.getLogger(name)

    # Evita adicionar múltiplos handlers se o logger já estiver configurado
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
