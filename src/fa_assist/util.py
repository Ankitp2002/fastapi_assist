def check_or_raise_error(condition, err_msg: str = "Condition not met"):
    """
    Checks a condition and raises a general error if it is not met.
    """
    if not condition:
        raise Exception(err_msg)


CONFIG_DIR = "mycli"
CONFIG_FILE = "config.json"

import json
from pathlib import Path

# def set_project_name_into_config(
#     project_name: str,
# ):
#     project_path = Path(__file__).parent.resolve()

#     config_dir = project_path / CONFIG_DIR
#     config_dir.mkdir(
#         parents=True,
#         exist_ok=True,
#     )

#     config_path = config_dir / CONFIG_FILE

#     config = {}

#     if config_path.exists():
#         try:
#             config = json.loads(config_path.read_text(encoding="utf-8"))
#         except Exception:
#             config = {}

#     config["project_name"] = project_name

#     config_path.write_text(
#         json.dumps(
#             config,
#             indent=4,
#         ),
#         encoding="utf-8",
#     )


# def get_project_name_into_config() -> str:
#     project_path = Path(__file__).parent.resolve()

#     config_path = project_path / CONFIG_DIR / CONFIG_FILE

#     if not config_path.exists():
#         return "."

#     try:
#         config = json.loads(config_path.read_text(encoding="utf-8"))
#     except Exception:
#         config = {}

#     project_name = config.get("project_name", ".")

#     return project_name
