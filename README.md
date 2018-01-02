# zabbix-tool.py

This tool can operate add host or get information like hosts or groups easily by using pyzabbix module if you don't want to need many operate one.

## Requirements
* python3
* pyYAML
* pyzabbix
* argparse

## Description
#### 1.Initialize config
First, you need to make /etc/yunctl/zabbix/config.yml to use zabbix API.
It's not encrypted. 
```bash
# zabbix-tool init
```
#### 2. Get infomation
Second, get group and template id.
```bash
# zabbix-tool get groups
# zabbix-tool get templates
```
#### 3. Make host file.
Following Zabbix API's host.create,  You make yaml file.
```yaml
host: 'test'
interfaces: [
    { 'type': 1, 'ip': '192.168.0.12', 'main': 1, 'useip': 1, 'dns': '', 'port': '10050'},
]
groups: [
    { 'groupid': '6' },
]
templates: [
    { 'templateid': '10104' },
    { 'templateid': '10102' },
]
```
#### 4. Add host
Finally, you add host by using host file.
```bash
# zabbix-tool create -f ./sample.yml
```
