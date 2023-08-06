from typer.testing import CliRunner
import typer
import shutil
import os
from automail import cli
from automail.storage import get_session, Process, Record
import pytest
import tempfile
import time

runner = CliRunner()


@pytest.fixture(scope="module", autouse=True)
def setup():
    # create a temporary directory
    test_dir = tempfile.mkdtemp()
    os.chdir(test_dir)
    # initialize the automail project
    runner.invoke(cli.app, ["init", "-db", "test-reg", "-ss", "smtp.gmail.com", "-sp", "111", "-t"], input="y\n")

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

    # register the contact list
    runner.invoke(cli.app, ["register", "../contact.csv", "-t", '../template.html'])

    yield
    # remove the directory after the test
    os.chdir("../..")
    # shutil.rmtree(test_dir)


def test_start_1():
    """Test if the process is started"""
    result = runner.invoke(cli.app, ["start"])
    assert result.exit_code == 0
    assert "Please enter the id of the process." in result.output


def test_start_2():
    """Test if the process is started"""
    result = runner.invoke(cli.app, ["start", "1"], input="y\n")
    assert result.exit_code == 0
    assert "Starting..." in result.output
    # assert "Process 1 is finished." in result.output
    assert "Sending email to: john@gmail.com" in result.output
    assert "<h1>Hello John Doe!</h1>" in result.output
    assert "Sending email to: jane@gmail.com" in result.output
    assert "<h1>Hello Jane Doe!</h1>" in result.output
    assert "Program finished successfully" in result.output

