from typer.testing import CliRunner

from fa_assist.cli import app
from pathlib import Path

runner = CliRunner()


def test_init_project():
    result = runner.invoke(
        app,
        [
            "init",
            "project",
            "my-project",
        ],
    )

    assert result.exit_code == 0

    project_path = Path.cwd() / "my-project"

    assert project_path.exists()
    assert (project_path / "pyproject.toml").exists()
    

def test_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "FastAPI development assistant" in result.stdout

def test_invalid_project_type():
    result = runner.invoke(
        app,
        [
            "init",
            "project",
            "my-project",
        ],
    )

    assert result.exit_code != 0