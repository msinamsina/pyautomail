from typer.testing import CliRunner
import shutil
import os
from automail import cli
from automail.storage import get_session, Process, Record

runner = CliRunner()


def _usual_output():
    pass


def test_register_1():
    result = runner.invoke(cli.app, ["register"])
    assert result.exit_code == 2
    assert "Error: Missing argument 'CONTACT_LIST'." in result.output


def test_register_2():
    try:
        os.remove("contact.csv")
    except FileNotFoundError:
        pass
    result = runner.invoke(cli.app, ["register", "contact.csv"])
    assert result.exit_code == 2
    assert "Error: Invalid value for 'CONTACT_LIST': Path 'contact.csv' does not exist." in result.output


def test_register_3():

    shutil.rmtree("Contact List", ignore_errors=True)
    with open("contact.csv", "w") as f:
        f.write("name,email\n")
        f.write("John Doe,john@gmail.com\n")
        f.write("Jane Doe, jane@gmail.com\n")

    result = runner.invoke(cli.app, ["register", "contact.csv"])
    assert result.exit_code == 0
    assert " => Registering user  with contacts Contact List\\contact.csv" in result.output
    assert " => Registering record for john@gmail.com" in result.output
    assert " => Registering record for jane@gmail.com" in result.output
    assert os.path.exists("Contact List/contact.csv")

    # check the database
    # go to the Contact List folder
    session, engine = get_session()
    assert session.query(Process).filter(Process.title == "Contact List").count() == 1

    session.close()
    engine.dispose()

