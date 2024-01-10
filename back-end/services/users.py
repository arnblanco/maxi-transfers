from passlib.context import CryptContext
from sqlalchemy import text

from app.request import CreateUserRequestSchema, LoginRequest
from app.response import CreateUserResponseSchema, LoginResponse
from core.config import connect
from core.exceptions import DatabaseSQLErrorException, UserNotFoundException
from core.token_helper import TokenHelper


class UserService:
    def __init__(self):
        ...

    def pwd_context(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def fetch_user_by_username(self, username: str):
        try:
            with connect() as conn:
                result = conn.execute(
                    text("EXEC GetUserByUsername :username"),
                    {
                        "username": username
                    }
                )
                user_data = result.fetchone()
                return user_data
        except Exception as error:
            raise DatabaseSQLErrorException

    async def create_user(self, req: CreateUserRequestSchema):
        try:
            hased_password = self.pwd_context().hash(req.password)

            with connect() as conn:
                result = conn.execute(
                    text("EXEC InsertUser :first_name, :last_name, :email, :username, :password, :is_active"),
                    {
                        "first_name": req.first_name,
                        "last_name": req.last_name,
                        "email": req.email,
                        "username": req.username,
                        "password": hased_password,
                        "is_active": True,
                    },
                )
                conn.commit()
            
            user_data = await self.fetch_user_by_username(req.username)
            return await self.transform_user_data(user_data)
        except Exception as error:
            raise DatabaseSQLErrorException

    async def verify_login(self, req: LoginRequest) -> LoginResponse:
        user_data = await self.fetch_user_by_username(req.username)

        if not user_data:
            raise UserNotFoundException
        
        response = LoginResponse(
            access_token=TokenHelper.encode(payload={"username": user_data[3]}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )

        return response

    async def transform_user_data(self, user_data)->CreateUserResponseSchema:
        user_response = CreateUserResponseSchema(
            first_name=user_data[0],
            last_name=user_data[1],
            email=user_data[2],
            username=user_data[3],
            is_active=user_data[4]
        )

        return user_response