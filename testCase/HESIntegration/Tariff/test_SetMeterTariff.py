# -*- coding: utf-8 -*-
# @Time : 2021/12/23 11:09
# @Author : JingYang
# @File : test_SetMeterTariff.py
from common.marker import *
from config.settings import *
import allure, pytest, requests, logging, time, datetime

class Test_SetMeterTariff:

    @hesAsyncTest
    def test_SetMeterTariff(self,url,get_database,caseData):

        testUrl = url + '/api/v1/Request/RequestMessage'
        count = 0
        # Step1 生成异步操作读取任务，hes-api，生成running表
        data = caseData('testData/{}/Tariff/setMeterTariff.json'.format(Project.name))['test_SetMeterTariff']
        requestData = data['request']
        # 设定三分钟异步任务，三分钟后失效
        currentTime = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        endTime = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime('%y%m%d%H%M%S')

        requestData['payload'][0]['startTime'] = currentTime
        requestData['payload'][0]['endTime'] = endTime
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        response = requests.post(url=testUrl, json=requestData)
        assert response.status_code == 200

        # Step2 生成异步任务后，任务正常执行完毕进入his，进入his表，则认为任务结束
        # 过期时间到，也会进入his表，这里暂不考虑
        time.sleep(3)
        #查询生成Core执行的任务的 AUTO_RUN_ID
        sql_running = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='SET_TARIFF_CONTENT'".format(setting[Project.name]['meter_no'])
        db_queue = get_database.orcl_fetchall_dict(sql_running)
        while len(db_queue) == 0 and count < 5:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql_running)
            print(db_queue)
            print('Waiting for set tariff Tasks to Create...')
            count = count + 1

        # Step3 验证读任务执行结束，task正常移入his表
        # 查询生成Core执行结束后，his表任务状态
        sql_his = "select TASK_STATE from H_TASK_RUN_HIS where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql_his)
        while len(db_queue) == 0 and count < 40:
            time.sleep(10)
            db_queue = get_database.orcl_fetchall_dict(sql_his)
            print(db_queue)
            print('Waiting for set tariff Tasks to finish...')
            count = count + 1
        assert db_queue[0]['TASK_STATE'] == 3