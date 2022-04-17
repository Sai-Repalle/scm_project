import os
import logging
from typing import List, Set, Dict 
from dynaconf import Dynaconf, Validator
from dynaconf.utils.boxing import DynaBox
from ordered_set import OrderedSet
import json 

logging.basicConfig(format='[%(levelname)s][%(asctime)s]::%(message)s',
                    datefmt="%m-%d-%Y %H:%M:%S")
logger = logging.getLogger()
supp_res = OrderedSet(['SERVICE', 'FILE', 'DIRECTORY'])
os.environ['ROOT_PATH_FOR_DYNACONF'] = "./my_configuration"
#os.environ['ENVIRONMENTS_FOR_DYNACONF'] =f"{list(supp_res)}"
#print(os.environ['ENVIRONMENTS_FOR_DYNACONF'])
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

def get_user_settings(receipe, validator=None,environments=True) -> Dict:
    return  Dynaconf(settings_files=[f"{receipe}.toml"], 
                        validators=validator)

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


def info(receipe) -> None:
    """list out the info for the settings"""
    # if validate(receipe):
    #     settings = get_user_settings(receipe)
    pass 

        # for i in supp_res:
        #     print(settings[i])


def validate(receipe) -> bool:
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

    #Validators =[Validator('name', 'action', 'test', envs='service',must_exist=True)]
    

    user_settings = get_user_settings(receipe)
    user_resources = get_user_defined_resources(user_settings)
    
    if not user_resources:
        logging.warning(f"No user resources found in the `{receipe}` configuration file")
        return False 

    return True

def gen_command(settings_dict: Dict, key: str, output: List) -> None:
    if key.upper() == "SERVICE":
        for index, value in settings_dict[key].items():
            if isinstance(value, DynaBox) and index != "params":
                for n in value['name']:
                    for act in value['action']:
                        if act == "install":
                            output.append(f"apt-get {act} {n} -y")
                        else: 
                            output.append(f"systemctl {act} {n} -force")

    if key.upper() == "DIRECTORY": 
        for index, value in settings_dict[key].items(): 
            for n in value['name']:
                for act in value['action']:
                    if act == "create" and value['params'].get('owner', None) and value['params'].get('group', None):
                        cmd: str = f"chown {value['params']['owner']}:{value['params']['group']} {n}"
                        if value['params'].get('recurse',None) and json.loads((value['params'].get('recurse',None)).lower()):
                            cmd += " -R"
                        output.append(cmd)
                    
            if value.get('notifies', None):
                inp_json = json.loads(value.get('notifies', None).replace("\'","\""))
                for n in inp_json['name']:
                    for act in inp_json['action']:
                        if act == "install":
                            output.append(f"apt-get {act} {n} -y")
                        else: 
                            output.append(f"systemctl {act} {n} -force")
        
                            
                        
                         
                         
                
                
            
        
    
    if key.upper() == "FILE": 
        #print(settings_dict[key])
        pass 
    return output 
     
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
                    
    

if __name__ == "__main__":
    receipe = "apache"
    # create(receipe)
    # valid = validate(receipe)
    # if valid:
    #     info(receipe)
    push(receipe)
