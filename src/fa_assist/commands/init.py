from pathlib import Path
from ..files_code.project_structure import (
    MAIN_PY,
    SERVER_PY,
    CONFIG_PY,
    DB_PY,
    ENV,
    REG_MODEL_PY,
    REG_ROUTER_PY,
    UTILS_PY,
    CONSTANT_PY,
    ENUMS_PY,
    DEPENDANCIES_PY,
)


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
    # 2. Create directories
    # ---------------------------------------------------------
    directories = [
        project_path / "cred",
        project_path / "apps",
        project_path / "indipended_scripts",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # 3. Create files with their initial content
    # ---------------------------------------------------------

    files = {
        "main.py": MAIN_PY,
        "server.py": SERVER_PY,
        "config.py": CONFIG_PY,
        "db.py": DB_PY,
        ".env": ENV,
        "apps/__init__.py": "",
        "apps/reg_model.py": REG_MODEL_PY,
        "apps/reg_router.py": REG_ROUTER_PY,
        "apps/utils.py": UTILS_PY,
        "apps/constant.py": CONSTANT_PY,
        "apps/enums.py": ENUMS_PY,
        "apps/dependencies.py": DEPENDANCIES_PY,
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
