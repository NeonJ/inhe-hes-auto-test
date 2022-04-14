# -*-coding:utf-8-*-
"""
# File       : test_key_change.py
# Time       ：2022/2/9 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import time
from common.marker import *
from common.HESRequest import HESRequest
from config.settings import *


class Test_Key_Change:

    @hesAsyncTest
    def test_key_change_Akey(self, caseData,get_database):
        """
        正常修改GPRS电表key - A key
        """
        count = 0
        data = caseData('testData/{}/KeyChange/key_change_task.json'.format(Project.name))['ChangeKey']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        print(requestData)
        response = HESRequest().post(url=Project.request_url, params=requestData)
        assert response.status_code == 200

        time.sleep(3)
        sql_running = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='CHANGE_KEY'".format(
            setting[Project.name]['meter_no'])
        db_queue = get_database.orcl_fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 3:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for set tariff Tasks to Create...')
            count = count + 1

        sql_his = "select TASK_STATE from H_TASK_RUN_HIS where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 40:
            time.sleep(10)
            db_queue = get_database.orcl_fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for set tariff Tasks to finish...')
            count = count + 1
        assert db_queue[0]['TASK_STATE'] == 3

    @hesAsyncTest
    def test_key_change_Ekey(self, caseData,get_database):
        """
        正常修改GPRS电表key - E key
        """
        count = 0
        data = caseData('testData/{}/KeyChange/key_change_task.json'.format(Project.name))['ChangeKey']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        requestData['payload'][0]['data'][0]['parameter']['KeyType'] = 0
        print(requestData)
        response = HESRequest().post(url=Project.request_url, params=requestData)
        assert response.status_code == 200

        time.sleep(3)
        sql_running = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='CHANGE_KEY'".format(
            setting[Project.name]['meter_no'])
        db_queue = get_database.orcl_fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 3:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for set tariff Tasks to Create...')
            count = count + 1

        sql_his = "select TASK_STATE from H_TASK_RUN_HIS where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 40:
            time.sleep(10)
            db_queue = get_database.orcl_fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for set tariff Tasks to finish...')
            count = count + 1
        assert db_queue[0]['TASK_STATE'] == 3