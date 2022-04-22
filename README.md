# SCM
Self Managed Configuration Management(SCM) is a simple command line app for configuration management, written in python.
# Installation
## Using Pip
```bash
  $ pip install scm
```
## Manual clone
```bash
  $ git clone https://github.com/Sai-Repalle/scm_project
  $ cd scm_project
  $ python3 -m venv venv 
  $ source venv/bin/activate
  $ pip install -r requirements.txt 
```
# Usage
```bash
Usage: scm [OPTIONS] COMMAND [ARGS]...
Options:
  -v, --version         Display\'s the application version
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  create
  diff
  info
  init
  push
  validate

```
## initlization
init command is used for initlization and helpful to create the respective directories, also this command is useful for exapanding future versions of the scm tool

`init <keyword>`
To start with the tool, initlizaze the tool without any parameters, this would set the configuration files required for tool to work
```bash
$ scm init python
```
### output 
```bash
scm init   
root@machine:~/scm# python3 -m scm init
[INFO][04-22-2022 06:08:13]::Reading the Json configuration /root/scm/scm/settings/settings.json
[INFO][04-22-2022 06:08:13]::creating directory CONFIG_DIR
[INFO][04-22-2022 06:08:13]::creating directory CONFIG_HASH_DIR
[INFO][04-22-2022 06:08:13]::creating files CONFIG_DEF_FILE
[INFO][04-22-2022 06:08:13]::creating files CONFIG_HASH_FILE

```
## create
`create <name>`
```bash
$ scm init --receipe_name <receipe_name>
```
Below example, will create a receipe called "apache" and `apache.toml` file is created in the config directory located at the root directory of the scm 
### output 
```bash
root@machine:~/scm# python3 -m scm create --receipe apache
[INFO][04-22-2022 06:09:56]::Reading the Json configuration /root/scm/scm/settings/settings.json
[INFO][04-22-2022 06:09:56]::creating directory CONFIG_DIR
[INFO][04-22-2022 06:09:56]::CONFIG_DIR directory already exists
[INFO][04-22-2022 06:09:56]::creating directory CONFIG_HASH_DIR
[INFO][04-22-2022 06:09:56]::CONFIG_HASH_DIR directory already exists
[INFO][04-22-2022 06:09:56]::creating files CONFIG_DEF_FILE
[INFO][04-22-2022 06:09:56]::creating files CONFIG_HASH_FIL
```


## info
`info --receipe_name <name>`
```bash
$ scm info --receipe_name <receipe_name>
```
```bash 

```
## validate
`validate <name>`
```bash
$ scm validate --receipe_name <receipe_name>
```

## push
`push <name>`
```bash
$ scm push --receipe_name <receipe_name>
```

## clean
`clean <name>`
```bash
$ scm clean --receipe_name <receipe_name>
```