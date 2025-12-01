from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # ANP
    ANP_BASE_URL: str = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc"
    OUTPUT_DIR: Path = Path("./dados_anp/")

    # ETL Config
    ETL_CONFIG_PATH: Path = Path("config/etl_rules.yaml")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
