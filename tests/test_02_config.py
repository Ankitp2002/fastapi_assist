import json

from src.fa_assist.util import set_project_name_into_config, get_project_name_into_config
from pathlib import Path

def test_set_project_name_into_config():
    set_project_name_into_config(
        project_name="my-project",
    )
    config_file = Path.cwd() / "src" / "fa_assist" / "mycli" / "config.json"

    assert config_file.exists()

    config = json.loads(config_file.read_text())

    assert config["project_name"] == "my-project"
    
def test_get_project_name():
    set_project_name_into_config(
        project_name="my-project",
    )

    result = get_project_name_into_config()

    assert result == "my-project"