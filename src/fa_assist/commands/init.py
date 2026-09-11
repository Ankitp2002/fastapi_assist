from pathlib import Path
from ..files_code.project_structure import *

def init_project(project_name: str, path: str):
    """
    Initialize a new FastAPI project with the standard
    FastAPI Assist project structure.
    """

    # ---------------------------------------------------------
    # 1. Create project root
    # ---------------------------------------------------------
    project_path = Path(path).resolve() / project_name

    if project_path.exists():
        raise FileExistsError(
            f"Project '{project_name}' already exists at: {project_path}"
        )

        # ---------------------------------------------------------
    # 3. Create directories
    # ---------------------------------------------------------
    directories = [
        project_path / "logs",
        project_path / "credential",
        project_path / "independent_scripts",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # 2. Create files with their initial content
    # ---------------------------------------------------------

    files = {
        "main.py": MAIN_PY,
        ".env": DOT_ENV_FILE,

        "configuration/config.py": CONFIG_PY.format(project_name=project_name),
        "configuration/custom_error.py": CUSTOM_ERROR_PY,
        "configuration/db.py": DB_PY,
        "configuration/logger.py": LOGGER_PY,
        "configuration/rate_limit.py": RATE_LIMIT_PY,
        "configuration/server.py": SERVER_PY.format(project_name=project_name),

        "apps/__init__.py": APPS_INIT_PY,
        "apps/constants.py": CONSTANT_PY,
        "apps/db_operations.py": DB_OPERATIONS_PY,
        "apps/https_response.py": HTTPS_RESPONSE_PY,
        "apps/models.py": MODELS_PY,
        "apps/reg_models.py": REG_MODELS_PY,
        "apps/reg_routers.py": REG_ROUTERS_PY,
        "apps/schemas.py": SCHEMAS_PY,
        "apps/utils.py": UTILS_PY,

        "Dockerfile": DOCKER,
        ".docker-compose.yaml": DOCKER_COMPOSE.format(project_name=project_name),
        "docker_setup.sh": DOCKER_SETUP_SH,

        "deployment.sh": DEPLOYMENT_SH.format(project_name=project_name),
    }

    for relative_path, content in files.items():
        file_path = project_path / relative_path

        # Make sure the parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(
            content,
            encoding="utf-8",
        )

    print()
    print(f"✓ FastAPI project '{project_name}' created successfully.")
    print(f"  Location: {project_path}")
    print()
