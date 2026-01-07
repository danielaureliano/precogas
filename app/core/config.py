from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Redis
    REDIS_URL: str = "redis://127.0.0.1:6379"

    # ANP
    ANP_BASE_URL: str = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc"
    OUTPUT_DIR: Path = Path("./dados_anp/")

    # ETL Config
    ETL_CONFIG_PATH: Path = Path("config/etl_rules.yaml")

    # Credenciais e Integrações
    GH_TOKEN: str | None = None
    GEMINI_API_KEY: str | None = None
    RENDER_DEPLOY_HOOK_URL: str | None = None

    # Segurança da Aplicação
    REDIS_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
