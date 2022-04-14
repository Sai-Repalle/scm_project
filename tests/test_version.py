from typer.testing import CliRunner 
from scm import __app__name__, __version__, cli 

test_runner = CliRunner()

def test_version():
    result = test_runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0 
    assert f"{__app__name__} - v{__version__}\n" in result.stdout 
    