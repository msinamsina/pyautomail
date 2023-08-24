from typer.testing import CliRunner
import typer
import shutil
import os
from pyautomail import cli
from pyautomail.storage import get_session, Process, Record
from pyautomail.utils import get_config_dict
import pytest
import tempfile

runner = CliRunner()


@pytest.fixture(scope="module", autouse=True)
def setup():
    # create a temporary directory
    test_dir = tempfile.mkdtemp()
    os.chdir(test_dir)
    # initialize the pyautomail project
    runner.invoke(cli.app, ["init", "-db", "test-reg", "-ss", "smtp.gmail.com", "-sp", "111", "-t",
                            '-e', 'example@gmail.com'], input="y\n")

    # create a contact list
    with open("contact.csv", "w") as f:
        f.write("name,email\n")
        f.write("John Doe,john@gmail.com\n")
        f.write("Jane Doe,jane@gmail.com\n")
    # create a template
    with open("template.html", "w") as f:
        f.write("<h1>Hello {{ name }}!</h1>")

    # go to the project directory
    os.chdir("test-reg")

    assert get_config_dict()["user"] == "example@gmail.com"

    yield
    # remove the directory after the test
    os.chdir("../..")
    shutil.rmtree(test_dir, ignore_errors=True)


def test_register_1():
    """Test if there is no contactlist the error is raised"""
    result = runner.invoke(cli.app, ["register"])
    assert result.exit_code == 2
    assert "Error: Missing argument 'CONTACT_LIST'." in result.output


def test_register_2():
    """Test is the contactlist is not existed the error is rased"""
    try:
        os.remove("contact.csv")
    except FileNotFoundError:
        pass
    result = runner.invoke(cli.app, ["register", "contact.csv"])
    assert result.exit_code == 2
    assert "Error: Invalid value for 'CONTACT_LIST': Path 'contact.csv' does not exist." in result.output


def test_register_3():
    """Test a registration process"""

    shutil.rmtree("Contact List", ignore_errors=True)

    result = runner.invoke(cli.app, ["register", "../contact.csv"])
    assert result.exit_code == 0

    assert " => Registering Process example@gmail.com with contacts Contact List\\contact.csv" in result.output
    assert " => Registering record for john@gmail.com" in result.output
    assert " => Registering record for jane@gmail.com" in result.output
    assert os.path.exists("Contact List/contact.csv")

    # check the database
    # go to the Contact List folder
    session, engine = get_session()
    assert session.query(Process).filter(Process.title == "Contact List").count() == 1

    session.close()
    engine.dispose()

