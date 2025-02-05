from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_PORT: int
    BASE_URL: str
    REDIS_HOST: str
    TIMEZONE: str

    model_config = SettingsConfigDict(env_file="./env")


settings = Settings()
