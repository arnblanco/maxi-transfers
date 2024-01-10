import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from starlette.middleware.sessions import SessionMiddleware
from typing import List

from core.authentication import AuthBackend, AuthenticationMiddleware
from core.exceptions import CustomException, DatabaseConnectionErrorException
from core.middleware import ResponseLogMiddleware
from core.logging import Logging


def connect():
    try:
        username = os.environ.get("MSSQL_USER")
        password = os.environ.get("MSSQL_PASSWORD")
        server = os.environ.get("MSSQL_HOST")
        database = os.environ.get("MSSQL_DB")
        
        engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=FreeTDS&port=1433&odbc_options='TDS_Version=8.0'", echo=False)
        connection = engine.connect()
    except Exception as e:
        raise DatabaseConnectionErrorException

    return connection


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
    title="Maxi Transfers",
        description="MaxiTransfers API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_listeners(app_=app_)
    return app_
