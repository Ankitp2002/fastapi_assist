from pathlib import Path

import typer

from fa_assist.commands.init import init_project
from .util import (
    check_or_raise_error,
    # get_project_name_into_config,
    # set_project_name_into_config,
)
from fa_assist.commands.create import create_app

app = typer.Typer(name="fa_assist", help="FastAPI development assistant.")


@app.command("init")
def init(
    project_type: str,
    project_name: str = typer.Argument("."),
    path: str = typer.Argument("."),
):

    check_or_raise_error(
        project_type == "project",
        "Provide project as resource to create a new FastAPI project.",
    )
    init_project(project_name, path)

    # if project_name != ".":
    #     set_project_name_into_config(project_name)


@app.command("add")
def add(
    resource: str,
    app_name: str,
):
    check_or_raise_error(
        resource == "app", "Provide app as resource to create a new FastAPI app."
    )
    # project_name = get_project_name_into_config()
    # create_app(project_name, app_name)
    create_app(app_name)


def main():
    app()
