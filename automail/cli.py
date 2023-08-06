import os
import shutil
import time
import typer
from typing import Optional
from pathlib import Path
from automail import __app_name__, __version__, EmailSender
from automail.utils import get_config_dict, read_config_file, init_logger
from automail.storage import get_session, create_tables
from automail.storage.model import Record, Process


app = typer.Typer()


def run_process(pid, resume=True):
    """
    This function will run a process with a specific id

    Parameters
    ----------
    pid : int
        the process id
    resume : bool
        if True, the program will resume the process if it is paused, otherwise it prints a warning message and \
        return without doing anything
    """

    session, engin = get_session()
    create_tables(engin)

    logger = init_logger('manager')
    logger.info("Reading arguments...")
    process = session.query(Process).filter(Process.id == pid).first()
    if not process:
        logger.error(f"ID:{pid} => Process not found. You can see all processes with 'mailmanager list' command")
        return
    sender_email = process.sender
    subject = process.subject
    temp_file = process.temp_file
    if resume:
        if process.status != "paused":
            print(f"ID:{pid} => Program is already {process.status}")
            return
        contacts = session.query(Record).filter(Record.process_id == pid, Record.status == "unsent").all()
    else:
        if process.status in ["paused", "in progress", 'finished']:
            logger.warning(f"ID:{pid} => Program is already {process.status}")
            print(f"ID:{pid} => Program is already {process.status}")
            print(f"You can resume the program with 'mailmanager resume {pid}' command")
            print(f"You can see all processes with 'mailmanager list' command")
            while True:
                check = input(f"Are you sure you want to sent all email again? (y/n)")
                if check == "n":
                    return
                elif check == "y":
                    break
                else:
                    print("Please enter y or n!")
        contacts = session.query(Record).filter(Record.process_id == pid).all()

    password = typer.prompt(f"Enter password for {sender_email}", hide_input=True)

    # Create a secure SSL context
    logger.info("Creating EmailSender obj...")
    sender = EmailSender(cfg="config.cfg", user=sender_email, password=password)
    if temp_file:
        sender.set_template(temp_file)

    process.status = "in progress"
    session.commit()

    pause = False
    for contact in contacts:
        process = session.query(Process).filter(Process.id == pid).first()
        if process.status == "paused":
            logger.info(f"ID:{pid} => Pausing the program")
            pause = True
            break
        logger.info(f"Sending email to: {contact.receiver}")
        sender.send(contact.receiver, subject, contact.data)
        contact.status = "sent"
        session.commit()
        logger.info(f"ID:{contact.id} => Email sent to {contact.receiver}")
        time.sleep(10)

    if not pause:
        process.status = "finished"
        session.commit()
        logger.info(f"ID:{pid} => Program finished successfully")


    session.close()
    engin.dispose()


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


@app.command()
def start(
    id: Optional[int] = typer.Argument(
        None,
        help="The id of the process.",
    ),
    is_test: bool = typer.Option(
        False,
        "--test",
        "-t",
        help="Test output.",
    ),
) -> None:
    """Start sending emails."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Starting...")
    if id is None:
        typer.secho("Please enter the id of the process.", fg=typer.colors.RED)
        raise typer.Exit(code=0)
    else:
        run_process(pid=id, resume=False)


@app.command()
def resume(
    id: Optional[int] = typer.Argument(
        None,
        help="The id of the process.",
    ),
    is_test: bool = typer.Option(
        False,
        "--test",
        "-t",
        help="Test output.",
    ),
) -> None:
    """Resume sending emails."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Resuming...")
    if id is None:
        typer.secho("Please enter the id of the process.", fg=typer.colors.RED)
        raise typer.Exit(code=0)
    else:
        run_process(pid=id, resume=True)


@app.command()
def stop(
    id: Optional[int] = typer.Argument(
        None,
        help="The id of the process.",
    ),
    is_test: bool = typer.Option(
        False,
        "--test",
        "-t",
        help="Test output.",
    ),
) -> None:
    """Stop sending emails."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Stopping...")
    if id is None:
        """This function will stop a process with a specific id"""
        session, engin = get_session()
        create_tables(engin)

        session.close()
        engin.dispose()
        process = session.query(Process).filter(Process.id == pid).first()
        if process.status == "in progress":
            process.status = "paused"
            session.commit()
            print(f"ID: {pid} => Pausing the program")
        else:
            print(f"ID: {pid} => Program is not running")


@app.command()
def delete_process(
    id: Optional[int] = typer.Argument(
        None,
        help="The id of the process.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Test output.",
    ),
) -> None:
    """Delete a process."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Deleting...")
    if id is None:
        typer.secho("Please enter the id of the process.", fg=typer.colors.RED)
        raise typer.Exit(code=0)
    else:
        session, engin = get_session()

        process = session.query(Process).filter(Process.id == id).first()
        if process is None:
            typer.secho(f"Process with id {id} does not exist.", fg=typer.colors.RED)
            raise typer.Exit(code=0)
        else:
            if dry_run:
                typer.echo(f"Process with id {id} will be deleted.")
            else:
                session.delete(process)
                session.commit()
                typer.echo(f"Process with id {id} has been deleted.")
                shutil.rmtree(process.title)
        session.close()
        engin.dispose()


@app.command()
def delete_record(
    id: Optional[int] = typer.Argument(
        None,
        help="The id of the record.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Test output.",
    ),
) -> None:
    """Delete a record."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Deleting...")
    if id is None:
        typer.secho("Please enter the id of the record.", fg=typer.colors.RED)
        raise typer.Exit(code=0)
    else:
        session, engin = get_session()

        record = session.query(Record).filter(Record.id == id).first()
        if record is None:
            typer.secho(f"Record with id {id} does not exist.", fg=typer.colors.RED)
            raise typer.Exit(code=0)
        else:
            if dry_run:
                typer.echo(f"Record with id {id} will be deleted.")
            else:
                session.delete(record)
                session.commit()
                typer.echo(f"Record with id {id} has been deleted.")
        session.close()
        engin.dispose()


@app.command()
def list() -> None:
    """List all processes."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Listing...")
    session, engin = get_session()
    create_tables(engin)

    processes = session.query(Process).all()
    if len(processes) == 0:
        typer.echo("There is no process.")
    else:
        for process in processes:
            typer.echo(
                f"ID: {process.id} | Title: {process.title} | Status: {process.status}"
            )
    session.close()
    engin.dispose()


@app.command()
def list_records(
        process_id: Optional[int] = typer.Argument(
            None,
            help="The id of the process.",
        )) -> None:
    """List all records."""
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        from automail.storage import util, Process, Record

        print("Listing...")
    session, engin = get_session()
    create_tables(engin)

    if process_id is None:
        records = session.query(Record).all()
    else:
        records = (
            session.query(Record).filter(Record.process_id == process_id).all()
        )
    if len(records) == 0:
        typer.echo("There is no record.")
    else:
        for record in records:
            typer.echo(
                f"ID: {record.id} | Process ID: {record.process_id} | Email: {record.receiver} | Status: {record.status}"
            )
    session.close()
    engin.dispose()

if __name__ == "__main__":
    app(prog_name=__app_name__)
