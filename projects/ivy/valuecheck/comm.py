# -*- coding:utf-8 -*-
# @Time     :2020/12/8
# @Author   :jiannan
# @Version  :v1
# @Updated  :0000/00/00
# @RunTime  :


def read_config(file_path):
    """读取配置文件内容"""
    with open(file_path, encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config


def check_len(profile, length):
    if len(profile) == length:
        return True
    else:
        return False
