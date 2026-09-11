UTILS_PY = """

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
CONSTANT_PY = """

"""

MODELS_PY = """

"""

INIT_PY = """

from configuration.logger import create_get_logger
    
get_logger = create_get_logger("{app}")

"""

VIEW_INIT_PY = """

import pkgutil, importlib
from . import *
from fastapi import APIRouter

_file_routers = tuple()

for file in pkgutil.iter_modules(__path__):
    _file = importlib.import_module(f"{__name__}.{file.name}")
    if hasattr(_file, "routers"):
        _file_routers += (_file.routers, )

__routers: tuple[APIRouter, ...] = _file_routers

"""

VIEW_PY = """

from pathlib import Path
import traceback

import pandas as pd
from tortoise.expressions import Q

from apps import generate_router as APIRoute
from apps.db_operations import read_instances
from apps.https_response import error_response, success_response
from fastapi import Body, Depends
from ...{app} import get_logger

routers = APIRoute('/{app}', tags=["{app} View Section"])
logger = get_logger("{app}_view")

@routers.get("")
async def api_view():
    logger.info("API view called")
    return success_response(data = "", message = "success")
    
"""
