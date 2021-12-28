"""
# File       : configs.py
# Time       : 2021/12/16 18:03
# Author     : 曹剑南
# version    : python 3.7
"""

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
        "meter_no": "M202009040003",
        "api_url": "http://empower.hes-api.kaifa.tst/",
        "web_url": "http://10.32.233.31:30071/",
        "kafka_url":"10.32.233.63:30077",
        "ami_user":"dmms",
        "ami_passwd":"sa",
        "daily_entries":93,
        "daily_len":22,
        "monthly_entries":12,
        "monthly_len":33,
        "lp_entries": 4512,
        "lp_len": 5,
        "pq_entries": 1440,
        "pq_len": 5,
        "event_entries": 3
    },
    "ivy": {
        "db_source": "Oracle",
        "db_host": "10.32.233.164",
        "db_port": 1621,
        "db_user": "ami",
        "db_pwd": "ami",
        "db_service": "ami",
        "db_database": "",
        "meter": 312121
    },
    "saturn03": {
        "db_source": "Oracle",
        "db_host": "10.32.233.164",
        "db_user": "ami",
        "db_port": 1621,
        "db_pwd": 'ami',
        "db_service": 'ami',
        "meter": 312121
    }
}


class Project:
    name = 'empower'  # 与下面setting项目key对应
    tag = 'hesSyncTest or hesAsyncTest'  # 对应comms.marker
    path = '/'  # 对testData目录接口对应
    continue_last_check = False  # 是否断点续测OBIS

    obis_sql1 = "select register_id, class_id, attribute_id, register_desc, is_method, data_type, rw from "
    obis_sql2 = " where PTL_TYPE = (select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no = '{}'))".format(
        setting[name]['meter_no'])
