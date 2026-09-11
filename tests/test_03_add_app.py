from typer.testing import CliRunner

from fa_assist.cli import app
from pathlib import Path

runner = CliRunner()


def test_add_app():
    result = runner.invoke(
        app,
        [
            "add",
            "app",
            "my-app",
        ],
    )

    assert result.exit_code == 0
    
    project_path = Path.cwd() / "my-project"
    assert project_path.exists()
    assert (project_path / "pyproject.toml").exists()
    

def test_invalid_add_app_type():
    result = runner.invoke(
        app,
        [
            "add",
            "app",
            "my-app",
        ],
    )

    assert result.exit_code != 0