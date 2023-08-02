import pytest
from automail.manager import main


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    try:
        main([option])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    print(output)
    assert "usage: automail [-h] {init,register,start,stop,resume,list}" in output


@pytest.mark.parametrize("option", ("register", "start", "stop", "resume", "list"))
def test_subcommand_help(capsys, option):
    try:
        main([option, "-h"])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    print(output)
    assert f"usage: automail {option} [-h]" in output


@pytest.mark.parametrize("option", ("register",))
def test_register(capsys, option):
    main([option, "youremail@gmail.com",  "../contact.csv"])

    output = capsys.readouterr().out
    print(output)
    assert "=> Registering user youremail@gmail.com with contacts ../contact.csv" in output
