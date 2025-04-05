from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    Для работы с переменными окружениями в FastAPI , 
    унаследованный от класса BaseSettings 
    """
    app_title: str = "Charity Project"
    database_url: str = "sqlite+aiosqlite:///./cat_charities.db"
    secret: str = "SERCET_KEY"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
