from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_USERNAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AZ_BLOB_ACCOUNT_NAME: str
    AZ_BLOB_ACCOUNT_KEY: str
    AZ_BLOB_CONTAINER_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USERNAME}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
