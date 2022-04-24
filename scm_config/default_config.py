"""Default configuration settings for the dynaconf"""
# scm/defaults_config.py
import os
import logging
from typing import List, Set, Dict
from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox
from dynaconf.vendor.toml.decoder import TomlDecodeError
from ordered_set import OrderedSet
import json
import hashlib
import shlex 
from deepdiff import DeepDiff
from deepdiff.model import PrettyOrderedSet
from json.decoder import JSONDecodeError
from scm_config.defaults import JSON_DIFF_ATTR
from pathlib import Path
from scm_config import defaults
from subprocess import STDOUT, check_call, CalledProcessError

from scm_config import (
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
    __app_name__

)

CONFIG_DIR = OrderedSet(['CONFIG_DIR', 'CONFIG_HASH_DIR'])
CONFIG_FILES = OrderedSet(['CONFIG_DEF_FILE', 'CONFIG_HASH_FILE'])
CONFIG_DIR_PATH = os.getcwd()
CONFIG_FILE_PATH = os.path.join(
    CONFIG_DIR_PATH,
    "settings.json")


def read_json(filename):
    try:
        with open(filename) as file:
            logging.info(f"Reading the Json configuration {filename}")
            try:
                return dict(json.load(file))
            except JSONDecodeError:
                logging.warning(f"Invalid JSON file {file}")
                return FILE_ERROR
    except FileNotFoundError:
        logging.ERROR(f"File {filename} not found")
        return FILE_ERROR


def create_def_directory(user_dict) -> bool:
    for key in CONFIG_DIR:
        logging.info(f"creating directory {key}")
        if user_dict.get(key, None):
            if not os.path.exists(user_dict[key]):
                os.mkdir(user_dict[key])
            else:
                logging.info(f"{key} directory already exists")
        else:
            logging.warning(f"Missing {key} value to create the directories")
            return False
    return True


def create_def_files(user_dict) -> bool:
    for key in CONFIG_FILES:
        logging.info(f"creating files {key}")
        if user_dict.get(key, None):
            if not os.path.exists(user_dict[key]):
                if key == "CONFIG_DEF_FILE":
                    Path(
                        os.path.join(
                            user_dict['CONFIG_DIR'],
                            user_dict[key])).touch()
                else:
                    hash_directory = os.path.join(
                            user_dict['CONFIG_HASH_DIR'],
                            user_dict[key])
                    if not os.path.exists(hash_directory):
                        Path(hash_directory).touch()
                        #write empty json dict to the file 
                        d = {}
                        # Serializing json 
                        json_object = json.dumps(d, indent = 4)
                        # Writing to sample.json
                        with open(os.path.join(
                                user_dict['CONFIG_HASH_DIR'],
                                user_dict[key]), "w") as outfile:
                            outfile.write(json_object)
            else:
                logging.info(f"{key} file already exists")
        else:
            logging.warning(f"Missing {key} value to create the files")
            return False

    return True


def check_if_receipe_exists(receipe) -> bool:
    return os.path.exists(
        os.path.join(os.getcwd(), os.environ['ROOT_PATH_FOR_DYNACONF'],
                     f"{receipe}.toml"))


def get_user_settings(receipe, validator=None, environments=True) -> Dict:
    return Dynaconf(settings_files=[f"{receipe}.toml"], validators=validator)


def get_user_defined_resources(settings) -> Set:
    return (OrderedSet([*settings]) - defaults.DEFAULT_PARAMTERS)


def validate_unsupported_resources(user_resources) -> Set:
    unsupported_resources = (
        {*user_resources} - defaults.DEFAULT_PARAMTERS) - defaults.SUPP_RES
    return unsupported_resources


def gen_command(
        settings_dict: Dict,
        key: str,
        output: List) -> None:
    """Function to the generate the OS commands by reading the settings_dict and update the input list format"""
    if key.upper() in ["SERVICE"]:
        for index, value in settings_dict[key].items():
            output[f"{key}.{index}"] = []
            if isinstance(
                    value, DynaBox) and index != "params":
                for n in value['name']:
                    for act in value['action']:
                        if act in defaults.SERVICE_SETUP_ACTIONS:
                            output[f"{key}.{index}"].append("sudo apt-get update -y")
                            output[f"{key}.{index}"].append(f"sudo apt-get {act} {n} -y")
                        else:
                            if act in defaults.SERVICE_OP_ACTIONS:
                                output[f"{key}.{index}"].append(f"systemctl {act} {n}")
                                
    if key.upper() in ["DIRECTORY", "FILE"]:
        for index, value in settings_dict[key].items():
            output[f"{key}.{index}"] = []
            for n in value['name']:
                for act in value['action']:
                    if act == "create" and value.get('content',None):
                        for i in value['content']:
                            if not value.get('override',None):
                                cmd: str = f"echo '{i}' >> {n}"
                            else:
                                cmd:str = f"echo '{i}' > {n}"
                            output[f"{key}.{index}"].append(cmd)

                    if act == "create" and key == "DIRECTORY":
                        cmd: str = f"mkdir -p {n}"
                        output[f"{key}.{index}"].append(cmd)

                    if act == "create" and value['params'].get(
                            'owner',
                            None) and value['params'].get(
                            'group',
                            None):
                        cmd: str = f"chown {value['params']['owner']}:{value['params']['group']} {n}"
                        if value['params'].get('recurse', None) and json.loads(
                                (value['params'].get('recurse', None)).lower()):
                            cmd += " -R"

                        output[f"{key}.{index}"].append(cmd)


                if value.get('notifies', None):
                    inp_json = json.loads(
                        value.get(
                            'notifies',
                            None).replace(
                            "\'",
                            "\""))
                    for n in inp_json['name']:
                        for act in inp_json['action']:
                            if act == "install":
                                output[f"{key}.{index}"].append(f"apt-get {act} {n} -y")
                            else:
                                output[f"{key}.{index}"].append(f"systemctl {act} {n}")

    if key.upper() in ["FIREWALL"]:
        for index, value in settings_dict[key].items():
            output[f"{key}.{index}"] = []
            for n in value['name']:
                for act in value['action']:
                    if act == "allow":
                        cmd: str = f"sudo ufw {act} in {n}"
                        output[f"{key}.{index}"].append(cmd)
                        
                        
    return None



def _hash_fun(user_dict: Dict) -> str:
    user_dict = json.dumps(user_dict, sort_keys=True)
    return hashlib.md5(user_dict.encode('utf-8')).hexdigest()


def _write_json(new_data, filename) -> None:
    with open(filename, 'w') as file:
        filedata = json.load(new_data)
        print(filedata)
        filedata.update(new_data)
        file.seek(0)
        json.dump(filedata, file, indent=4)


def _read_json(filename) -> Dict:
    f = open(filename)
    try:
        dict_output = json.load(f)
    except Exception as e:
        return None
    return dict_output 

def _get_diff_hash(existing_hash, curr_hash) -> List:
    output = []
    if existing_hash:
        res = DeepDiff(curr_hash, existing_hash)
        for i in JSON_DIFF_ATTR:
            if res.get(i, None):
                for split_val in res.get(i, None):
                    first_idx = split_val.find('[')
                    last_idx = split_val.find(']')
                    split_val = split_val[first_idx+1:last_idx]
                    output.append(split_val.replace("'",""))

    else:
        output = (list(curr_hash.keys()))
        
    return output


def get_diff_hash_res(receipe, hash_config) -> List:

    user_settings = dict(get_user_settings(receipe))
    user_resources = get_user_defined_resources(user_settings)
    data = {f"{receipe}": []}
    hash_dict = {}

    existing_hash = _read_json(hash_config)

    for res in user_resources:
        if res in user_settings:
            for i, value in user_settings[res].items():
                print(value)
                hash_val = _hash_fun(value)
                hash_dict[f"{res}.{i}"] = hash_val
    
    data[f"{receipe}"] = [hash_dict]
    print(existing_hash)
    print(data)

    diff_resources = _get_diff_hash(existing_hash, data, receipe)

    return diff_resources


# write configuration to the build hash set
def write_hash_config(hash_dict_set, receipe, hash_file_name):
    output = {}
    user_settings = dict(get_user_settings(receipe))
    user_resources = get_user_defined_resources(user_settings)

    for res in user_resources:
        if res in user_settings:
            for key, val in user_settings[res].items():
                valid_con = f"{res}.{key}"
                if valid_con in hash_dict_set:
                    output[key] = dict(val)
    return {receipe: output}


def run_os_command(command) -> None: 
    try: 
        commands = shlex.split(command)
        if commands[0] == "echo":
            if commands[2] == ">>":
                f = open(commands[-1], mode="a")
            else:
                f = open(commands[-1], mode="w")
            code = check_call(commands[:2], stderr=STDOUT, stdout=f)
        else:            
            code = check_call(commands, stderr=STDOUT) 
    except CalledProcessError as e:
        logging.error(str(e))
        code = 1 
    return code 


