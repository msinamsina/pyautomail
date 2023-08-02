from typer.testing import CliRunner
import shutil
import os
from automail import cli


runner = CliRunner()


def usual_output(result):
    assert result.exit_code == 0
    assert "Where do you want to initialize the automail project? [./automail-workspace]: " in result.stdout
    assert "What is your smtp server? [smtp.gmail.com]: " in result.stdout
    assert "What is your smtp port? [465]: " in result.stdout


def test_init_1():
    # check if the init command is working
    result = runner.invoke(cli.app, ["init"])
    print(result.stdout)
    usual_output(result)


def test_init_2():
    # enter a path that does not exist
    shutil.rmtree("test", ignore_errors=True)
    result = runner.invoke(cli.app, ["init"], input="test")
    usual_output(result)
    assert "Initializing automail database..." in result.stdout
    assert "Done!" in result.stdout
    assert os.path.exists("test") is True
    assert os.path.exists("test/mail.db") is True
    with open("test/config.cfg") as f:
        config = f.read()
    assert "[smtp]\nserver = smtp.gmail.com\nport = 465\nis_test = False\n\n[account]\nuser = \npassword = \n" == config


def test_init_3():
    # enter a path that already exists and choose not to delete it
    result = runner.invoke(cli.app, ["init"], input="test")
    usual_output(result)
    assert "Directory test already exists." in result.stdout
    assert "Do you want to delete it? [y/N]: " in result.stdout
    assert "Initializing automail database..." not in result.stdout
    assert "Aborted!" in result.stdout


def _helper_init(result):
    assert result.exit_code == 0
    assert "Directory test already exists." in result.stdout
    assert "Do you want to delete it? [y/N]: " in result.stdout
    assert "Deleting..." in result.stdout
    assert "Initializing automail database..." in result.stdout
    assert "Done!" in result.stdout

    assert os.path.exists("test") is True
    assert os.path.exists("test/mail.db") is True


def test_init_4():
    # enter a path that already exists and choose to delete it
    result = runner.invoke(cli.app, ["init"], input="test\n\n\ny")
    _helper_init(result)
    usual_output(result)


def test_init_5():

    # enter a path that already exists and choose to delete it
    result = runner.invoke(cli.app, ["init", "--db-path", "test"], input="\n\ny")
    _helper_init(result)
    assert "What is your smtp server? [smtp.gmail.com]: " in result.stdout
    assert "What is your smtp port? [465]: " in result.stdout


def test_init_6():
    result = runner.invoke(cli.app, ["init", "-db", "test"], input="\n\ny")
    _helper_init(result)
    assert "What is your smtp server? [smtp.gmail.com]: " in result.stdout
    assert "What is your smtp port? [465]: " in result.stdout


def test_init_7():
    result = runner.invoke(cli.app, ["init", "-db", "test", "-ss", "smtp.server.com"], input="\ny\n")
    _helper_init(result)
    assert "What is your smtp port? [465]: " in result.stdout
    with open("test/config.cfg") as f:
        config = f.read()
    assert "[smtp]\nserver = smtp.server.com\nport = 465\nis_test = False\n\n[account]\nuser = \npassword = \n" == config


def test_init_8():
    result = runner.invoke(cli.app, ["init", "-db", "test", "-ss", "smtp.gmail.com", "-sp", "111"], input="y\n")
    _helper_init(result)
    with open("test/config.cfg") as f:
        config = f.read()
    assert "[smtp]\nserver = smtp.gmail.com\nport = 111\nis_test = False\n\n[account]\nuser = \npassword = \n" == config


def test_init_9():
    result = runner.invoke(cli.app, ["init", "-db", "test", "-ss", "smtp.gmail.com", "-sp", "111", "-t"], input="y\n")
    _helper_init(result)
    with open("test/config.cfg") as f:
        config = f.read()
    assert "[smtp]\nserver = smtp.gmail.com\nport = 111\nis_test = True\n\n[account]\nuser = \npassword = \n" == config
