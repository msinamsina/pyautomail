from typer.testing import CliRunner

from automail import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_init():
    result = runner.invoke(cli.app, ["init"])
    assert result.exit_code == 1
    assert "Where do you want to initialize the automail project? [./]: " in result.stdout
    # enter a path that does not exist
    result = runner.invoke(cli.app, ["init"], input="test\n")
    assert result.exit_code == 1
    assert "Directory test already exists." in result.stdout
    assert "Do you want to delete it? [y/N]: " in result.stdout
    # press enter to abort