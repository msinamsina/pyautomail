import logging
import os
import shutil
import time
import typer
from typing import Optional
from pathlib import Path
from pyautomail import __app_name__, __version__, EmailSender
from pyautomail import utils
from pyautomail.utils import get_config_dict, init_logger
from pyautomail.storage import get_session, create_tables
from pyautomail.storage import util, Process, Record

app = typer.Typer()


def get_logger():
    return init_logger('cli', filename='cli.log', level=logging.DEBUG)


def run_process(pid, is_resume=True, wait_time=.05):
    """
    This function will run a process with a specific id

    Parameters
    ----------
    pid : int
        the process id
    is_resume : bool
        if True, the program will resume the process if it is paused, otherwise it prints a warning message and \
        return without doing anything
    wait_time : int
        the time to wait between sending emails
    """
    # initialize the logger
    logger = get_logger()
    logger.info("Reading arguments...")

    # get the database session
    session, engin = get_session()
    create_tables(engin)

    # get the process and check if it exists
    process = session.query(Process).filter(Process.id == pid).first()
    if not process:
        logger.error(f"ID:{pid} => Process not found. You can see all processes with 'automail list' command")
        return

    sender_email = process.sender
    subject = process.subject
    temp_file = process.temp_file

    if is_resume:
        if process.status != "paused":
            logger.error(f"ID:{pid} => Program is already {process.status}. "
                         f"For resuming the program, it should be paused")
            return
        contacts = session.query(Record).filter(Record.process_id == pid, Record.status == "unsent").all()
    else:
        if process.status in ["paused", "in progress", 'finished']:
            logger.warning(f"ID:{pid} => Program is already {process.status}")
            logger.warning(f"the `automail start {id}` command will start the program from the beginning")

            check = typer.confirm(f"Are you sure you want to start the program from the beginning?", default=False)
            if not check:
                logger.info(f"ID:{pid} => Program not started")
                return

        contacts = session.query(Record).filter(Record.process_id == pid).all()

    # get the password
    logger.info("Creating EmailSender obj...")
    if typer.confirm(f"Do you want to use the initial password for {sender_email}?", default=True):
        sender = EmailSender(cfg="config.cfg", user=sender_email)
    else:
        password = typer.prompt(f"Enter password for {sender_email}", hide_input=True)
        sender = EmailSender(cfg="config.cfg", user=sender_email, password=password)

    # Create a secure SSL context
    if temp_file:
        sender.set_template(temp_file)

    process.status = "in progress"
    session.commit()

    pause = False
    for contact in contacts:
        process = session.query(Process).filter(Process.id == pid).first()
        if process.status == "paused":
            logger.info(f"ID:{pid} => is paused by other process")
            session.close()
            engin.dispose()
            return
        logger.info(f"Sending email to: {contact.receiver}")
        sender.send(contact.receiver, subject, contact.data)
        contact.status = "sent"
        session.commit()
        logger.info(f"ID:{contact.id} => Email sent to {contact.receiver}")
        time.sleep(wait_time)

    process.status = "finished"
    session.commit()
    logger.info(f"ID:{pid} => Program finished successfully")


def _version_callback(value: bool) -> None:
    """Show the application's version and exit."""
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
            '<your-email>',
            "--email",
            "-e",
            help="Your email address.",
            prompt="Enter a default email address?",
        ),
        password: str = typer.Option(
            'None',
            "--password",
            "-p",
            help="Your email password.",
            hide_input=True,
            prompt="If you want to save the password of default email please enter your password"
                   " otherwise press enter to continue?",
        ),
        is_test: bool = typer.Option(
            False,
            "--test",
            "-t",
            help="Test output.",
        ),
) -> None:
    """Initialize the mail database."""
    logger = get_logger()
    if not shutil.os.path.exists(db_path):
        shutil.os.makedirs(db_path)
    elif not os.listdir(db_path):
        pass
    else:
        logger.error(f"Directory {db_path} already exists.")
        if shutil.os.path.exists(db_path + '/mail.db') and shutil.os.path.exists(db_path + '/config.cfg'):
            # delete the folder if it exists
            if typer.confirm(f"Do you want to delete {db_path} directory?", default=False):
                shutil.rmtree(db_path)
                logger.info(f"Deleting {db_path} directory...")
                time.sleep(0.5)
                shutil.os.mkdir(db_path)
            else:
                logger.info(f"Aborted!")
                raise typer.Exit(code=0)
        else:
            logger.error(f"This directory is not a previous automail project."
                         f" please choose another directory or project name.")
            raise typer.Exit(code=0)
    # create the database
    logger.info(f"Initializing {__app_name__} database...")
    os.chdir(db_path)
    session, engin = get_session()
    create_tables(engin)
    logger.info(f"Creating tables...")
    logger.info(f"Done!")

    # create the config file
    logger.info(f"Creating config file...")
    utils.create_config_file(
        smtp_server=smtp_server, smtp_port=smtp_port, password=password, sender_email=email, is_test=is_test
    )
    logger.info(f"Done!")
    logger.info(f"You can see and change the configuration file in the {os.path.abspath('./config.cfg')}!")

    os.chdir("../")
    session.close()
    engin.dispose()
    return


@app.command()
def register(
        email: str = typer.Option(
            "default(see config.cfg)",
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
            help="The body of your email.",
        ),

) -> None:
    """Register your email account."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
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
        if not os.path.exists(title):
            shutil.os.mkdir(title)
        else:
            logger.error(f"Directory {title} already exists. Please choose another title.")
            raise typer.Exit(code=0)

        shutil.copy(contact_list, title)
        contact_list = os.path.join(title, os.path.basename(contact_list))

        if attachment:
            shutil.copy(attachment, title)
            attachment = os.path.join(title, os.path.basename(attachment))
        if template:
            shutil.copy(template, title)
            template = os.path.join(title, os.path.basename(template))

        logger.info(f"Registering your email account...")
        if email == "default(see config.cfg)":
            email = get_config_dict()["user"]
        util.register_new_process(
            email=email,
            contact_list=contact_list,
            title=title,
            custom_pdf=custom_pdf,
            attachment=attachment,
            custom_pdf_dir=str(custom_pdf_dir),
            subject=subject,
            template=template,
        )

    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


@app.command()
def start(
        pid: Optional[int] = typer.Argument(
            None,
            help="The id of the process.",
        ),
) -> None:
    """Start sending emails."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Starting...")
        if pid is None:
            logger.error("Please enter the id of the process.")
            raise typer.Exit(code=0)
        else:
            run_process(pid=pid, is_resume=False)
    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


@app.command()
def resume(
        pid: Optional[int] = typer.Argument(
            None,
            help="The id of the process.",
        ),

) -> None:
    """Resume sending emails."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Resuming...")
        if pid is None:
            typer.secho("Please enter the id of the process.", fg=typer.colors.RED)
            raise typer.Exit(code=0)
        else:
            run_process(pid=pid, is_resume=True)
    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


@app.command()
def stop(
        pid: Optional[int] = typer.Argument(
            None,
            help="The id of the process.",
        ),
) -> None:
    """Stop a process."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Stopping...")
        if pid is None:
            logger.error("Please enter the id of the process.")
            raise typer.Exit(code=0)
        else:
            session, engin = get_session()
            process = session.query(Process).filter(Process.id == pid).first()
            if process is None:
                logger.error(f"Process with id {pid} does not exist.")
                session.close()
                engin.dispose()
                raise typer.Exit(code=0)
            if process.status == "in progress":
                process.status = "paused"
                session.commit()
                logger.info(f"ID: {pid} => Pausing the program.")
            else:
                logger.warning(f"ID: {pid} => Program is not in progress.")
            session.close()
            engin.dispose()
    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


@app.command()
def delete_process(
        pid: Optional[int] = typer.Argument(
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
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Deleting...")
        if pid is None:
            typer.secho("Please enter the id of the process.", fg=typer.colors.RED)
            raise typer.Exit(code=0)
        else:
            session, engin = get_session()

            process = session.query(Process).filter(Process.id == pid).first()
            if process is None:
                logger.error(f"Process with id {pid} does not exist.")
                raise typer.Exit(code=0)
            else:
                if dry_run:
                    logger.info(f"Process with id {pid} will be deleted.")
                else:
                    session.delete(process)
                    session.commit()
                    logger.info(f"Process with id {pid} has been deleted.")
                    shutil.rmtree(process.title)
            session.close()
            engin.dispose()
    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


@app.command()
def delete_record(
        rid: Optional[int] = typer.Argument(
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
    """Delete a record by ID."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Deleting...")
        if rid is None:
            logger.error("Please enter the id of the record.")
            raise typer.Exit(code=0)
        else:
            session, engin = get_session()
            record = session.query(Record).filter(Record.id == rid).first()
            if record is None:
                logger.error(f"Record with id {rid} does not exist.")
                raise typer.Exit(code=0)
            else:
                if dry_run:
                    logger.info(f"Record with id {rid} will be deleted.")
                else:
                    session.delete(record)
                    session.commit()
                    logger.info(f"Record with id {rid} has been deleted.")
            session.close()
            engin.dispose()
    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


@app.command("list")
def list_processes() -> None:
    """List all processes."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Listing...")
        session, engin = get_session()
        create_tables(engin)

        processes = session.query(Process).all()
        if len(processes) == 0:
            logger.warning("There is no process.")
        else:
            for process in processes:
                logger.info(f"ID: {process.id} | Title: {process.title} | Status: {process.status}")
        session.close()
        engin.dispose()


@app.command()
def list_records(
        process_id: Optional[int] = typer.Argument(
            None,
            help="The id of the process.",
        )) -> None:
    """List all records of one process."""
    logger = get_logger()
    if os.path.exists('./mail.db') and os.path.exists('./config.cfg'):
        logger.info("Listing...")
        session, engin = get_session()
        create_tables(engin)

        if process_id is None:
            records = session.query(Record).all()
        else:
            records = (
                session.query(Record).filter(Record.process_id == process_id).all()
            )
        if len(records) == 0:
            logger.warning("There is no record.")
        else:
            for record in records:
                logger.info(f"ID: {record.id} | Process ID: {record.process_id} | Email: {record.receiver} |"
                            f" Status: {record.status}"
                            )
        session.close()
        engin.dispose()
    else:
        logger.error("Please initialize the automail project first.")
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app(prog_name=__app_name__)
