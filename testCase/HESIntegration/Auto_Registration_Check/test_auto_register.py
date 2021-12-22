# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import pytest, allure, time, datetime, json, random
from kafka import KafkaProducer
from common.marker import *
from config.settings import *


class Test_Auto_Register:
    """
    验证GPRS电表是否支持系统的自动注册功能
    """

    # @hesAsyncTest
    def test_meter_register(self, get_database, caseData, meter_init):
        data = caseData('testData/HESAPI/AutoRegistration/register-event-process.json')['gprs_meter']
        requestData = data['pl']
        requestData[0]['dn'] = setting[Project.name]['meter_no']
        producer = KafkaProducer(bootstrap_servers=setting[Project.name]['kafka_url'])
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        sql1 = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='M202009040003' and JOB_TYPE='DeviceRegist'"
        db_queue = get_database.orcl_fetchall_dict(sql1)
        print(db_queue)
        while len(db_queue) == 0:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')

        sql2 = "select TASK_STATE from h_task_run_his where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql2)
        while len(db_queue) == 0:
            time.sleep(8)
            db_queue = get_database.orcl_fetchall_dict(sql2)
            print(db_queue)
            print('Waiting for Reg Tasks to finish...')

        assert db_queue[0]['TASK_STATE'] == 3
