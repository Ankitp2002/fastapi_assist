from pathlib import Path
from ..files_code.app_structure import (
    CONSTANT_PY,
    URLS_PY,
    MODELS_PY,
    UTILS_PY,
    INIT_PY,
)


def create_app(project_name: str):
    """
    Creates a new FastAPI app with the given name.
    """

    # ---------------------------------------------------------
    # 1. Get current FastAPI project
    # ---------------------------------------------------------
    project_path = Path.cwd()

    apps_path = project_path / "apps"

    if not apps_path.exists():
        raise FileNotFoundError(
            "apps directory not found. "
            "Make sure you are running this command "
            "from a FastAPI project."
        )

    # ---------------------------------------------------------
    # 2. Create app directory
    # ---------------------------------------------------------
    app_path = apps_path / project_name

    if app_path.exists():
        raise FileExistsError(f"App '{project_name}' already exists.")

    app_path.mkdir(parents=True)

    # ---------------------------------------------------------
    # 3. Create directories
    # ---------------------------------------------------------
    directories = [
        app_path / "views",
        app_path / "enums",
        app_path / "dependencies",
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
        "__init__.py": INIT_PY,
        "models.py": MODELS_PY,
        "urls.py": URLS_PY,
        "constant.py": CONSTANT_PY,
        "utils.py": UTILS_PY,
        "views/__init__.py": "",
        "enums/__init__.py": "",
        "dependencies/__init__.py": "",
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
    print(f"✓ FastAPI app '{project_name}' " f"created successfully.")
    print(f"  Location: {app_path}")
    print()
