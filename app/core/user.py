from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import (
    AUTHENTIFICATION_BACKEND_NAME,
    LIFETIME_SECONDS,
    MIN_LEN_PASSWORD,
    PASSWORD_CONTAINS_EMAIL,
    PASSWORD_MIN_LEN_EXCEPTION,
    REGISTRATION_COMPLETE,
    settings,
    TOKEN_URL,
)
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(settings.secret, LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    AUTHENTIFICATION_BACKEND_NAME,
    BearerTransport(TOKEN_URL),
    get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[User, UserCreate],
    ) -> None:
        if len(password) < MIN_LEN_PASSWORD:
            raise InvalidPasswordException(PASSWORD_MIN_LEN_EXCEPTION)
        if user.email in password:
            raise InvalidPasswordException(PASSWORD_CONTAINS_EMAIL)

    async def on_after_register(
        self, user: User, request: Optional[Request] = None,
    ):
        print(REGISTRATION_COMPLETE.format(email=user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
