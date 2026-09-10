import typer

from fa_assist.commands.init import init_project
from .util import check_or_raise_error
from fa_assist.commands.create import create_app

app = typer.Typer(name="fa_assist", help="FastAPI development assistant.")


@app.command("init")
def init(
    project_type: str,
    project_name: str,
    path: str = ".",
):

    check_or_raise_error(
        project_type == "project",
        "Provide project as resource to create a new FastAPI project.",
    )
    init_project(project_name, path)


@app.command("add")
def add(
    resource: str,
    name: str,
):
    check_or_raise_error(
        resource == "app", "Provide app as resource to create a new FastAPI app."
    )
    create_app(name)


def main():
    app()
