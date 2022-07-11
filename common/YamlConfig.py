# _*_ coding: utf-8 _*_
# @Time      : 2022/5/5 16:50
# @Author    : Jiannan Cao
# @FileName  : YamlConfig.py.py
import os
import yaml
import nacos

def readConfig():
    current_path = os.path.abspath(__file__)
    config_file_path = os.path.join(
        os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".." + os.path.sep + 'config'),
        'settings.yaml')
    with open(config_file_path, 'r') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result

def writeConfig(data):
    current_path = os.path.abspath(__file__)
    config_file_path = os.path.join(
        os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".." + os.path.sep + 'config'),
        'settings.yaml')
    with open(config_file_path, 'w') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


def nacosConfig():
    client = nacos.NacosClient(server_addresses=readConfig()['nacos_url'], namespace='HES', username="nacos",
                               password="nacos")
    data_id = readConfig()['project']
    group = readConfig()['group']
    config = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
    return config