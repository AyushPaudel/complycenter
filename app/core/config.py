from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from yarl import URL
import pytz
from passlib.context import CryptContext


class Settings(BaseSettings):
    # Timezone (stored as a string and parsed when needed)
    TIMEZONE: str = "Asia/Kathmandu"
    POSTGRES_DB: str = "complycenter"
    POSTGRES_PASSWORD: str = "Password1234!"
    POSTGRES_USER: str = "postgres"
    POSTGRES_HOST: str = "complycenter-database"
    POSTGRES_PORT: int = 5432
    DB_ECHO: bool = False

    SECRET_KEY: SecretStr = SecretStr("default-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    LOG_LEVEL: str = "INFO"
    LOG_BACKUP_COUNT: int = 5

    REDIS_HOST: str = "complycenter-cache"
    REDIS_PORT: int = 6379
    PASSWORD_HASHING_ALGORITHM : str =  "sha256_crypt"

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )

    @property
    def timezone(self):
        return pytz.timezone(self.TIMEZONE)
    
    @property
    def pwd_context(self):
        return CryptContext(schemes=[self.PASSWORD_HASHING_ALGORITHM])

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
