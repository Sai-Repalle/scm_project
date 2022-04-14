"""Default configuration settings for the dynaconf"""
#scm/defaults_config.py 

import configparser
from pathlib import Path 

import typer 

from scm import (
    DIR_ERROR, 
    FILE_ERROR, 
    SUCCESS,
    __app_name__

)


CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "default.ini"

def _init_config_file() -> int: 
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError: 
        return DIR_ERROR
    try: 
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    

def init_app() -> int: 
    """Initialize the application.."""
    
    config_code = _init_config_file()
    
    if config_code != SUCCESS: 
        return config_code
    
    config = configparser.ConfigParser()
    sections = config.read(CONFIG_FILE_PATH)
    
    def_loc = sections['DEFAULTS']['config_loc']
    def_file = sections['DEFAULTS']['config_file']
    

    
    
    
    


