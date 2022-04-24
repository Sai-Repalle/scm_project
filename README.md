# SCM
Self Managed Configuration Management(SCM) is a simple command line app for configuration management, written in python.
> Designed to run only on ubuntu operating system

This tool, currently supports only below resources 
* service
* directory
* file 
* firewall


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
## Usage
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
## initialization
init command is used for initialization and helpful to create the respective directories, also this command is useful for expanding future versions of the scm tool

`init <keyword>`
To start with the tool, initialize the tool without any parameters, this would set the configuration files required for tool to work
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