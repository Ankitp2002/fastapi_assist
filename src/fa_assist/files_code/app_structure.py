UTILS_PY = """\
\"\"\"
Utility functions for this application.
\"\"\"


def success_response(
    data=None,
    message="Success",
):
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message="Something went wrong",
):
    return {
        "success": False,
        "message": message,
        "data": None,
    }
"""
CONSTANT_PY = """\
\"\"\"
Application-level constants.
\"\"\"

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
"""
URLS_PY = """\
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def index():
    return {
        "message": "Application is working"
    }
"""
MODELS_PY = """\
\"\"\"
Database models for this application.
\"\"\"

# Example:
#
# from sqlalchemy import Column, Integer, String
# from db import Base
#
#
# class Example(Base):
#     __tablename__ = "examples"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
"""
INIT_PY = """\
"""
