# -*-coding:utf-8-*-
"""
# File       : test_meter_profile.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import datetime
import time

import requests

from common.HESRequest import HESRequest
from common.marker import *
from config.settings import *


class Test_Meter_Relay_Status:

    @smokeTest
    def test_read_relay_status_sync(self, url, caseData):
        """
        使用同步读取的方式去对电表进行读取闸状态
         """
        data, user_config = caseData('testData/empower/RelayControlTask/read_RelayControlStatus.json')
        requestData = data['ReadRelayControlStatusSync']['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        assert '636F6E6E6563746564' in str(response) or '646973636F6E6E6563746564' in str(response)

    @hesAsyncTest
    def test_read_relay_status_async(self, url, get_database, caseData):
        """
        使用异步读取的方式去对电表进行读取闸状态
         """
        testUrl = url + '/api/v1/Request/RequestMessage'
        count = 0
        print("Step 1 : 生成异步操作读取任务，hes-api异步执行，生成running表")
        data, user_config = caseData('testData/empower/RelayControlTask/read_RelayControlStatus.json')
        requestData = data['ReadRelayControlStatusAsync']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=3)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        response = requests.post(url=testUrl, json=requestData)
        assert response.status_code == 200

        print("Step 2 : 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束")
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(3)
        # 查询生成Core执行的任务的 AUTO_RUN_ID
        sql_running = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='GET_COMMON_PARAM'".format(
            setting[Project.name]['meter_no'])
        db_queue = get_database.orcl_fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 2:
            time.sleep(3)
            db_queue = get_database.orcl_fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for read relay_control Tasks to Create...')
            count = count + 1

        print("Step 3 : 验证读任务执行结束，task正常移入his表")
        # 查询生成Core执行结束后，his表任务状态
        sql_his = "select TASK_STATE from H_TASK_RUN_HIS where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 50:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for read relay_control Tasks to finish...')
            count = count + 1
        assert db_queue[0]['TASK_STATE'] == 3
