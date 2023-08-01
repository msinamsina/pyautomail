from typer.testing import CliRunner
import shutil
import os
from automail import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_init_1():
    # check if the init command is working
    result = runner.invoke(cli.app, ["init"])
    assert result.exit_code == 0
    assert "Where do you want to initialize the automail project? [./]: " in result.stdout


def test_init_2():
    # enter a path that does not exist
    shutil.rmtree("test", ignore_errors=True)
    result = runner.invoke(cli.app, ["init"], input="test\n")
    assert result.exit_code == 0
    assert "Where do you want to initialize the automail project? [./]: " in result.stdout
    assert "Initializing automail database..." in result.stdout
    assert "Done!" in result.stdout
    assert os.path.exists("test") is True
    assert os.path.exists("test/mail.db") is True


def test_init_3():
    # enter a path that already exists and choose not to delete it
    result = runner.invoke(cli.app, ["init"], input="test\nn\n")
    assert result.exit_code == 0
    assert "Where do you want to initialize the automail project? [./]: " in result.stdout
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
    result = runner.invoke(cli.app, ["init"], input="test\ny\n")
    _helper_init(result)
    assert "Where do you want to initialize the automail project? [./]: " in result.stdout


def test_init_5():

    # enter a path that already exists and choose to delete it
    result = runner.invoke(cli.app, ["init", "--db-path", "test"], input="y\n")
    _helper_init(result)


def test_init_6():
    result = runner.invoke(cli.app, ["init", "-db", "test"], input="y\n")
    _helper_init(result)