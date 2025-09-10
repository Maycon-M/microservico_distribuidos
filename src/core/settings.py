from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    
    ENV: str = "dev"
    
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    
    # Banco de dados
    DB_SERVER: str
    DB_PORT: str
    DB_DATABASE: str
    DB_UID: str
    DB_PWD: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @computed_field(return_type=str)
    @property
    def DATABASE_URL (self) -> str: #pylint: disable=invalid-name
        return (
            f"postgresql+psycopg://{self.DB_UID}:{quote_plus(self.DB_PWD)}"
            f"@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

settings = Settings() #type: ignore