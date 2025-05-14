from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application metadata
    app_name: str = "DigiPocket Online Transaction System"
    version: str = "1.0.0"

    # MongoDB settings (hardcoded)
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "digital_wallet"

    # JWT configuration (hardcoded)
    jwt_secret_key: str = "AVeryLongSecretKeyForTheSecurityOfData"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_minutes: int = 30

    # Daily limits per user tier
    basic_daily_limit: float = 5_000.0
    premium_daily_limit: float = 50_000.0

    # Log file configuration
    log_file: str = "./core/logs/digital_wallet.log"

settings = Settings()
