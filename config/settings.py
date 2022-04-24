"""
# File       : configs.py
# Time       : 2021/12/16 18:03
# Author     : 曹剑南
# version    : python 3.7
"""
from common.HESAPI import *

# 所有项目配置
setting = {
    "empower": {
        "db_source": "Oracle",
        "db_host": "10.32.233.209",
        "db_port": 1521,
        "db_user": "empower",
        "db_pwd": "empower",
        "db_service": "ami_empower",
        "db_database": "ami_db",
        "api_url": "http://empower.hes-api.kaifa.tst",
        "web_url": "http://10.32.233.31:30071",
        "kafka_url": "10.32.233.63:30077",
        "ami_user": "dmms",
        "ami_passwd": "sa"
    },
    "ivy": {
        "db_source": "Oracle",
        "db_host": "10.32.233.209",
        "db_port": 1521,
        "db_user": "empower",
        "db_pwd": "empower",
        "db_service": "ami_empower",
        "db_database": "ami_db",
        "api_url": "http://empower.hes-api.kaifa.tst",
        "web_url": "http://10.32.233.31:30071",
        "kafka_url": "10.32.233.63:30077",
        "ami_user": "dmms",
        "ami_passwd": "sa"
    },
    "saturn03": {
        "db_source": "Oracle",
        "db_host": "10.32.233.209",
        "db_port": 1521,
        "db_user": "empower",
        "db_pwd": "empower",
        "db_service": "ami_empower",
        "db_database": "ami_db",
        "api_url": "http://empower.hes-api.kaifa.tst",
        "web_url": "http://10.32.233.31:30071",
        "kafka_url": "10.32.233.63:30077",
        "ami_user": "dmms",
        "ami_passwd": "sa"
    },
    "bamboo01": {
        "db_source": "Oracle",
        "db_host": "10.32.233.209",
        "db_port": 1521,
        "db_user": "empower",
        "db_pwd": "empower",
        "db_service": "ami_empower",
        "db_database": "ami_db",
        "api_url": "http://empower.hes-api.kaifa.tst",
        "web_url": "http://10.32.233.31:30071",
        "kafka_url": "10.32.233.63:30077",
        "ami_user": "dmms",
        "ami_passwd": "sa"
    },
    "octopus02": {
        "db_source": "Oracle",
        "db_host": "10.32.233.209",
        "db_port": 1521,
        "db_user": "empower",
        "db_pwd": "empower",
        "db_service": "ami_empower",
        "db_database": "ami_db",
        "api_url": "http://10.32.233.31:30018",
        "web_url": "http://10.32.233.31:30071",
        "kafka_url": "10.32.233.63:30077",
        "ami_user": "dmms",
        "ami_passwd": "sa"
    },
    "smartpark": {
        "db_source": "Oracle",
        "db_host": "10.32.233.209",
        "db_port": 1521,
        "db_user": "empower",
        "db_pwd": "empower",
        "db_service": "ami_octopus_prod_qa",
        "db_database": "ami_db",
        "api_url": "http://10.32.233.31:30351",
        "web_url": "http://10.32.233.31:30351",
        "kafka_url": "10.32.233.31:30012",
        "ami_user": "dmms"
    }
}


class Project:
    name = 'empower'  # 与下面setting项目key对应
    tag = 'smokeTest'  # 对应common.marker  smokeTest or hesAsyncTest
    retry = 0  # 用例失败自动重试次数

    path = '/'  # 对testData目录接口对应
    continue_last_check = False  # 是否断点续测OBIS

    request_url = HESAPI(Address=setting[name]['api_url']).requestAddress()