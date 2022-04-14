import os 

def write_default_config(file): 
    with open(file, mode="w") as f: 
        f.write("#This is the default configuration file")
        f.write("#sample file for testing the command line interface")
    f.close()