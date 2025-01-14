import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Tienda Online API"
    SECRET_KEY: str = "tu_clave_secreta_muy_segura"  # En producción, usar variable de entorno
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STRIPE_API_KEY: str = os.getenv("Stripe_apikey")
    PUBLIC_KEY: str = os.getenv("Stripe_publickey")
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]




settings = Settings() 