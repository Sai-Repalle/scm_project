import os
import glob 
from dynaconf import Dynaconf



configuration = Dynaconf(
    envvar_prefix="scm",
    settings_files=glob.glob(f"{con_dir_full}/*.toml")
)
