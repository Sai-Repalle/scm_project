# SCM
Self Managed Configuration Management(SCM) is a simple command line app for configuration management, written in python.
> Designed to run only on ubuntu operating system

This tool, currently supports below resources 
* service
* directory
* file 
* firewall
>A resource definition in scm is directly related to the action of standard linux commands, example. service, directories, files.

>pre-requisites install python3 environment on the machine
# Usage
```bash 
pip install scm-config
```

```bash
Usage: scm [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version                   Display's the application version
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create
  diff
  info
  init
  push
  remove
  validate
```

# Commands overview 

| command  | command description                                                                                                                      | usage                                                               | Example                                           |   |
|----------|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------|---|
| init     | used for initialization, creates necessary files and directories                                                                         | scm init                                                            |                                                   |   |
| create   | creates the receipe .toml file in the config directory based on the receipe name                                                         | scm create --receipe <name>                                         | scm create --receipe apache                       |   |
| validate | validates the receipe file configuration based on the standard defined resources                                                         | scm validate --receipe <name>                                       | scm validate --receipe apache                     |   |
| info     | lists the configurations that are defined in the receipe file                                                                            | scm info --receipe <name>                                           | scm info --receipe apache                         |   |
| diff     | lists the differences between the existing and the current configuration, if this is this is new receipe, outputs all the configurations | scm diff --receipe <name>                                           | scm diff --receipe apache                         |   |
| push     | pushes the configuration defined in the receipe file to the operating system and stores the configuration in config_hash_directory       | scm push --receipe <name>                                           | scm push --receipe apache                         |   |
| remove   | Removes the configuration from the hash directory and also removes the receipe file from the config directory                            | scm push --receipe <name> [optional --force [optional --clean-files | scm remove --receipe apache --force --clean-files |   |


# Resource Detailed information 
## Service 
Service resource is useful for installing and managing packages from the linux repository, 
> Note that currently this tool is designed to support only on Ubuntu Operating System

***Name parameter in the below section is a list format, meaning it can take multiple values and the actions and other parameters are applied to each name resource accordingly**
### Example 
```
[service.setup]
name = ["apache2"] 
action= ["install", "enable"]
```
In the above example, "service" is the resource and "setup" is the service identifier. 
* name  -> Name of the service that is to be installed on the ubuntu system 
* action -> Action to be done on the listed service, currently these are only supported 
> ["install", "enable", "disable"]

```
[service.ops]
name = ["apache2"]
action =["restart"]
```
In the above example, "service" is the resource and "ops" is the service identifier. once the service is installed and service operations can be done using this tool. 
* name  -> Name of the service that is to be installed on the ubuntu system 
* action -> Action to be done on the listed service, currently these are only supported 
> ["stop", "start", "restart", "reload", "disable", "enable"]

## Directory
Directory resource is useful for installing and managing the metadata directories on the system, 
> Note that currently this resource is tested only on Ubuntu Operating System, but can run on any Linux Operating System

### Example 
```
# Modify the directory permissions 
[directory.list]
name = ["/etc/apache"] 
params = {'owner'='root','group'='root','mode'= '0755'}
action = ['create']
notifies = "@format {this.service.ops}"
```
In the above example, "directory" is the resource and "list" is the service identifier. 
* name  -> Name of the directory where the metadata needs modification including creation of the directory using the action method
* params -> parameter to support the directory operations, currently ['owner', 'group' and 'mode'] are supported in the list 
* action -> Action to be done on the listed service, currently for directories only ['create'] is supported
* notifies -> Parameter to notify any other resource in the same recipe file, In example, notifies the service ops resources, that would restart the apache2 service based on the modifications 
> ["install", "enable", "disable"]

### Example 
```
# Modify the input content of the file 
[file.conf]
name = ["/var/www/customers/public_html/index.php"]
action = ["create"]
override ="true"
content  = ["This is the test file"]
params = {'owner'= 'root','group'= 'root','mode' = '0755'}
notifies = "@format {this.service.ops}"

```
In the above example, "file" is the resource and "conf" is the service identifier. 
* name  -> Name of the file where the content need to be added or appended based on the configuration requirement
* action -> Action to be done on the listed service, currently for file only ['create'] is supported
* override -> This parameter will override if there is any existing file, default it will append the content to the file 
* content -> Input content for the file provide in the form the double quotes. For simplicity ,large content is not tested with the current version of the code. 
* params -> parameter to support the file operations, currently ['owner', 'group' and 'mode'] are supported in the list 
* notifies -> Parameter to notify any other resource in the same recipe file, In example, notifies the service ops resources, that would restart the apache2 service based on the modifications 
> ["install", "enable", "disable"]

# Complete overview of the example file 

```toml
# Service setup for the apache instance 
[service.setup]
name = ["apache2"] 
action= ["install", "enable"]

# Service restart for the apache instance 
[service.ops]
name = ["apache2"]
action =["restart"]


# Modify the directory permissions 
[directory.list]
name = ["/etc/apache"] 
params = {'owner'='root','group'='root','mode'= '0755'}
action = ['create']
notifies = "@format {this.service.ops}"

# Modify the input content of the file 
[file.conf]
name = ["/var/www/customers/public_html/index.php"]
action = ["create"]
content  = ["This is the test file"]
params = {'owner'= 'root','group'= 'root','mode' = '0755'}
notifies = "@format {this.service.ops}"
```
# Installation and Usage # 

## Manual clone
```bash
  $ git clone https://github.com/Sai-Repalle/scm_project
  $ cd scm_project
  $ python3 -m venv venv 
  $ source venv/bin/activate
  $ pip install -r requirements.txt 
```

## initialization
init command is used for initialization and helpful to create the respective directories, also this command is useful for expanding future versions of the scm tool

`init`
To start with the tool, initialize the tool without any parameters, this would set the configuration files required for tool to work
```bash
$ scm init
```
### output 
```bash   
scm init
[INFO][04-22-2022 06:08:13]::Reading the Json configuration /root/scm/scm/settings/settings.json
[INFO][04-22-2022 06:08:13]::creating directory CONFIG_DIR
[INFO][04-22-2022 06:08:13]::creating directory CONFIG_HASH_DIR
[INFO][04-22-2022 06:08:13]::creating files CONFIG_DEF_FILE
[INFO][04-22-2022 06:08:13]::creating files CONFIG_HASH_FILE

```
## create
`create <name>`
```bash
$ scm create --receipe <receipe>
```
Below example, will create a receipe called "apache" and `apache.toml` file is created in the config directory located at the root directory of the scm 
### output 
```bash
scm create --receipe apache
[INFO][04-22-2022 06:09:56]::Reading the Json configuration /root/scm/scm/settings/settings.json
[INFO][04-22-2022 06:09:56]::creating directory CONFIG_DIR
[INFO][04-22-2022 06:09:56]::CONFIG_DIR directory already exists
[INFO][04-22-2022 06:09:56]::creating directory CONFIG_HASH_DIR
[INFO][04-22-2022 06:09:56]::CONFIG_HASH_DIR directory already exists
[INFO][04-22-2022 06:09:56]::creating files CONFIG_DEF_FILE
[INFO][04-22-2022 06:09:56]::creating files CONFIG_HASH_FIL
```


## info
`info --receipe <name>`
```bash
$ scm info --receipe <receipe>
```
Below example, info command is listing all the resources and its actions based on the configuration defined in the receipe file.
### output 
```bash
scm info --receipe apache
[INFO][04-25-2022 02:00:37]::Reading the Json configuration /root/scm/settings.json
[INFO][04-25-2022 02:00:37]::creating directory CONFIG_DIR
[INFO][04-25-2022 02:00:37]::CONFIG_DIR directory already exists
[INFO][04-25-2022 02:00:37]::creating directory CONFIG_HASH_DIR
[INFO][04-25-2022 02:00:37]::CONFIG_HASH_DIR directory already exists
[INFO][04-25-2022 02:00:37]::creating files CONFIG_DEF_FILE
[INFO][04-25-2022 02:00:37]::creating files CONFIG_HASH_FILE
[INFO][04-25-2022 02:00:37]::SERVICE.setup - {'name': ['apache2'], 'action': ['install', 'enable', 'start']}
[INFO][04-25-2022 02:00:37]::SERVICE.ops - {'name': ['apache2'], 'action': ['restart']}
[INFO][04-25-2022 02:00:37]::SERVICE.setup_php - {'name': ['php', 'libapache2-mod-php'], 'action': ['install']}
[INFO][04-25-2022 02:00:37]::FIREWALL.setup - {'name': ['Apache'], 'action': ['allow']}
[INFO][04-25-2022 02:00:37]::FILE.conf - {'name': ['/var/www/html/index.php'], 'action': ['create'], 'override': 'true', 'content': ['<?php\n header("Content-Type: text/plain");\n echo "Hello, world!\n";\n'], 'params': {'owner': 'root', 'group': 'root', 'mode': '0755'}, 'notifies': "{'name': ['apache2'], 'action': ['restart']}"}
[INFO][04-25-2022 02:00:37]::FILE.phpindex - {'name': ['/etc/apache2/mods-enabled/dir.conf'], 'action': ['create'], 'override': 'true', 'content': ['<IfModule mod_dir.c>\n DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm </IfModule>'], 'params': {'owner': 'root', 'group': 'root', 'mode': '0755'}, 'notifies': "{'name': ['apache2'], 'action': ['restart']}"}
```

## validate
`validate -receipe <name>`
```bash
$ scm validate --receipe <receipe>
```
Below example, validate command is validating all the resources and its actions based on the configuration defined in the receipe file, If all the resources and its configurations are in valid state, receipe would output to do next step, if there are any issues, please refere to the documentation.
### output  
```bash
scm validate --receipe apache
[INFO][04-25-2022 02:01:47]::Reading the Json configuration /root/scm/settings.json
[INFO][04-25-2022 02:01:47]::creating directory CONFIG_DIR
[INFO][04-25-2022 02:01:47]::CONFIG_DIR directory already exists
[INFO][04-25-2022 02:01:47]::creating directory CONFIG_HASH_DIR
[INFO][04-25-2022 02:01:47]::CONFIG_HASH_DIR directory already exists
[INFO][04-25-2022 02:01:47]::creating files CONFIG_DEF_FILE
[INFO][04-25-2022 02:01:47]::creating files CONFIG_HASH_FILE
[INFO][04-25-2022 02:01:47]::apache receipe file is valid for push, use `scm diff` to differences with the existing configuration
```

## diff
`diff -receipe <name>`
```bash
$ scm diff --receipe <receipe>
```
```bash
[INFO][04-25-2022 02:05:00]::Reading the Json configuration /root/scm/settings.json
[INFO][04-25-2022 02:05:00]::Reading the Json configuration /root/scm/settings.json
[INFO][04-25-2022 02:05:00]::creating directory CONFIG_DIR
[INFO][04-25-2022 02:05:00]::CONFIG_DIR directory already exists
[INFO][04-25-2022 02:05:00]::creating directory CONFIG_HASH_DIR
[INFO][04-25-2022 02:05:00]::CONFIG_HASH_DIR directory already exists
[INFO][04-25-2022 02:05:00]::creating files CONFIG_DEF_FILE
[INFO][04-25-2022 02:05:00]::creating files CONFIG_HASH_FILE
[INFO][04-25-2022 02:05:00]::apache receipe file is valid for push, use `scm diff` to differences with the existing configuration
[INFO][04-25-2022 02:05:00]::Reading the Json configuration config_hash/hash_config_md5.json
[INFO][04-25-2022 02:05:00]::`apache` configuration is update to date with the existing configuration
```

## push
`push -receipe <name>`
```bash
$ scm push --receipe <receipe>
```

## remove
`remove --receipe <name> --force <optional> --clean_files <optional>`
```bash
$ scm push --receipe <receipe>