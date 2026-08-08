from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, SecretStr


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: SecretStr = SecretStr("")
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @computed_field
    @property
    def URL_DATABASE(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
