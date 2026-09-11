from pathlib import Path
from ..files_code.app_structure import *


def create_app(project_name, app_name: str):
    """
    Creates a new FastAPI app with the given name.
    """

    # ---------------------------------------------------------
    # 1. Get current FastAPI project
    # ---------------------------------------------------------
    project_path = Path.cwd()

    apps_path = project_path / project_name / "apps"
    if not apps_path.exists():
        raise FileNotFoundError(
            "apps directory not found. "
            "Make sure you are running this command "
            "from a FastAPI project."
        )

    # ---------------------------------------------------------
    # 2. Create app directory
    # ---------------------------------------------------------
    app_path = apps_path / app_name

    if app_path.exists():
        raise FileExistsError(f"App '{app_name}' already exists.")

    app_path.mkdir(parents=True)

    # ---------------------------------------------------------
    # 3. Create directories
    # ---------------------------------------------------------
    directories = [
        app_path / "views",
        app_path / "schemas",
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # 4. Create files
    # ---------------------------------------------------------
    files = {
        "__init__.py": INIT_PY.format(app=app_name),
        "views/__init__.py": VIEW_INIT_PY,
        f"views/api_{app_name}_view.py": VIEW_PY.format(app=app_name),
        "schemas/__init__.py": "",
        "utils.py": UTILS_PY,
        "models.py": MODELS_PY,
        "constants.py": CONSTANT_PY,
        "enums.py": "",
        "dependencies.py": "",
        "internal_api_calls.py": "",
    }

    # ---------------------------------------------------------
    # 5. Write files
    # ---------------------------------------------------------
    for relative_path, content in files.items():

        file_path = app_path / relative_path

        file_path.write_text(
            content,
            encoding="utf-8",
        )

    print()
    print(f"✓ FastAPI app '{app_name}' " f"created successfully.")
    print(f"  Location: {app_path}")
    print()
