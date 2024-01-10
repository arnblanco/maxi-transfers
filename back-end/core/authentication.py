import jwt
import os

from typing import Optional, Tuple
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from core.current_user import CurrentUser


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        
        if not authorization:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload = jwt.decode(
                credentials,
                os.environ.get("SECRET_KEY"),
                algorithms=[os.environ.get("ALGORITHM")],
                options={"verify_signature": False}
            )
            username = payload.get("username")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.username = username
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
