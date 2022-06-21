from datetime import timedelta
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'KapkaMarket'
    app_description: str = 'Price comparison service'
    database_url: str
    secret: str = 'where is my money lebowski'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    statistic_time_period: timedelta = timedelta(hours=24)

    class Config:
        env_file = '.env'


settings = Settings()
