from typer.testing import CliRunner
import typer
import shutil
import os
from pyautomail import cli
from pyautomail.storage import get_session, Process, Record
import pytest
import tempfile
import time
import re

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
    result = runner.invoke(cli.app, ["register", "../contact.csv", "-t", '../template.html'])
    print(result)
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


def test_list():
    """Test if the process is listed"""
    result = runner.invoke(cli.app, ["list"])
    assert result.exit_code == 0
    assert re.search(r"ID: * | Title: * | Status: .*", result.output) is not None


def test_stop_1():
    """Test if the process is stopped"""
    result = runner.invoke(cli.app, ["stop"])
    assert result.exit_code == 0
    assert "Please enter the id of the process." in result.output


def test_stop_2():
    """Test if the process is stopped"""
    result = runner.invoke(cli.app, ["stop", "134"], input="y\n")
    assert result.exit_code == 0
    assert "Process with id 134 does not exist." in result.output


def test_stop_3():
    """Test if the process is stopped"""
    result = runner.invoke(cli.app, ["stop", "1"], input="y\n")
    assert result.exit_code == 0
    assert "Program is not in progress." in result.output


def test_stop_4():
    """Test if the process is stopped"""
    result = runner.invoke(cli.app, ["register", "../contact.csv", "-t", '../template.html', "--title", "sasa"])
    id = re.findall(r"ID: \d+ => Registering Process", result.output)[0].split(" ")[1]
    session, engine = get_session()
    process = session.query(Process).filter_by(id=id).first()
    process.status = "in progress"
    session.commit()
    result = runner.invoke(cli.app, ["stop", f"{process.id}"], input="y\n")
    assert result.exit_code == 0
    assert "Stopping..." in result.output
    assert f"ID: {process.id} => Pausing the program." in result.output


def test_delete_record():
    """Test if the record is deleted"""
    session, engine = get_session()
    record = session.query(Record).first()

    result = runner.invoke(cli.app, ["delete-record", f"{record.id}"], input="y\n")
    assert result.exit_code == 0
    assert "Record with id 1 has been deleted." in result.output

    record = session.query(Record).filter_by(id=record.id).first()
    assert record is None


def test_delete_process():
    """Test if the process is deleted"""
    session, engine = get_session()
    process = session.query(Process).first()

    result = runner.invoke(cli.app, ["delete-process", f"{process.id}"], input="y\n")
    assert result.exit_code == 0
    assert "Process with id 1 has been deleted." in result.output

    process = session.query(Process).filter_by(id=process.id).first()
    assert process is None
