from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser[int]):
    """Базовая схема модели пользователя для чтения."""


class UserCreate(BaseUserCreate):
    """Схема для создания нового пользователя."""


class UserUpdate(BaseUserUpdate):
    """Схема для обновления существующего пользователя."""
