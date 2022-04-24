"""Main entry point for scm"""
from scm_config import cli, __app_name__ 

def main_cli(): 
    cli.app(prog_name=__app_name__)
    
if __name__ == "__main__":
    main_cli()