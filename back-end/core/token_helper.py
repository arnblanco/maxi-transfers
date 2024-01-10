import jwt
import os
from datetime import datetime, timedelta

from core.exceptions import DecodeTokenException, ExpiredTokenException


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=os.environ.get("SECRET_KEY"),
            algorithm=os.environ.get("ALGORITHM"),
        )
        return str(token)

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                os.environ.get("SECRET_KEY"),
                os.environ.get("ALGORITHM"),
                options={"verify_signature": False}
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                os.environ.get("SECRET_KEY"),
                os.environ.get("ALGORITHM"),
                options={"verify_exp": False, "verify_signature": False}
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
