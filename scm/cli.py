"""Module provides the CLI package"""
# scm/cli.py 
import os
import sys
import logging  
from distutils.log import ERROR
from typing import Optional
from ordered_set import OrderedSet 
import typer
from scm import ERRORS, __version__, __app_name__, default_config
from scm.default_config import read_json,create_def_directory, create_def_files, get_diff_hash_res,check_if_receipe_exists, get_user_settings, get_user_defined_resources, validate_unsupported_resources, gen_command
from typing import List, Set, Dict
from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox
from dynaconf.vendor.toml.decoder import TomlDecodeError
from ordered_set import OrderedSet
import json
import hashlib
from deepdiff import DeepDiff
from deepdiff.model import PrettyOrderedSet
from scm import defaults 

#BASIC LOGGING MESSAGE
logging.basicConfig(format='[%(levelname)s][%(asctime)s]::%(message)s',
                    datefmt="%m-%d-%Y %H:%M:%S", level=logging.INFO)
logger = logging.getLogger()

# Global variables 
def_settings_dict = {}

app = typer.Typer() 

def _version(value: bool) -> None: 
    if value: 
        typer.echo(f"{__app_name__} - v{__version__}")
        raise typer.Exit() 

@app.command()
def init(
    file: str = typer.Option(
        str(default_config.CONFIG_FILE_PATH), 
        "--default-file", 
        "-f"
    )
) -> None:
    global def_settings_dict 
    
    def_settings_dict = read_json(file)['default'] 
    
    os.environ['ROOT_PATH_FOR_DYNACONF'] = def_settings_dict.get(
                    'CONFIG_DIR', os.path.join(os.getcwd(), "config"))
    
    is_dir_created = create_def_directory(def_settings_dict)
    
    if not is_dir_created: 
        logging.warning("default directories creation failed")
        raise typer.Exit()
    
    is_files_created = create_def_files(def_settings_dict)
    
    if not is_files_created:
        logging.warning("default files creation failed")
        raise typer.Exit()
        
    return 0 
    
# create command 
@app.command()
def create(
    receipe: str = typer.Option(...),
    force: bool = typer.Option(False)
) -> None: 
         
    init(default_config.CONFIG_FILE_PATH)
    con_dir, def_file = def_settings_dict.get('CONFIG_DIR'), f"{receipe}.toml"
    con_dir_full = os.path.join(os.getcwd(), con_dir)
    def_file_full = os.path.join(con_dir_full, def_file)
    
    if not check_if_receipe_exists(receipe) or force:
        with open(def_file_full, mode="w") as f:
            f.write(f"# Place holder for creating the scm {receipe} receipe")
    else:
        logging.warning(
            f"`{receipe}` configuration file exists, use --force to override.")
        raise typer.Exit()
    
    return 0 
  
    
@app.command()
def info(
    receipe: str = typer.Option(...)
    ) -> None:
    
    init(default_config.CONFIG_FILE_PATH)
    con_dir, def_file = def_settings_dict.get('CONFIG_DIR'), f"{receipe}.toml"
    con_dir_full = os.path.join(os.getcwd(), con_dir)
    def_file_full = os.path.join(con_dir_full, def_file)
    
    if not check_if_receipe_exists(receipe):
        logging.warning(f"receipe {receipe} doesn't exist in the config directory")
        logging.warning("use `scm create` for the receipe creation")
        raise typer.Exit()
    
    user_settings = get_user_settings(receipe)
    user_resources = get_user_defined_resources(user_settings)

    for res in user_resources: 
        if res in user_settings: 
            for i in user_settings[res]:
                logging.info(f"{res}.{i} - {user_settings[res][i]}")

    return 0 

#validate command 
@app.command()
def validate(
    receipe: str = typer.Option(...)
) -> None:
    
    init(default_config.CONFIG_FILE_PATH)
    con_dir, def_file = def_settings_dict.get('CONFIG_DIR'), f"{receipe}.toml"
    con_dir_full = os.path.join(os.getcwd(), con_dir)
    def_file_full = os.path.join(con_dir_full, def_file)
    
    if not check_if_receipe_exists(receipe):
        logging.warning(f"receipe {receipe} doesn't exist in the config directory")
        logging.warning("use `scm create` for the receipe creation")
        raise typer.Exit()
    
    res_validation = validate_unsupported_resources(get_user_settings(receipe))
    
    if res_validation:
        logging.warning(
            f"Unsupported resources found in the `{receipe}` configuration file"
        )
        for i in res_validation:
            logging.warning(
                f"`{i}` resource in {receipe} receipe isn't supported")
            raise typer.Exit()

    user_settings = get_user_settings(receipe)
    user_resources = get_user_defined_resources(user_settings)

    if not user_resources:
        logging.warning(
            f"No user resources found in the `{receipe}` configuration file")
        raise typer.Exit()

    for res in user_resources:
        if res in user_settings:
            for i in user_settings[res]:

                if not isinstance(user_settings[res][i], DynaBox):
                    logging.warning(
                        f"Missing subconfig `{res}` resource in {receipe} receipe"
                    )
                    raise typer.Exit()

                if not user_settings[res][i].get('name', None):
                    logging.warning(
                        f"Missing `name`attributes in resource `{i}` in receipe {receipe}"
                    )
                    raise typer.Exit()

                if not user_settings[res][i].get('action', None):
                    logging.warning(
                        f"Missing `action` attributes in resource `{i}` in receipe {receipe}"
                    )
                    raise typer.Exit()

                defaults.UNSUPPORTED_ATTR = OrderedSet(
                    user_settings[res][i].keys()) - defaults.RES_ATTRIBUTES

                if (defaults.UNSUPPORTED_ATTR - defaults.SRV_ATTRIBUTES) and res.upper() == "SERVICE":
                    logging.warning(
                        f"Found one more attributes that aren't supported"
                    )
                    for unsup in (defaults.UNSUPPORTED_ATTR - defaults.SRV_ATTRIBUTES):
                        logging.warning(
                            f"`{unsup}` not supported attribute in resource {res} in receipe {receipe}"
                        )
                    raise typer.Exit()

                if (defaults.UNSUPPORTED_ATTR - defaults.DIR_ATTRIBUTES) and res.upper() == "DIRECTORY":
                    logging.warning(
                        f"Found one more attributes that aren't supported"
                    )
                    for unsup in (defaults.UNSUPPORTED_ATTR - defaults.DIR_ATTRIBUTES):
                        logging.warning(
                            f"`{unsup}` not supported attribute in resource {res} in receipe {receipe}"
                        )
                    raise typer.Exit()

                if (defaults.UNSUPPORTED_ATTR - defaults.FILE_ATTRIBUTES) and res.upper() == "FILE":
                    logging.warning(
                        f"Found one more attributes that aren't supported"
                    )
                    for unsup in (defaults.UNSUPPORTED_ATTR - defaults.FILE_ATTRIBUTES):
                        logging.warning(
                            f"`{unsup}` not supported attribute in resource {res} in receipe {receipe}"
                        )
                    raise typer.Exit()

                # now validate the values from the user-input string
                user_values = user_settings[res][i].get('action', None)
                if res.upper() == "SERVICE":
                    for val in user_values:
                        if val not in defaults.SERVICE_SETUP_ACTIONS.union(
                                defaults.SERVICE_OP_ACTIONS):
                            logging.warning(
                                f"`{val}` not supported in action attribute in resource {res} in receipe {receipe}"
                            )

                else:
                    if res.upper() in ["FILE", "DIRECTORY"]:
                        for val in user_values:
                            if val not in defaults.DIR_FILE_ACTIONS:
                                logging.warning(
                                    f"`{val}` not supported in action attribute in resource {res} in receipe {receipe}"
                                )

    logging.info(f"{receipe} receipe file is valid for push, use `scm push` to push the file")
    return 0
 
#push command 
@app.command()
def push(
    receipe: str = typer.Option(...)
) -> None:
    output = []
    
    settings = read_json(default_config.CONFIG_FILE_PATH)['default'] 
    
    os.environ['ROOT_PATH_FOR_DYNACONF'] = settings.get(
                    'CONFIG_DIR', os.path.join(os.getcwd(), "config"))

    hash_config_dir = os.path.join(settings.get('CONFIG_HASH_DIR'),settings.get('CONFIG_HASH_FILE'))
    
    validate(receipe)
    
    user_settings = get_user_settings(receipe)
    user_resources = get_user_defined_resources(user_settings)
    
    for i in user_resources: 
        gen_command(user_settings,i,output)
    
    logging.info(output)
    
    return 0     

#diff command 
@app.command()
def diff (
    receipe: str = typer.Option(...)
) -> None:
    settings = read_json(default_config.CONFIG_FILE_PATH)['default'] 
    
    os.environ['ROOT_PATH_FOR_DYNACONF'] = settings.get(
                    'CONFIG_DIR', os.path.join(os.getcwd(), "config"))

    hash_config_dir = os.path.join(settings.get('CONFIG_HASH_DIR'),settings.get('CONFIG_HASH_FILE'))
    
    validate(receipe)
    
    diff = get_diff_hash_res(receipe, hash_config_dir)
    user_settings = get_user_settings(receipe)
    
    logging.info("Following changes will be applied to the configuration")
    for i in diff:
        logging.info(f"{i} - {user_settings[i.split('.')[0]][i.split('.')[1]]}")
    
    return 0


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