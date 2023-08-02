from automail import __app_name__, __version__
from typing import Optional
import typer
import shutil
from automail.storage import get_session, create_tables
import time
import os
from pathlib import Path
from automail.utils import get_config_dict, read_config_file



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
        './automail-workspace',
        "--db-path",
        "-db",
        prompt="Where do you want to initialize the automail project?",
    ),
    smtp_server: str = typer.Option(
        'smtp.gmail.com',
        "--smtp-server",
        "-ss",
        prompt="What is your smtp server?",
        help="Your smtp server.",
    ),
    smtp_port: int = typer.Option(
        465,
        "--smtp-port",
        "-sp",
        prompt="What is your smtp port?",
        help="Your smtp port.",
    ),
    email: str = typer.Option(
        '',
        "--email",
        "-e",
        help="Your email address.",
    ),
    password: str = typer.Option(
        '',
        "--password",
        "-p",
        help="Your email password.",
        hide_input=True,
    ),
    is_test: bool = typer.Option(
        False,
        "--test",
        "-t",
        help="Test output.",
    ),
) -> None:
    """Initialize the mail database."""
    from automail import utils
    from automail import __app_name__

    if not shutil.os.path.exists(db_path):
        shutil.os.mkdir(db_path)
    else:
        typer.secho(f"Directory {db_path} already exists.", fg=typer.colors.RED)
        # delete the folder if it exists
        if typer.confirm("Do you want to delete it?", default=False):
            shutil.rmtree(db_path)
            print("Deleting...")
            time.sleep(0.5)
            shutil.os.mkdir(db_path)

        else:
            typer.echo("Aborted!")
            raise typer.Exit(code=0)

    typer.echo(f"Initializing {__app_name__} database...")
    os.chdir(db_path)
    session, engin = get_session()
    create_tables(engin)
    typer.echo("Done!")
    # create the config file
    typer.echo("Creating config file...")
    utils.create_config_file(
        smtp_server=smtp_server, smtp_port=smtp_port, password=password, sender_email=email, is_test=is_test
    )
    os.chdir("../")

    session.close()
    engin.dispose()
    return


@app.command()
def register(
    email: str = typer.Option(
        get_config_dict().get("user", None),
        "--email",
        "-e",
        prompt="What is your email address?",
        help="Your email address.",
    ),
    contact_list: Path = typer.Argument(
            ...,
            exists=True,
            help="The path to your contact list.",
        ),
    title: str = typer.Option(
        "Contact List",
        "--title",
        "-T",
        prompt="What is the title of your contact list?",
        help="The title of your contact list.",
    ),
    custom_pdf: bool = typer.Option(
        False,
        "--custom-pdf",
        "-CA",
        help="Convert your contact list to pdf.",
    ),
    attachment: Path = typer.Option(
        None,
        "--attachment",
        "-a",
        help="The path to the attachment file.",
    ),
    custom_pdf_dir: Path = typer.Option(
        None,
        "--custom-pdf-dir",
        "-cpd",
        help="The path to the custom pdf directory.",
    ),
    subject: str = typer.Option(
        'None',
        "--subject",
        "-s",
        prompt="What is the subject of your email?",
        help="The subject of your email.",
    ),
    template: Optional[Path] = typer.Option(
        None,
        "--template",
        "-t",
        # exists=True,
        # file_okay= True,
        help="The body of your email.",
    ),

) -> None:
    """Register your email account."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util
        from automail import utils

        if template is None:
            tmp = typer.confirm("Do you want to use template?", default=False)
            if tmp:
                while True:
                    template = typer.prompt("Please enter the path to your template file.", type=Path)
                    if os.path.isfile(template) and (template.suffix == '.txt' or template.suffix == '.html'):
                        template = str(template)
                        break
                    else:
                        typer.secho(f"File {template} does not exist. or the file type is not supported. "
                                    f"the file type should be .txt or .html", fg=typer.colors.RED)
                        continue
        print(title)
        if not os.path.exists(title):
            shutil.os.mkdir(title)
        else:
            typer.secho(f"Directory {title} already exists. Please choose another title.", fg=typer.colors.RED)
            raise typer.Exit(code=0)

        shutil.copy(contact_list, title)
        contact_list = os.path.join(title, os.path.basename(contact_list))

        if attachment:
            shutil.copy(attachment, title)
            attachment = os.path.join(title, os.path.basename(attachment))
        if template:
            shutil.copy(template, title)
            template = os.path.join(title, os.path.basename(template))

        typer.echo("Registering your email account...")
        util.register_new_process(
            email=email,
            contact_list=contact_list,
            title=title,
            custom_pdf=custom_pdf,
            attachment=attachment,
            custom_pdf_dir=custom_pdf_dir,
            subject=subject,
            template=template,
        )

    else:
        typer.secho("Please initialize the automail project first.", fg=typer.colors.RED)
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app(prog_name=__app_name__)
