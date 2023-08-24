import pytest
from pyautomail.manager import main


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    try:
        main([option])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    print(output)
    assert "usage: pyautomail [-h] {init,register,start,stop,resume,list}" in output


@pytest.mark.parametrize("option", ("register", "start", "stop", "resume", "list"))
def test_subcommand_help(capsys, option):
    try:
        main([option, "-h"])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    print(output)
    assert f"usage: pyautomail {option} [-h]" in output
