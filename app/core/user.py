from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User

from app.services.constants import Limits


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Aсинхронный генератор, создает адаптер для взаимодействия с базой
    данных, передавая в качестве параметров экземпляр сессии и класс модели
    пользователя
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=Limits.JWT_TOKEN_LIFETIME.value
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Args:
        IntegerIDMixin : обеспечивает возможность использования
            целочисленных id для таблицы пользователей
        BaseUserManager : этом классе производятся основные действия:
            аутентификация, регистрация, сброс пароля, верификация и другие.
    """
    async def validate_password(
            self,
            password,
            user
    ):
        if len(password) < Limits.MIN_PASSWORD_LENGTH.value:
            raise InvalidPasswordException(
                reason="Passord should be at least 3 chars long."
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password shouldn't contain e-mail."
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.email} has been registred.")


async def get_user_manager(user_db=Depends(get_user_db)):
    """Корутина, возвращающая объект класса UserManager"""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
