"""Main entry point for scm"""
from scm import cli, __app__name__ 

def main(): 
    cli.app(prog_name=__app__name__)
    
if __name__ == "__main__":
    main()