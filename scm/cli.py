"""Module provides the CLI package"""
# scm/cli.py 

from distutils.log import ERROR
from typing import Optional 
import typer
from scm import ERRORS, __version__, __app__name__, default_config

app = typer.Typer() 

def _version(value: bool) -> None: 
    if value: 
        typer.echo(f"{__app__name__} - v{__version__}")
        raise typer.Exit() 

@app.command()
def init(
    file: str = typer.Option(
        str(default_config.CONFIG_FILE_PATH), 
        "--default-file", 
        "-f", 
        prompt="configuration file for configs"
    )
) -> None: 
    """Initialize the configuration file for the configuration"""
    app_init_error = default_config.init_app(file)
    
    if app_init_error:
        typer.secho(
            f'Creating the config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED 
        )
        raise typer.Exit(1)
    

@app.callback() 
def main(
    version: Optional[bool] = typer.Option(
        None, 
        "--version", 
        "-v", 
        help="Display's the application version",
        callback=_version, 
        is_eager=True,
        ) 
    ) -> None: 
    return 0  
