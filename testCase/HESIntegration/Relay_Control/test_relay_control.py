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

from common.HESRequest import *
from common.marker import *


class Test_Relay_Control:

    @smokeTest
    def test_relay_on_standard_1(self, requestMessage, device, caseData):
        """
        同步标准合闸 - 合闸状态去合闸
         """
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RELAY_CONTROL_RELAYON']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert 'CONNECTED' in str(response)
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert 'CONNECTED' in str(response)

    @smokeTest
    def test_relay_on_standard_2(self, requestMessage, device, caseData):
        """
        同步标准合闸 - 拉闸状态去合闸
         """
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RELAY_CONTROL_RELAYOFF']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert 'DISCONNECTED' in str(response)
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RELAY_CONTROL_RELAYON']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert 'CONNECTED' in str(response)

    @smokeTest
    def test_relay_off_standard_1(self, requestMessage, device, caseData):
        """
        同步标准拉闸 - 合闸状态去拉闸
         """
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RELAY_CONTROL_RELAYON']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert 'CONNECTED' in str(response)
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RELAY_CONTROL_RELAYOFF']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert 'DISCONNECTED' in str(response)

    @smokeTest
    def test_relay_off_standard_2(self, requestMessage, device, caseData):
        """
        同步标准拉闸 - 拉闸状态去拉闸
         """
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RELAY_CONTROL_RELAYOFF']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert 'DISCONNECTED' in str(response)
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert 'DISCONNECTED' in str(response)
        # assert AssertIn().checkIn(expectResJson, response.json()) is True

    @smokeTest
    def test_relay_on_home(self, requestMessage, device, caseData):
        """
        调用Home界面合闸接口
         """
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_relay_on_home_sync']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert "CONNECTED" in str(response)

    @smokeTest
    def test_relay_off_home(self, requestMessage, device, caseData):
        """
        调用Home界面拉闸接口
         """
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_relay_off_home_sync']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert "DISCONNECTED" in str(response)

    @asyncTest
    def test_relay_on_task(self, requestMessage, device, dbConnect, caseData):
        """
        调用异步Relay Control
         """
        count = 0
        # Step1 生成异步操作读取任务，hes-api异步执行，生成running表
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RelayControl_OnTask']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response = requests.post(url=requestMessage, json=requestData)
        assert response.status_code == 200

        # Step2 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(5)
        # 查询生成Core执行的任务的 auto_run_id
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='RELAY_CONTROL'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 2:
            time.sleep(5)
            db_queue = dbConnect.fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for read relay_control Tasks to Create...')
            count = count + 1

        # Step3 验证读任务执行结束，task正常移入his表
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

    @asyncTest
    def test_relay_off_task(self, requestMessage, device, dbConnect, caseData):
        """
        调用异步Relay Control
         """
        count = 0
        # Step1 生成异步操作读取任务，hes-api异步执行，生成running表
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RelayControl_OffTask']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response = requests.post(url=requestMessage, json=requestData)
        assert response.status_code == 200

        # Step2 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(5)
        # 查询生成Core执行的任务的 auto_run_id
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='RELAY_CONTROL'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 2:
            time.sleep(5)
            db_queue = dbConnect.fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for read relay_control Tasks to Create...')
            count = count + 1

        # Step3 验证读任务执行结束，task正常移入his表
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

    @asyncTest
    def test_relay_on_task_billing(self, requestMessage, device, dbConnect, caseData):
        """
        调用异步Relay Control
         """
        count = 0
        # Step1 生成异步操作读取任务，hes-api异步执行，生成running表
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RelayControl_OnTask']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response = requests.post(url=requestMessage, json=requestData)
        assert response.status_code == 200

        # Step2 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(5)
        # 查询生成Core执行的任务的 auto_run_id
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='RELAY_CONTROL'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 2:
            time.sleep(5)
            db_queue = dbConnect.fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for read relay_control Tasks to Create...')
            count = count + 1

        # Step3 验证读任务执行结束，task正常移入his表
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

    @asyncTest
    def test_relay_off_task_billing(self, requestMessage, device, dbConnect, caseData):
        """
        调用异步Relay Control
         """
        count = 0
        # Step1 生成异步操作读取任务，hes-api异步执行，生成running表
        data = caseData('testData/RelayControlTask/relayControl.json')
        requestData = data['test_RelayControl_OffTask']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response = requests.post(url=requestMessage, json=requestData)
        assert response.status_code == 200

        # Step2 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(5)
        # 查询生成Core执行的任务的 auto_run_id
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='RELAY_CONTROL'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 2:
            time.sleep(5)
            db_queue = dbConnect.fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for read relay_control Tasks to Create...')
            count = count + 1

        # Step3 验证读任务执行结束，task正常移入his表
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
