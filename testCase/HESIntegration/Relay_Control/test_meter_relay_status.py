# -*-coding:utf-8-*-
"""
# File       : test_meter_profile.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import datetime

from common.HESRequest import *
from common.marker import *


class Test_Meter_Relay_Status:

    @smokeTest
    def test_read_relay_status_sync(self, requestMessage, caseData, device):
        """
        使用同步读取的方式去对电表进行读取闸状态
         """
        data = caseData('testData/RelayControlTask/read_RelayControlStatus.json')
        requestData = data['ReadRelayControlStatusSync']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Request ---  ', response)
        assert '636F6E6E6563746564' in str(response) or '646973636F6E6E6563746564' in str(response)

    @asyncTest
    def test_read_relay_status_async(self, device, requestMessage, dbConnect, caseData):
        """
        使用异步读取的方式去对电表进行读取闸状态
         """
        count = 0
        print("Step 1 : 生成异步操作读取任务，hes-api异步执行，生成running表")
        data = caseData('testData/RelayControlTask/read_RelayControlStatus.json')
        requestData = data['ReadRelayControlStatusAsync']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=3)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response = requests.post(url=requestMessage, json=requestData)
        assert response.status_code == 200

        print("Step 2 : 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束")
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(3)
        # 查询生成Core执行的任务的 auto_run_id
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='GET_COMMON_PARAM'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 2:
            time.sleep(3)
            db_queue = dbConnect.fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for read relay_control Tasks to Create...')
            count = count + 1

        print("Step 3 : 验证读任务执行结束，task正常移入his表")
        # 查询生成Core执行结束后，his表任务状态
        sql_his = "select task_state from H_TASK_RUN_HIS where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
        db_queue = dbConnect.fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 50:
            time.sleep(5)
            db_queue = dbConnect.fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for read relay_control Tasks to finish...')
            count = count + 1
        assert db_queue[0]['task_state'] == 3
