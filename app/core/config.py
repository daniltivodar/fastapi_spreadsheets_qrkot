from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./cat_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()

AUTHENTIFICATION_BACKEND_NAME = 'jwt'

CHARITY_PROJECT_NOT_FOUND = 'Благотворительный проект не найден!'

DUPLICATE_NAME_ERROR = (
    'Благотворительный проект с таким именем уже существует!'
)

EMPTY_NAME_ERROR = 'Поле name не может быть null!'

FULL_AMOUNT_LOWER_THAN_INVESTED_AMOUNT_ERROR = (
    'Нелья установить значение full_amount меньше уже вложенной суммы.'
)

LIFETIME_SECONDS = 3600

MAX_LEN_DESCRIPTION = 500

MAX_LEN_NAME = 100

MIN_LEN_PASSWORD = 3

MIN_LEN_STRING = 1

MIN_VALUE_AMOUNT = 0

PASSWORD_CONTAINS_EMAIL = 'Пароль не должен содержать email!'

PASSWORD_MIN_LEN_EXCEPTION = (
    'Пароль должен содержать как минимум три символа!'
)

PROJECT_CLOSED_ERROR = 'Закрытый проект нельзя редактировать!'

PROJECT_HAS_MONEY_ERROR = (
    'В проект были внесены средства, не подлежит удалению!'
)

REGISTRATION_COMPLETE = 'Пользователь {email} зарегистрирован.'

TOKEN_URL = 'auth/jwt/login'
