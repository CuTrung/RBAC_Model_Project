from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"   

settings = Settings()
