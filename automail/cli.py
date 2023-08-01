from automail import __app_name__, __version__
from typing import Optional
import typer
import shutil
from automail.storage import get_session, create_tables


app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )

) -> None:
    return


@app.command()
def init(
    db_path: str = typer.Option(
        './',
        "--db-path",
        "-db",
        prompt="Where do you want to initialize the automail project?",
    ),
) -> None:
    """Initialize the to-do database."""
    from automail.storage import util
    from automail import __app_name__

    typer.echo(f"Initializing {__app_name__} database...")

    # db_path = shutil.os.path.abspath(db_path)
    if not shutil.os.path.exists(db_path):
        shutil.os.mkdir(db_path)
    else:
        typer.secho(f"Directory {db_path} already exists.", fg=typer.colors.RED)
        # delete the folder if it exists
        if typer.confirm("Do you want to delete it?", default=False):
            shutil.rmtree(db_path)
            shutil.os.mkdir(db_path)
        else:
            typer.echo("Aborted!")
            raise typer.Exit(code=1)
    shutil.os.chdir(db_path)
    session, engin = get_session()
    create_tables(engin)
    typer.echo("Done!")
    return


if __name__ == "__main__":
    app(prog_name=__app_name__)
