from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv(override=True)


class Settings(BaseSettings):
    app_title: str = 'QRkot'
    app_description: str = 'Приложение для Благотворительного фонда ' \
                           'поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    auth_provider_x509_cert_url: Optional[str] = None
    auth_uri: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    private_key: Optional[str] = None
    private_key_id: Optional[str] = None
    project_id: Optional[str] = None
    token_uri: Optional[str] = None
    type: Optional[str] = None

    class Config:

        env_file = ".env"


settings = Settings()
