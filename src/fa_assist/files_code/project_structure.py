MAIN_PY = """
from configuration.server import Server


def create_app():
    "Create and return the FastAPI app."
    return Server().app


app = create_app()

"""


SERVER_PY = """


from fastapi.concurrency import asynccontextmanager
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from configuration.config import get_app_setting
from configuration.rate_limit import ApiRateLimit
from apps.reg_routers import __routers__
from configuration.db import init_db, close_db

@asynccontextmanager
async def _lifespan(app: FastAPI):
    await init_db()
    
    # set app config at startup
    app.state.settings = get_app_setting()
    
    yield
    await close_db()
    
class Server:
    __slots__ = ["_app", "_setting", "_rate_limit"]
    
    def __init__(self):
        self._setting = get_app_setting()
        self._rate_limit = ApiRateLimit()
        self._app: FastAPI = FastAPI(
            docs_url="/api/{project_name}/docs",
            redoc_url="/api/{project_name}/redoc",
            openapi_url="/api/{project_name}/openapi.json",
            title=self._setting.APP_NAME,
            debug=self._setting.APP_DEBUG_MODE,
            lifespan=_lifespan
        )
        self._configure_routers(*__routers__)
        self._middleware()
                
    @property
    def app(self) -> FastAPI:
        return self._app

    def _configure_routers(self, *routers: APIRouter) -> None:
        for router in routers:
            self._app.include_router(router, prefix="/api/{project_name}")
            
    def _middleware(self) -> None:
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins = self._setting.ALLOW_ORIGINS,
            allow_credentials = True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        @self._app.middleware("http")
        async def rate_limit_middleware(request: Request, call_next):
            client_ip = request.client.host
            if not self._rate_limit.is_allow(client_ip):
                raise HTTPException(status_code=429, detail="Too Many Request")
            return await call_next(request)
            
"""


CONFIG_PY = """
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Setting(BaseSettings):
    ENV: str = "dev"
    UI_DOMAIN: str = "localhost:3000"
    APP_NAME: str = "{project_name}"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "pas_ai"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_SSL: bool = False
    SSL_KEY_PATH: str = ""
    SSL_CERT_PATH: str = ""
    SSL_CA_PATH: str = ""
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "your_secret_key"
    APP_DEBUG_MODE: bool = False
    ALLOW_ORIGINS: list = ["*"]
    
    class config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    @field_validator("*", mode="before")
    def env_validate(cls, v):

        if v in ["True", "true", True]:
            return True

        if v in ["False", "false", False]:
            return False

        if isinstance(v, str):
            return v.strip()

        return v        
    
@lru_cache
def get_app_setting() -> Setting:
    return Setting()

"""


DB_PY = """

from configuration.config import get_app_setting
import ssl
from tortoise import Tortoise
from apps.reg_models import __models__

app_config = get_app_setting()

if app_config.DB_SSL:
    # ssl enable then map with cert..
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(app_config.SSL_CA_PATH)
    ssl_context.load_cert_chain(app_config.SSL_CERT_PATH, app_config.SSL_KEY_PATH)
    ssl_context.check_hostname = False

# prefix formate for async tortoise orm
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": app_config.DB_HOST,
                "port": app_config.DB_PORT,
                "user": app_config.DB_USER,
                "password": app_config.DB_PASSWORD,
                "database": app_config.DB_NAME,
                "charset": "utf8mb4",
                "ssl": ssl_context if app_config.DB_SSL else None,
            },
        }
    },
    "apps": {
        "models": {
            "models": [*__models__],
            "default_connection": "default",
        }
    },
}

async def init_db():
    if not Tortoise._inited:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas(safe=True)    

async def close_db():
    await Tortoise.close_connections()

"""


REG_MODEL_PY = """

from tortoise.models import Model
from tortoise import fields

class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True, description="Created timestamp")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated timestamp")

    class Meta:
        abstract = True
"""


REG_ROUTER_PY = """
from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
"""


UTILS_PY = """
import pandas as pd

def safe_fillna(df: pd.DataFrame) -> pd.DataFrame:
    "Fill NaN/NA values safely based on dtype."
    fill_values = {}
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            fill_values[col] = pd.NaT
        elif pd.api.types.is_numeric_dtype(df[col]):
            fill_values[col] = 0
        else:  # object, string, Boolean, etc.
            fill_values[col] = "NA"

    return df.fillna(value=fill_values)
"""


CONSTANT_PY = """
MONTH_PATTERN = "%b '%y"
IST_TIME_ZONE = "Asia/Kolkata"
TRACEBACK_INFO = "Traceback info: "

"""


ENV = """
APP_NAME=FastAPI Application
DEBUG=True
DATABASE_URL=
"""

ENUMS_PY = """
# Define your application enums here.
"""

DEPENDENCIES_PY = """
# Define your application dependencies here.
"""

APPS_INIT_PY = """

import logging
from fastapi import APIRouter

def generate_router(_app_name, tags: list[str] = []) -> APIRouter:
    
    if not tags:
        tags = [_app_name]
        
    _router = APIRouter(prefix=_app_name, tags=tags)
    
    return _router
"""

CUSTOM_ERROR_PY = """
class InvalidSKUArgumentError(Exception):...

"""


LOGGER_PY = """
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import glob
import logging
import os
from apps.constants import IST_TIME_ZONE

LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_RETENTION_DAYS = 7

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def cleanup_old_logs(log_path, module_name, level_name):
    pattern = os.path.join(log_path, f"{module_name}_{level_name}_*.log")
    all_logs = glob.glob(pattern)

    cutoff_date = datetime.now(ZoneInfo(IST_TIME_ZONE)) - timedelta(days=LOG_RETENTION_DAYS)
    for log_file in all_logs:
        try:
            date_str = log_file.rsplit("_", 1)[-1].replace(".log", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff_date:
                os.remove(log_file)
        except Exception:
            continue  # Ignore errors in date parsing or file deletion
        
def create_log_level_handler(module_name, level_name, level):
    log_path = os.path.join(LOG_DIR, module_name)
    os.makedirs(log_path, exist_ok=True)

    module_base = module_name.split("/")[-1]
    current_filename = f"{module_base}_{level_name}.log"

    log_file_path = os.path.join(log_path, current_filename)

    # If yesterday's log file exists, rename it with the date
    if os.path.exists(log_file_path):
        file_mod_date = datetime.fromtimestamp(os.path.getmtime(log_file_path), tz=ZoneInfo(IST_TIME_ZONE)).date()
        if file_mod_date < datetime.now(ZoneInfo(IST_TIME_ZONE)).date():
            dated_log = os.path.join(log_path, f"{module_base}_{level_name}_{file_mod_date}.log")
            os.rename(log_file_path, dated_log)

    # Clean up old logs
    cleanup_old_logs(log_path, module_base, level_name)

    handler = logging.FileHandler(log_file_path)
    handler.setLevel(level)
    handler.addFilter(LevelFilter(level))
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def _core_get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:  # Prevent duplicate handlers
        logger.addHandler(create_log_level_handler(module_name, "info", logging.INFO))
        logger.addHandler(create_log_level_handler(module_name, "debug", logging.DEBUG))
        logger.addHandler(
            create_log_level_handler(module_name, "warning", logging.WARNING)
        )
        logger.addHandler(create_log_level_handler(module_name, "error", logging.ERROR))

    return logger


def create_get_logger(prefix: str) -> logging.Logger:
    "Middleware factory that returns a get_logger function with a fixed prefix"

    def get_logger(name: str = "") -> logging.Logger:
        if not name:
            raise ValueError("Please provide a logger name (e.g., 'user', 'smal')")
        full_name = f"{prefix}/{name}"
        return _core_get_logger(full_name)

    return get_logger

"""


RATE_LIMIT_PY = """

import threading
from typing_extensions import Self
from time import time

# Singleton Method to do this api rate limit 

class ApiRateLimit:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, call_limit: int = 50, sec_time_window: int = 60):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.call_limit = call_limit
                cls._instance.sec_time_window = sec_time_window
                cls._instance.requests = {} # {ip:[timeStamps]}
            return cls._instance
    
    def is_allow(self, ip:str) -> bool:
        now = time()
        window_start = now - self.sec_time_window
        
        if ip not in self.requests:
            self.requests[ip] = []
            
        self.requests[ip] = [t for t in self.requests[ip] if t > window_start]
        
        if len(self.requests[ip]) < self.call_limit:
            self.requests[ip].append(now)
            return True
        
        return False
"""


DB_OPERATIONS_PY = """
import asyncio
import traceback
from typing import Optional, Type, List, Union
from tortoise.models import Model
from pydantic import BaseModel
from tortoise.transactions import in_transaction
import pandas as pd
import logging
from tortoise.expressions import Q
from apps.utils import safe_fillna
from apps.constants import TRACEBACK_INFO
from .https_response import error_response
from fastapi import status

async def insert_instance(
    model: Type[Model], data: dict, logger: logging.Logger
) -> Model:
    try:
        logger.info(
            f"Inserting instance into {model.__name__} with data: {data}"
        )
        db_entry = model(**data)
        await db_entry.save()
        return db_entry
    
    except Exception as e:
        logger.error(f"Error inserting instance into {model.__name__}: {e}")
        logger.error(f"{TRACEBACK_INFO} {traceback.format_exc()}")
        error_response(f"Error inserting instance into {model.__name__}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_instance(
    model: Type[Model], instance_id: int, data: dict, logger: logging.Logger
) -> None:
    try:
        logger.info(
            f"Updating instance in {model.__name__} with id {instance_id} using data: {data}"
        )
        async with in_transaction():
            db_entry = model.filter(id=instance_id)
            if not db_entry.exists():
                raise ValueError(f"Instance with id {instance_id} not found")
            await db_entry.update(**data)
            
    except Exception as e:
        logger.error(
            f"Error updating instance in {model.__name__} with id {instance_id}: {e}"
        )
        logger.error(f"{TRACEBACK_INFO} {traceback.format_exc()}")
        error_response(f"Error updating instance in {model.__name__} with id {instance_id}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)


# Read generic
async def read_instances(
    model: Type[Model],
    logger: logging.Logger,
    schema: Type[BaseModel] = BaseModel,
    response_df: bool = False,
    filters: Union[dict, Q] = {},
    order_by: List[str] = [],
    fields: List[str] = [],
    prefetch: List[str] = [],
    select_related: List[str] = [],
    response_fields: list[str] = []
) -> Union[list, pd.DataFrame]:
    try:
        logger.info(
            f"Reading instances from {model.__name__} with filters: {filters}, order_by: {order_by}, fields: {fields}"
        )
        async with in_transaction():
            qs = model.all()
            if prefetch:
                qs = qs.prefetch_related(*prefetch)
            if select_related:
                qs = qs.select_related(*select_related)
            if filters:
                if isinstance(filters, Q):
                    qs = qs.filter(filters)
                elif filters:
                    qs = qs.filter(**filters)
            if order_by:
                qs = qs.order_by(*order_by)

            if fields:
                # Use values_list for speeds
                rows = await qs.distinct().values_list(*fields)
                
                if response_fields:
                    fields = response_fields
                    
                if response_df:
                    df = pd.DataFrame(rows, columns=fields)
                    df.drop_duplicates(inplace=True)
                    df = safe_fillna(df)
                    return df
                
                return [(dict(zip(fields, row))) for row in rows]
            else:
                # Fallback: full model fetch + values()
                rows = await qs.distinct().values()
                if response_df:
                    return pd.DataFrame(rows)
                return [schema.model_validate(row) for row in rows]
    except Exception as e:
        logger.error(f"Error reading instances from {model.__name__}: {e}")
        logger.error(f"{TRACEBACK_INFO} {traceback.format_exc()}")
        error_response(f"Error reading instances from {model.__name__}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def bulk_insert_instances(
    model: Type[Model], records: List[dict], logger: logging.Logger, return_created_index:bool = False
) -> Union[Optional[List[BaseModel]], list]:
    try:
        logger.info(
            f"Starting bulk insert for {model.__name__} with {len(records)} records"
        )
        if not records:
            logger.warning(
                f"No data provided for bulk insert into {model.__name__}"
            )
            return None  # No data to insert

        if return_created_index:
            async with in_transaction():
                async with asyncio.Semaphore(50):
                    _objs = await asyncio.gather(*(insert_instance(model, i, logger) for i in records))
                return [i.id for i in _objs]

        async def insert_batch(_records: list):
            async with in_transaction():
                await model.bulk_create((model(**_record) for _record in _records), batch_size=5000)
        
        async with asyncio.Semaphore(100):
            await asyncio.gather(*(insert_batch(records[i:i + 10000]) for i in range(0, len(records), 10000)))
        
        # Fastest path: skip schema and return None
        logger.info(
            f"Bulk insert completed for {model.__name__} without returning models"
        )
        return None

    except Exception as e:
        logger.error(f"Error during bulk insert for {model.__name__}: {e}")
        logger.error(f"{TRACEBACK_INFO} {traceback.format_exc()}")
        # error_response(f"Error during bulk insert for {model.__name__}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def bulk_update_instances(
    model: Type[Model],
    update_records: List[dict],
    fields: List,
    logger: logging.Logger
) -> None:
    '''
    update_data: List of dicts, each must include 'id' or specified id_field
    '''
    try:
        logger.info(
            f"Starting bulk update for {model.__name__} with {len(update_records)} records"
        )
        async with in_transaction():
            await model.bulk_update([model(**data) for data in update_records], fields=fields, batch_size=5000)

    except Exception as e:
        logger.error(f"Error during bulk update for {model.__name__}: {e}")
        logger.error(f"{TRACEBACK_INFO} {traceback.format_exc()}")
        error_response(f"Error during bulk update for {model.__name__}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)



async def truncate_table(model: Type[Model], logger: logging.Logger) -> None:
    try:
        table_name = model._meta.db_table  # get actual DB table name
        logger.info(f"Truncating table {table_name}")

        async with in_transaction() as conn:
            await conn.execute_script(f'TRUNCATE TABLE `{table_name}`;')

        logger.info(f"Table {table_name} truncated successfully")

    except Exception as e:
        logger.error(f"Error truncating table {model.__name__}: {e}")
        logger.error(f"{TRACEBACK_INFO} %s", traceback.format_exc())
        error_response(f"Error truncating table {model.__name__}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
async def delete_records(model: Type[Model], filters: Q, logger: logging.Logger) -> None:
    try:
        table_name = model._meta.db_table  # get actual DB table name
        logger.info(f"Delete records from {table_name}")
        
        if not filters:
            return 
        
        qry = model.filter(filters)
        await qry.delete()
        logger.info(f"Delete records successfully from {table_name}")

    except Exception as e:
        logger.error(f"Error truncating table {model.__name__}: {e}")
        logger.error(f"{TRACEBACK_INFO} %s", traceback.format_exc())
        error_response(f"Error truncating table {model.__name__}: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
"""


HTTPS_RESPONSE_PY = """

from typing import Any, Union

from fastapi import HTTPException, status
from apps.schemas import APIResponse


def success_response(data:Union[Any, list] = None, message:str = "Success", status_code: int = status.HTTP_200_OK):
    return APIResponse(data=data, message=message, status_code=status_code)
    
def error_response(error_msg: str = "", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    raise HTTPException(detail=error_msg, status_code=status_code)
"""


MODELS_PY = """
# Define your application database models here.

# Example:
#
# from sqlalchemy.orm import Mapped, mapped_column
#
#
# class User:
#     pass
"""


REG_MODELS_PY = """
import os
base_path = os.path.join(os.getcwd(), "apps")
__models__: list[str] = [f"apps.{i}.models" for i in os.listdir(base_path) if os.path.isdir(f"{base_path}/{i}") and "models.py" in os.listdir(f"{base_path}/{i}")] + ["aerich.models"]
"""


REG_ROUTERS_PY = """

import importlib
from fastapi import APIRouter
import os 

_apps = [
    entry.name
    for entry in os.scandir("apps")
    if entry.is_dir() and os.path.isfile(os.path.join(entry.path, "__init__.py"))
]

_app_routers = tuple()
for _app in _apps:
    _app = importlib.import_module(f"apps.{_app}.views")
    
    if hasattr(_app, "__routers"):
        _app_routers += _app.__routers

__routers__: tuple[APIRouter, ...] = _app_routers

"""


SCHEMAS_PY = """
from typing import Any, Generic, TypeVar, Optional
from pydantic import ConfigDict,BaseModel
from fastapi import status

T = TypeVar("T", bound=BaseModel)

# APIResponse is a generic response model that can be used to standardize API responses.
class APIResponse(BaseModel, Generic[T]):
    data: Optional[Any] = None
    message: str = "Success!!"
    status_code:int = status.HTTP_200_OK

    model_config = ConfigDict(from_attributes=True)        

"""


DOCKER_COMPOSE = """
services:
  {project_name}_be:
    build: 
      context: .
      dockerfile: Dockerfile
      args:
        BUILDKIT_ENABLED: "true"
        
    image: {project_name}_be
    container_name: {project_name}_be
    environment:
      - WORKERS=${{BACKEND_WORKERS:-2}}
    env_file:
      - .env
    ports:
      - "127.0.0.1:8002:8000"
    networks:
      - {project_name}
    restart: unless-stopped
    command: >
      sh -c "aerich upgrade && gunicorn main:app --workers ${{WORKERS:-2}} --bind 0.0.0.0:8000 --access-logfile logs/gunicorn/access.log --error-logfile logs/gunicorn/error.log --log-level info --worker-class uvicorn.workers.UvicornWorker --preload"
    volumes:
      - ./db_data.json:/app/db_data.json
      
      - type: bind
        source: ./logs/docker/
        target: /app/logs
        
      - type: bind
        source: ./ssl_cert/
        target: /app/ssl_cert
    
    
networks:
  {project_name}:
    external: true
"""


DEPLOYMENT_SH = """
# ------ Git ------
git pull

# ------ Configuration ------
LOG_DIR="logs/docker"
BACKEND_IMAGE_NAME="{project_name}_be"
NETWORK="{project_name}"

# mkdir -p ${{LOG_DIR}}/gunicorn sku_excels

# touch db_data.json

# ===========  Step 1: Create Docker network if it doesn't exist =========== #
if ! docker network inspect "$NETWORK" >/dev/null 2>&1; then
    docker network create "$NETWORK"
fi

# ------ Deployment ------
docker compose up -d --build

# ------ Delete None Images ------
docker image prune -f


echo "Deployment completed successfully."
"""


DOCKER_SETUP_SH = """
#!/bin/bash

set -e

echo "Starting Docker installation..."

# Update package list
sudo apt update

# Install dependencies
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker APT repository
echo 
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] 
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | 
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again with Docker repo
sudo apt update

# Show available Docker versions (optional)
# apt-cache policy docker-ce

# Install Docker CE
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Enable and start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Add current user to docker group
sudo usermod -aG docker $USER

echo "Docker installation completed. Please log out and log back in for group changes to take effect."
"""

DOCKER = """ 
# ========= Stage 1: Build with uv (Python 3.12) =========
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 
    UV_LINK_MODE=copy

# Copy only dependency files first (best cache)
COPY pyproject.toml uv.lock* requirements.txt /app/

# Create venv and install ONLY deps (no project yet for better caching)
RUN --mount=type=cache,target=/root/.cache/uv 
    uv venv /opt/.venv && 
    . /opt/.venv/bin/activate && 
    # --frozen enforces the lockfile if present
    uv sync --active

# Now add source and install your project (editable or wheel)
COPY . /app

# ========= Stage 2: Runtime (slim, no compilers) =========
FROM python:3.12-slim-bookworm AS runtime
WORKDIR /app

ENV VIRTUAL_ENV=/opt/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder /opt/.venv /opt/.venv
COPY . .

RUN mkdir -p logs/gunicorn/

# RUN useradd -m appuser && chown -R appuser:appuser /app /opt/venv
# USER appuser
"""

DOT_ENV_FILE = """

DB_NAME=db_name
DB_USER=root
DB_PASSWORD=root

"""
