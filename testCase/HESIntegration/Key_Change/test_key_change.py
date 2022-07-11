# -*-coding:utf-8-*-
"""
# File       : test_key_change.py
# Time       ：2022/2/9 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import time
from common.marker import *
from common.HESRequest import *


class Test_Key_Change:

    @asyncTest
    def test_key_change_Akey(self, caseData, get_database,device,requestMessage):
        """
        正常修改GPRS电表key - A key
        """
        count = 0
        data = caseData('testData/KeyChange/key_change_task.json')
        requestData = data['ChangeKey']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        print(requestData)
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert response.status_code == 200

        time.sleep(3)
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='CHANGE_KEY'".format(
            device['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 3:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for set tariff Tasks to Create...')
            count = count + 1

        sql_his = "select task_state from H_TASK_RUN_HIS where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
        db_queue = get_database.orcl_fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 40:
            time.sleep(10)
            db_queue = get_database.orcl_fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for set tariff Tasks to finish...')
            count = count + 1
        assert db_queue[0]['task_state'] == 3

    @asyncTest
    def test_key_change_Ekey(self, caseData,get_database,device,requestMessage):
        """
        正常修改GPRS电表key - E key
        """
        count = 0
        data,user_config = caseData('testData/KeyChange/key_change_task.json')
        requestData = data['ChangeKey']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        requestData['payload'][0]['data'][0]['parameter']['KeyType'] = 0
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        print(requestData)
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert response.status_code == 200

        time.sleep(3)
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='CHANGE_KEY'".format(
            device['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 3:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for set tariff Tasks to Create...')
            count = count + 1

        sql_his = "select task_state from H_TASK_RUN_HIS where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
        db_queue = get_database.orcl_fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 40:
            time.sleep(10)
            db_queue = get_database.orcl_fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for set tariff Tasks to finish...')
            count = count + 1
        assert db_queue[0]['task_state'] == 3