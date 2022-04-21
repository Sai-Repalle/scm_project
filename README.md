# SCM
self managed configuration mangement(scm) is a simple command line app for configuration management, written in python.
# Installation
## Using Pip
```bash
  $ pip install scm
```
## Manual
```bash
  $ git clone https://github.com/Sai-Repalle/scm_project
  $ cd scm_project
  $ python setup.py install
```
# Usage
```bash
$ scm
```
## initlization
init command is used for initlization and helpful to create the respective directories, also this command is useful for exapanding future versions of the scm tool

`init <keyword>`

```bash
$ scm init python
```
### output 
```
scm init   
[INFO][04-17-2022 23:59:26]::Reading the Json configuration C:\Users\sarepall\Documents\scm_project\scm\settings\settings.json
[INFO][04-17-2022 23:59:26]::creating directory CONFIG_DIR
[INFO][04-17-2022 23:59:26]::creating directory CONFIG_HASH_DIR
[INFO][04-17-2022 23:59:26]::creating files CONFIG_DEF_FILE
[INFO][04-17-2022 23:59:26]::creating files CONFIG_HASH_FILE
```
## Lookup
`search <name>`
```bash
$ cver look-up CVE-2020-2121
```