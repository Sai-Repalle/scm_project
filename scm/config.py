import os
import logging
from typing import List, Set, Dict
from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox
from dynaconf.vendor.toml.decoder import TomlDecodeError
from ordered_set import OrderedSet
import json
import hashlib
from deepdiff import DeepDiff
from deepdiff.model import PrettyOrderedSet

logging.basicConfig(format='[%(levelname)s][%(asctime)s]::%(message)s',
                    datefmt="%m-%d-%Y %H:%M:%S")
logger = logging.getLogger()
supp_res = OrderedSet(['SERVICE', 'FILE', 'DIRECTORY'])
service_setup_actions = OrderedSet(["install", "enable", "disable"])
service_op_actions = OrderedSet(
    ["stop", "start", "restart", "reload", "disable", "enable"])
dir_file_actions = OrderedSet(['create'])
res_attributes = OrderedSet(['name', 'action'])
srv_attributes = OrderedSet(['name', 'action', 'notifies'])
dir_attributes = OrderedSet(['params', 'notifies'])
file_attributes = OrderedSet(['params', 'notifies', 'content'])
json_diff_attr = OrderedSet(
    ['dictionary_item_added', 'dictionary_item_removed', 'values_changed'])


os.environ['ROOT_PATH_FOR_DYNACONF'] = "./my_configuration"
hash_file = "hash_config.md5.json"
hash_configuration = os.path.join(
    os.environ['ROOT_PATH_FOR_DYNACONF'], hash_file)


default_paramters = OrderedSet([
    'SETTINGS_FILE_FOR_DYNACONF', 'RENAMED_VARS', 'ROOT_PATH_FOR_DYNACONF',
    'ENVIRONMENTS_FOR_DYNACONF', 'MAIN_ENV_FOR_DYNACONF',
    'LOWERCASE_READ_FOR_DYNACONF', 'ENV_SWITCHER_FOR_DYNACONF',
    'ENV_FOR_DYNACONF', 'FORCE_ENV_FOR_DYNACONF', 'DEFAULT_ENV_FOR_DYNACONF',
    'ENVVAR_PREFIX_FOR_DYNACONF', 'IGNORE_UNKNOWN_ENVVARS_FOR_DYNACONF',
    'ENCODING_FOR_DYNACONF', 'MERGE_ENABLED_FOR_DYNACONF',
    'NESTED_SEPARATOR_FOR_DYNACONF', 'ENVVAR_FOR_DYNACONF',
    'REDIS_FOR_DYNACONF', 'REDIS_ENABLED_FOR_DYNACONF', 'VAULT_FOR_DYNACONF',
    'VAULT_ENABLED_FOR_DYNACONF', 'VAULT_PATH_FOR_DYNACONF',
    'VAULT_MOUNT_POINT_FOR_DYNACONF', 'VAULT_ROOT_TOKEN_FOR_DYNACONF',
    'VAULT_KV_VERSION_FOR_DYNACONF', 'VAULT_AUTH_WITH_IAM_FOR_DYNACONF',
    'VAULT_AUTH_ROLE_FOR_DYNACONF', 'VAULT_ROLE_ID_FOR_DYNACONF',
    'VAULT_SECRET_ID_FOR_DYNACONF', 'CORE_LOADERS_FOR_DYNACONF',
    'LOADERS_FOR_DYNACONF', 'SILENT_ERRORS_FOR_DYNACONF',
    'FRESH_VARS_FOR_DYNACONF', 'DOTENV_PATH_FOR_DYNACONF',
    'DOTENV_VERBOSE_FOR_DYNACONF', 'DOTENV_OVERRIDE_FOR_DYNACONF',
    'INSTANCE_FOR_DYNACONF', 'YAML_LOADER_FOR_DYNACONF',
    'COMMENTJSON_ENABLED_FOR_DYNACONF', 'SECRETS_FOR_DYNACONF',
    'INCLUDES_FOR_DYNACONF', 'PRELOAD_FOR_DYNACONF', 'SKIP_FILES_FOR_DYNACONF',
    'DYNACONF_NAMESPACE', 'NAMESPACE_FOR_DYNACONF', 'DYNACONF_SETTINGS_MODULE',
    'DYNACONF_SETTINGS', 'SETTINGS_MODULE', 'SETTINGS_MODULE_FOR_DYNACONF',
    'PROJECT_ROOT', 'PROJECT_ROOT_FOR_DYNACONF', 'DYNACONF_SILENT_ERRORS',
    'DYNACONF_ALWAYS_FRESH_VARS', 'BASE_NAMESPACE_FOR_DYNACONF',
    'GLOBAL_ENV_FOR_DYNACONF'])


def check_if_receipe_exists(receipe) -> bool:
    return os.path.exists(
        os.path.join(os.getcwd(), os.environ['ROOT_PATH_FOR_DYNACONF'],
                     f"{receipe}.toml"))


def validate_unsupported_resources(user_resources) -> Set:
    global default_paramters, supp_res
    unsupported_resources = ({*user_resources} - default_paramters) - supp_res
    return unsupported_resources


def get_user_settings(receipe, validator=None, environments=True) -> Dict:
    return Dynaconf(settings_files=[f"{receipe}.toml"], validators=validator)


def get_user_defined_resources(settings) -> Set:
    return (OrderedSet([*settings]) - default_paramters)


def create(receipe) -> None:
    """creates the configuration file based on the input"""
    con_dir, def_file = os.environ['ROOT_PATH_FOR_DYNACONF'], f"{receipe}.toml"
    con_dir_full = os.path.join(os.getcwd(), con_dir)
    def_file_full = os.path.join(con_dir_full, def_file)

    if not os.path.isdir(con_dir_full):
        os.mkdir(con_dir_full)

    if not check_if_receipe_exists(receipe):
        with open(def_file_full, mode="w") as f:
            f.write("# This is the chef receipe that I created the file")
    else:
        logging.warning(
            f"`{receipe}` configuration file exists, use --force to override.")


def _hash_fun(user_dict: Dict) -> str:
    user_dict = json.dumps(user_dict, sort_keys=True)
    return hashlib.md5(user_dict.encode('utf-8')).hexdigest()


def _write_json(new_data, filename) -> None:
    with open(filename, 'w') as file:
        filedata = json.load(f)
        filedata.update(new_data)
        file.seek(0)
        json.dump(filedata, file, indent=4)


def _read_json(filename) -> Dict:
    f = open(filename)
    try:
        dict_output = json.load(f)
    except Exception as e:
        return None


def _get_diff_hash(existing_hash, curr_hash, receipe) -> List:
    output = []
    if existing_hash:
        res = DeepDiff(curr_hash, existing_hash)
        for i in json_diff_attr:
            if res.get(i, None):
                if isinstance(res.get(i, None), PrettyOrderedSet):
                    for val in res.get(i, None):
                        split_val = val.split('[0]')[1]
                        if split_val[0] == '[' and split_val[-1] == "]":
                            split_val = split_val[1:-1]
                        output.append(split_val.strip("\'"))

    else:
        for i in curr_hash[receipe]:
            output += list(i.keys())
    return output


def get_diff_hash_res(receipe) -> List:

    user_settings = dict(get_user_settings(receipe))
    user_resources = get_user_defined_resources(user_settings)
    data = {f"{receipe}": []}
    hash_dict = {}

    existing_hash = _read_json(hash_configuration)

    for res in user_resources:
        if res in user_settings:
            for i, value in user_settings[res].items():
                hash_val = _hash_fun(user_settings[res][i])
                hash_dict[f"{res}.{i}"] = hash_val

    data[f"{receipe}"] = [hash_dict]

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


def info(receipe) -> None:
    """list out the info for the settings"""
    # if validate(receipe):
    #     settings = get_user_settings(receipe)
    pass


def validate(receipe, settings) -> bool:
    """Validate the user configuration"""

    if not check_if_receipe_exists(receipe):
        logging.error(f"`{i}` receipe doesn't exist in configuration files")
        return False

    res_validation = validate_unsupported_resources(get_user_settings(receipe))

    if res_validation:
        logging.warning(
            f"Unsupported resources found in the `{receipe}` configuration file"
        )
        for i in res_validation:
            logging.warning(
                f"`{i}` resource in {receipe} receipe isn't supported")
            return False

    user_settings = get_user_settings(receipe)
    user_resources = get_user_defined_resources(user_settings)

    if not user_resources:
        logging.warning(
            f"No user resources found in the `{receipe}` configuration file")
        return False

    for res in user_resources:
        if res in user_settings:
            for i in user_settings[res]:

                if not isinstance(user_settings[res][i], DynaBox):
                    logging.warning(
                        f"Missing subconfig `{res}` resource in {receipe} receipe"
                    )
                    return False

                if not user_settings[res][i].get('name', None):
                    logging.warning(
                        f"Missing `name`attributes in resource `{i}` in receipe {receipe}"
                    )
                    return False

                if not user_settings[res][i].get('action', None):
                    logging.warning(
                        f"Missing `action` attributes in resource `{i}` in receipe {receipe}"
                    )
                    return False

                unsupported_attr = OrderedSet(
                    user_settings[res][i].keys()) - res_attributes

                if (unsupported_attr - srv_attributes) and res.upper() == "SERVICE":
                    logging.warning(
                        f"Found one more attributes that aren't supported"
                    )
                    for unsup in (unsupported_attr - srv_attributes):
                        logging.warning(
                            f"`{unsup}` not supported attribute in resource {res} in receipe {receipe}"
                        )
                    return False

                if (unsupported_attr - dir_attributes) and res.upper() == "DIRECTORY":
                    logging.warning(
                        f"Found one more attributes that aren't supported"
                    )
                    for unsup in (unsupported_attr - dir_attributes):
                        logging.warning(
                            f"`{unsup}` not supported attribute in resource {res} in receipe {receipe}"
                        )
                    return False

                if (unsupported_attr - file_attributes) and res.upper() == "FILE":
                    logging.warning(
                        f"Found one more attributes that aren't supported"
                    )
                    for unsup in (unsupported_attr - file_attributes):
                        logging.warning(
                            f"`{unsup}` not supported attribute in resource {res} in receipe {receipe}"
                        )
                    return False

                # now validate the values from the user-input string
                user_values = user_settings[res][i].get('action', None)
                if res.upper() == "SERVICE":
                    for val in user_values:
                        if val not in service_setup_actions.union(
                                service_op_actions):
                            logging.warning(
                                f"`{val}` not supported in action attribute in resource {res} in receipe {receipe}"
                            )

                else:
                    if res.upper() in ["FILE", "DIRECTORY"]:
                        for val in user_values:
                            if val not in dir_file_actions:
                                logging.warning(
                                    f"`{val}` not supported in action attribute in resource {res} in receipe {receipe}"
                                )
                print(user_settings[res][i])

    return True


def gen_command(settings_dict: Dict, key: str, output: List) -> None:
    """Function to the generate the OS commands by reading the settings_dict and update the input list format"""
    if key.upper() in ["SERVICE"]:
        for index, value in settings_dict[key].items():
            if isinstance(value, DynaBox) and index != "params":
                for n in value['name']:
                    for act in value['action']:
                        if act in service_setup_actions:
                            output.append("sudo apt update")
                            output.append(f"sudo apt {act} {n} -y")
                        else:
                            if act in service_op_actions:
                                output.append(f"systemctl {act} {n} -force")

    if key.upper() in ["DIRECTORY", "FILE"]:
        for index, value in settings_dict[key].items():
            for n in value['name']:
                for act in value['action']:
                    if act == "create" and value['params'].get(
                            'owner', None) and value['params'].get('group', None):
                        cmd: str = f"chown {value['params']['owner']}:{value['params']['group']} {n}"
                        if value['params'].get('recurse', None) and json.loads(
                                (value['params'].get('recurse', None)).lower()):
                            cmd += " -R"
                        output.append(cmd)

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
                            output.append(f"apt-get {act} {n} -y")
                        else:
                            output.append(f"systemctl {act} {n} -force")

    return None


def push(receipe) -> None:
    """Pushes the configuration to the operating system"""
    output = []
    user_settings = get_user_settings(receipe)
    user_resources = get_user_defined_resources(user_settings)

    for key, value in user_settings.items():
        if key in user_resources:
            res = gen_command(user_settings, key, output)

    print(output)


def clean(receipe) -> None:
    pass

import subprocess 

def loop_through_os_commands(input) -> None:
    for i in input: 
        process = subprocess.Popen(i.split(), stdout = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    print(output.strip())
                break
    



if __name__ == "__main__":
    loop_through_os_commands(['powershell.exe echo hello world', 'powershell.exe echo test1'])
    
