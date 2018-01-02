#!/usr/bin/env python

from pyzabbix import ZabbixAPI as z
import yaml
import sys
import argparse as ap
import os
import sys

conf_dir = '/etc/yunctl/zabbix'
conf_file = 'config.yml'
conf_path = conf_dir + '/' + conf_file

def init(args):
  if os.path.exists(conf_path):
    print("%s is existed, you need move or remove one." % conf_file)
    sys.exit(1)
  elif not os.path.exists(conf_dir):
    os.makedirs(conf_dir)

  conf = {
    'api_server': '127.0.0.1',
    'https': 'False',
    'api_user': 'admin',
    'api_pass': 'zabbix',
    'api_url': '',
}
  args = {}
  args['api_server'] = input('Please enter zabbix api server\'s ip or hostname. (default=127.0.0.1)\napi_server : ')
  args['https'] = input('Please enter True if you need https. (default=False)\n https : ')
  args['api_user'] = input('Please enter api user. (default=admin)\n api_user : ')
  args['api_pass'] = input('Please enter api pass. (default=zabbix)\n api_pass : ')

  for i in args.keys():
    if not args[i] == '':
      conf[i] = args[i]

  if conf['https'] in ['True', 'true']:
    conf['api_url'] = 'https://' + conf['api_server'] + '/zabbix/'
  else:
    conf['api_url'] = 'http://' + conf['api_server'] + '/zabbix/'

  with open(conf_path, 'w') as f:
    for key in conf.keys():
      f.write('%s: \'%s\'\n' % (key, conf[key]))

def get(args):
  arg = args.args
  if not arg in [ 'hosts', 'groups', 'templates']:
    raise TypeError('Invalid argument')

  params = {}
  if arg == 'hosts':
    params = { 'method': 'host', 'id': 'hostid', 'name': 'host' }
  elif arg == 'groups':
    params = { 'method': 'hostgroup', 'id': 'groupid', 'name': 'name' }
  elif arg == 'templates':
    params = { 'method': 'template', 'id': 'templateid', 'name': 'name' }


  if not os.path.exists(conf_path):
    print('%s is not found...')
    init('init')

  conf = _load_yaml(conf_path)
  result = _call_api(conf['api_url'], conf['api_user'], conf['api_pass'], params['method'] + '.get')
  for line in result:
    print('{name: %s, id: %s}' % (line[params['name']], line[params['id']]))

def create(args):
  f_name = args.f
  if not os.path.exists(f_name):
    raise FileNotFoundError('%s is not found' % f_name)

  if not os.path.exists(conf_path):
    print('%s is not found...')
    init('init')

  conf = _load_yaml(conf_path)
  params = _load_yaml(f_name)
  try:
    _call_api(conf['api_url'], conf['api_user'], conf['api_pass'], 'host.create', params)
  except Exception as e:
    print('faild add host...\n %s' % e)
    sys.exit(1)


def _call_api(url, api_user, api_pass, method, args=''):
  obj = z(url)
  obj.login(api_user, api_pass)
  api_method = "obj.%s(%s)" % (method, args)
  return(eval(api_method))

def _load_yaml(path):
  with open(path) as f:
    result = yaml.load(f)
  return(result)


parser = ap.ArgumentParser(description='This is operate zabbix')

sub = parser.add_subparsers(help='sub_command')
sub_get = sub.add_parser('get', help='get hosts,groups or templates infomation')
sub_get.add_argument('args', help='[hosts | groups | templates]')
sub_get.set_defaults(func=get)

sub_create = sub.add_parser('create', help='add new hosts')
sub_create.add_argument('-f',metavar='file_name', help='need yaml file', required=True)
sub_create.set_defaults(func=create)

sub_create = sub.add_parser('init', help='initialize and make config')
sub_create.set_defaults(func=init)

# parse argument
args = parser.parse_args()

# execute sub_command function
args.func(args)
