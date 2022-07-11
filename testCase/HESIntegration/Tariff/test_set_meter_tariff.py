# -*- coding: utf-8 -*-
# @Time : 2021/12/23 11:09
# @Author : JingYang
# @File : test_SetMeterTariff.py
import datetime
import time

import requests

from common.marker import *


class Test_Set_Meter_Tariff:

    @asyncTest
    def test_SetMeterTariff(self, requestMessage, dbConnect,device, caseData):
        """使用异步方式设置测试费率到电表"""
        count = 0
        # Step1 生成异步操作读取任务，hes-api，生成running表
        data = caseData('testData/Tariff/setMeterTariff.json')
        requestData = data['test_SetMeterTariff']['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response = requests.post(url=requestMessage, json=requestData)
        assert response.status_code == 200

        # Step2 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(3)
        # 查询生成Core执行的任务的 auto_run_id
        sql_running = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='SET_TARIFF_CONTENT'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 5:
            time.sleep(5)
            db_queue = dbConnect.fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for set tariff Tasks to Create...')
            count = count + 1

        # Step3 验证读任务执行结束，task正常移入his表
        # 查询生成Core执行结束后，his表任务状态
        sql_his = "select task_state from H_TASK_RUN_HIS where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
        db_queue = dbConnect.fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 40:
            time.sleep(10)
            db_queue = dbConnect.fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for set tariff Tasks to finish...')
            count = count + 1
        assert db_queue[0]['task_state'] == 3
