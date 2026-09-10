MAIN_PY = """\
from fastapi import FastAPI

from apps.reg_router import router


app = FastAPI(
    title="FastAPI Application",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "FastAPI application is running"
    }
"""


SERVER_PY = """\
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
"""


CONFIG_PY = """\
import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "FastAPI Application",
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "True",
    ).lower() == "true"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "",
    )


settings = Settings()
"""


DB_PY = """\
# Database configuration will be implemented here.

# Example:
#
# from sqlalchemy import create_engine
#
# engine = create_engine(
#     settings.DATABASE_URL
# )
"""


REG_MODEL_PY = """\
# Register your application models here.

# Example:
#
# from sqlalchemy.orm import DeclarativeBase
#
#
# class Base(DeclarativeBase):
#     pass
"""


REG_ROUTER_PY = """\
from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
"""


UTILS_PY = """\
def success_response(data=None, message="Success"):
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message="Something went wrong"):
    return {
        "success": False,
        "message": message,
        "data": None,
    }
"""


CONSTANT_PY = """\
APP_NAME = "FastAPI Application"

API_VERSION = "v1"

DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100
"""


ENV = """\
APP_NAME=FastAPI Application
DEBUG=True
DATABASE_URL=
"""

ENUMS_PY = """\
# Define your application enums here.
"""

DEPENDANCIES_PY = """
# Define your application dependencies here.
"""
