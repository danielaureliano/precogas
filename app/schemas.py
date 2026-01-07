from pydantic import BaseModel, Field, ConfigDict
from typing import Dict


class PrecoGasolinaResponse(BaseModel):
    data_inicial: int = Field(
        ...,
        alias="dataInicial",
        description="Data de início da semana de referência. Formato: UNIX Timestamp em milissegundos (UTC). Origem: Data baseada em America/Sao_Paulo (BRT) convertida para UTC.",
        json_schema_extra={"example": 1766890800000},
    )
    data_final: int = Field(
        ...,
        alias="dataFinal",
        description="Data de fim da semana de referência. Formato: UNIX Timestamp em milissegundos (UTC). Origem: Data baseada em America/Sao_Paulo (BRT) convertida para UTC.",
        json_schema_extra={"example": 1767409200000},
    )
    preco_medio_revenda: float = Field(
        ...,
        alias="precoMedioRevenda",
        description="Preço médio de revenda no Distrito Federal (R$)",
        json_schema_extra={"example": 5.89},
    )

    model_config = ConfigDict(populate_by_name=True)


class HealthCheckResponse(BaseModel):
    status: str = Field(
        ...,
        description="Status geral da aplicação",
        json_schema_extra={"example": "UP"},
    )
    version: str = Field(
        ...,
        description="Versão atual da aplicação",
        json_schema_extra={"example": "1.12.3"},
    )
    checks: Dict[str, str] = Field(
        ...,
        description="Detalhes das verificações de dependências",
        json_schema_extra={
            "example": {
                "internet_connection": "OK",
                "redis_connection": "OK",
                "api_service": "OK",
            }
        },
    )


class ErrorResponse(BaseModel):
    erro: str = Field(
        ...,
        description="Descrição do erro ocorrido",
        json_schema_extra={"example": "Arquivo não encontrado no site da ANP"},
    )
