import logging
import sys
import structlog
import structlog.stdlib
import structlog.processors
import structlog.dev
import structlog.contextvars
import json

def configure_structlog():
    """
    Configura o structlog para output JSON estruturado.
    """
    # Processadores padrão que adicionam contexto
    shared_processors = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"), # Adiciona timestamp ISO
        structlog.processors.StackInfoRenderer(),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            ]
        ),
        structlog.contextvars.merge_contextvars, # Para trace_id
    ]

    # Configura o logger padrão do Python
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Configura os processadores do structlog
    if sys.stdout.isatty():
        # Renderização amigável para terminais interativos
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # JSON para ambiente de produção/CI
        processors = shared_processors + [
            structlog.processors.JSONRenderer(serializer=json.dumps),
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def setup_logger(name: str) -> structlog.BoundLogger:
    """
    Configura e retorna um logger baseado em structlog para o nome especificado.
    """
    return structlog.get_logger(name)

# Garante que a configuração seja executada apenas uma vez
configure_structlog()
