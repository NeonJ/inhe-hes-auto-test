# -*-coding:utf-8-*-
"""
# File       : test_schedule_setting.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import time

import allure
import requests
from faker import Faker

from common.DB import *
from common.marker import *

faker = Faker(locale='en_US')


class Test_Schedule_Setting:

    @asyncTest
    def test_meter_schedule_setting_daily(self, gatewayURL, dbConnect, token, get_daily_date, device):
        """
        验证chedule Setting生成采集GPRS电表日结
        """
        count = 1
        with allure.step('添加电表日结采集任务'):
            scheduleName = "AutoHES-Daily" + faker.name()
            url = gatewayURL + '/api/hes-service/schedule.json'
            etime = datetime.datetime.strptime(get_daily_date, "%y%m%d%H%M%S")
            sstime = (etime - datetime.timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S')
            eetime = etime.strftime('%d/%m/%Y %H:%M:%S')
            data = {
                "taskType": "ProfileRD",
                "scheduleType": "TEMPORARY",
                "taskObjectType": "METER",
                "deviceType": "METER",
                "frequencyInterval": 1,
                "frequencyUnit": "DAY",
                "delayTimeHour": 2,
                "delayTimeMin": 10,
                "retryTimes": 3,
                "retryInterval": 1,
                "isAdd": "true",
                "taskTypeName": "Read Daily",
                "taskTypeNameI18nCode": "view.read_daily",
                "desc": "AutoTest",
                "delayExecutionTime": 130,
                "profileType": "DAILY",
                "scheduleName": scheduleName,
                "startTime": sstime,  # "25/12/2021 00:00:00"
                "endTime": eetime  # "27/12/2021 00:00:00"
            }
            response = requests.post(url=url, headers=token, json=data)
            assert response.status_code == 200
            assert response.json()['code'] == 200

        with allure.step('获取任务schedule ID'):
            url = gatewayURL + '/api/hes-service/schedule.json'
            data = 'pageNo=1&pageSize=20&scheduleName={}'.format(scheduleName)
            re = requests.get(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            schedule_id = re.json()['data']['pageData'][0]['scheduleId']

        with allure.step('获取电表object ID'):
            sql = "select  meter_id,install_meter_no from C_AR_METER_PNT where  DEV_STATUS=4 and FULL_AREA_ID is not null  and COMMUNICATION_TYPE !=0 and  install_meter_no='{}'".format(
                device['device_number'])
            object_id = dbConnect.fetchall_dict(sql)[0]['meter_id']
            meter_no = dbConnect.fetchall_dict(sql)[0]['install_meter_no']

        with allure.step('添加设备到Task'):
            url = gatewayURL + '/api/hes-service/schedule/object/{}'.format(schedule_id)
            data = {"taskObjectType": "METER", "scheduleObjectList": [{"objectId": object_id, "objectNo": meter_no}]}
            re = requests.post(url, json=data, headers=token)

            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('执行任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {"scheduleId": schedule_id, "scheduleName": scheduleName,
                    "startTime": sstime, "endTime": eetime}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('查看生成任务是否正确'):
            url = gatewayURL + '/api/hes-service/schedule/task/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType='
            sql1 = "select * from H_CONFIG_PRODUCT_PROFILE where PROFILE_TYPE=1 and PRODUCT_CODE=(select PRODUCT_CODE from c_ar_meter where METER_NO='{}')".format(
                device['device_number'])
            obis = dbConnect.fetchall_dict(sql1)
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 20:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.json()['data']['totalRow'] == len(obis)
            # assert obis in re.json()['data']['pageData'][0]['remark']  可以添加采集profiel obis的对比

        with allure.step('查看任务执行状态'):
            url = gatewayURL + '/api/hes-service/schedule/task/history/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType=&startGenerateTime{}&endGenerateTime={}'.format(
                (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
                (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y'))
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 20:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.status_code == 200
            assert re.json()['code'] == 200
            print(re.json())
            assert re.json()['data']['pageData'][0]['taskStatus'] == 'SUCCESS'

    @asyncTest
    def test_meter_schedule_setting_monthly(self, gatewayURL, dbConnect, token, get_monthly_date, device):
        """
        验证Schedule Setting生成采集GPRS电表月结
        """
        count = 1
        with allure.step('添加电表月结采集任务'):
            scheduleName = "AutoHES-Monthly" + faker.name()
            url = gatewayURL + '/api/hes-service/schedule.json'
            etime = datetime.datetime.strptime(get_monthly_date, "%y%m%d%H%M%S")
            sstime = (etime - datetime.timedelta(days=15)).strftime('%d/%m/%Y %H:%M:%S')
            eetime = (etime).strftime('%d/%m/%Y %H:%M:%S')
            data = {
                "taskType": "ProfileRM",
                "scheduleType": "TEMPORARY",
                "taskObjectType": "METER",
                "deviceType": "METER",
                "frequencyInterval": 1,
                "frequencyUnit": "MONTH",
                "delayTimeHour": 2,
                "delayTimeMin": 10,
                "retryTimes": 3,
                "retryInterval": 1,
                "isAdd": "true",
                "taskTypeName": "Read Monthly",
                "taskTypeNameI18nCode": "view.read_monthly",
                "desc": "AutoTest",
                "delayExecutionTime": 130,
                "profileType": "MONTHLY",
                "scheduleName": scheduleName,
                "scheduleTypeFilter": "ALL",
                "startTime": sstime,  # "25/12/2021 00:00:00"
                "endTime": eetime  # "27/12/2021 00:00:00"
            }
            print(data)
            response = requests.post(url=url, headers=token, json=data)
            assert response.status_code == 200
            assert response.json()['code'] == 200

        with allure.step('获取任务schedule ID'):
            url = gatewayURL + '/api/hes-service/schedule.json'
            data = 'pageNo=1&pageSize=20&scheduleName={}'.format(scheduleName)
            re = requests.get(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            schedule_id = re.json()['data']['pageData'][0]['scheduleId']

        with allure.step('获取电表object ID'):
            sql = "select  meter_id,install_meter_no from C_AR_METER_PNT where  DEV_STATUS=4 and FULL_AREA_ID is not null  and COMMUNICATION_TYPE !=0 and  install_meter_no='{}'".format(
                device['device_number'])
            object_id = dbConnect.fetchall_dict(sql)[0]['meter_id']
            meter_no = dbConnect.fetchall_dict(sql)[0]['install_meter_no']
            print(object_id, meter_no)

        with allure.step('添加设备到Task'):
            url = gatewayURL + '/api/hes-service/schedule/object/{}'.format(schedule_id)
            data = {"taskObjectType": "METER", "scheduleObjectList": [{"objectId": object_id, "objectNo": meter_no}]}
            re = requests.post(url, json=data, headers=token)

            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('执行任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {"scheduleId": schedule_id, "scheduleName": scheduleName,
                    "startTime": sstime, "endTime": eetime}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('查看生成任务是否正确'):
            url = gatewayURL + '/api/hes-service/schedule/task/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType='
            sql1 = "select * from H_CONFIG_PRODUCT_PROFILE where PROFILE_TYPE=2 and PRODUCT_CODE=(select PRODUCT_CODE from c_ar_meter where METER_NO='{}')".format(
                device['device_number'])
            obis = dbConnect.fetchall_dict(sql1)
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 30:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.json()['data']['totalRow'] == len(obis)
            # assert obis in re.json()['data']['pageData'][0]['remark']  可以添加采集profiel obis的对比

        with allure.step('查看任务执行状态'):
            url = gatewayURL + '/api/hes-service/schedule/task/history/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType=&startGenerateTime{}&endGenerateTime={}'.format(
                (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
                (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y'))
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 40:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['data']['pageData'][0]['taskStatus'] == 'SUCCESS'

    @asyncTest
    def test_meter_schedule_setting_lp(self, gatewayURL, dbConnect, token, get_lp_date, device):
        """
        验证Schedule Setting生成采集GPRS电表曲线
        """
        count = 1
        with allure.step('添加电表曲线采集任务'):
            scheduleName = "AutoHES-LP" + faker.name()
            url = gatewayURL + '/api/hes-service/schedule.json'
            etime = datetime.datetime.strptime(get_lp_date, "%y%m%d%H%M%S")
            sstime = (etime - datetime.timedelta(hours=1)).strftime('%d/%m/%Y %H:%M:%S')
            eetime = (etime + datetime.timedelta(hours=1)).strftime('%d/%m/%Y %H:%M:%S')
            data = {
                "taskType": "ProfileRP",
                "scheduleType": "TEMPORARY",
                "taskObjectType": "METER",
                "deviceType": "METER",
                "frequencyInterval": 60,
                "frequencyUnit": "MIN",
                "delayTimeHour": 2,
                "delayTimeMin": 10,
                "retryTimes": 3,
                "retryInterval": 1,
                "isAdd": "true",
                "taskTypeName": "Read Profile",
                "taskTypeNameI18nCode": "view.read_profile",
                "desc": "AutoTest",
                "delayExecutionTime": 130,
                "profileType": "ELP",
                "scheduleName": scheduleName,
                "startTime": sstime,  # "25/12/2021 00:00:00"
                "endTime": eetime  # "27/12/2021 00:00:00"
            }
            response = requests.post(url=url, headers=token, json=data)
            assert response.status_code == 200
            assert response.json()['code'] == 200

        with allure.step('获取任务schedule ID'):
            url = gatewayURL + '/api/hes-service/schedule.json'
            data = 'pageNo=1&pageSize=20&scheduleName={}'.format(scheduleName)
            re = requests.get(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            schedule_id = re.json()['data']['pageData'][0]['scheduleId']

        with allure.step('获取电表object ID'):
            sql = "select  meter_id,install_meter_no from C_AR_METER_PNT where  DEV_STATUS=4 and FULL_AREA_ID is not null  and COMMUNICATION_TYPE !=0 and  install_meter_no='{}'".format(
                device['device_number'])
            object_id = dbConnect.fetchall_dict(sql)[0]['meter_id']
            meter_no = dbConnect.fetchall_dict(sql)[0]['install_meter_no']
            print(object_id, meter_no)

        with allure.step('添加设备到Task'):
            url = gatewayURL + '/api/hes-service/schedule/object/{}'.format(schedule_id)
            data = {"taskObjectType": "METER", "scheduleObjectList": [{"objectId": object_id, "objectNo": meter_no}]}
            re = requests.post(url, json=data, headers=token)

            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('执行任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {"scheduleId": schedule_id, "scheduleName": scheduleName,
                    "startTime": sstime, "endTime": eetime}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('查看生成任务是否正确'):
            url = gatewayURL + '/api/hes-service/schedule/task/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType='
            sql1 = "select * from H_CONFIG_PRODUCT_PROFILE where PROFILE_TYPE=3 and PRODUCT_CODE=(select PRODUCT_CODE from c_ar_meter where METER_NO='{}')".format(
                device['device_number'])
            obis = dbConnect.fetchall_dict(sql1)
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 20:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.json()['data']['totalRow'] == len(obis)
            # assert obis in re.json()['data']['pageData'][0]['remark']  可以添加采集profiel obis的对比

        with allure.step('查看任务执行状态'):
            url = gatewayURL + '/api/hes-service/schedule/task/history/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType=&startGenerateTime{}&endGenerateTime={}'.format(
                (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
                (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y'))
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 20:
                re = requests.get(url, json=data, headers=token)
                time.sleep(15)
                count = count + 1
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['data']['pageData'][0]['taskStatus'] == 'SUCCESS'

    @asyncTest
    def test_meter_schedule_setting_daily_event(self, gatewayURL, dbConnect, token, get_daily_event, device):
        """
        验证Schedule Setting生成采集GPRS电表日事件
        """
        count = 1
        with allure.step('添加电表日结采集任务'):
            scheduleName = "AutoHES-Daily-FreezeEvent" + faker.name()
            url = gatewayURL + '/api/hes-service/schedule.json'
            etime = datetime.datetime.strptime(get_daily_event, "%y%m%d%H%M%S")
            sstime = (etime - datetime.timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S')
            eetime = (etime + datetime.timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S')
            data = {
                "taskType": "ProfileREFreeze",
                "scheduleType": "TEMPORARY",
                "taskObjectType": "METER",
                "deviceType": "METER",
                "frequencyInterval": 1,
                "frequencyUnit": "DAY",
                "delayTimeHour": 2,
                "delayTimeMin": 10,
                "retryTimes": 3,
                "retryInterval": 1,
                "isAdd": "true",
                "taskTypeName": "Read FreezeEvent",
                "taskTypeNameI18nCode": "view.read_freezeevent",
                "desc": "AutoTest",
                "delayExecutionTime": 130,
                "profileType": "EVENT",
                "scheduleName": scheduleName,
                "startTime": sstime,  # "25/12/2021 00:00:00"
                "endTime": eetime  # "27/12/2021 00:00:00"
            }
            response = requests.post(url=url, headers=token, json=data)
            assert response.status_code == 200
            assert response.json()['code'] == 200

        with allure.step('获取任务schedule ID'):
            url = gatewayURL + '/api/hes-service/schedule.json'
            data = 'pageNo=1&pageSize=20&scheduleName={}'.format(scheduleName)
            re = requests.get(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            schedule_id = re.json()['data']['pageData'][0]['scheduleId']

        with allure.step('获取电表object ID'):
            sql = "select  meter_id,install_meter_no from C_AR_METER_PNT where  DEV_STATUS=4 and FULL_AREA_ID is not null  and COMMUNICATION_TYPE !=0 and  install_meter_no='{}'".format(
                device['device_number'])
            object_id = dbConnect.fetchall_dict(sql)[0]['meter_id']
            meter_no = dbConnect.fetchall_dict(sql)[0]['install_meter_no']
            print(object_id, meter_no)

        with allure.step('添加设备到Task'):
            url = gatewayURL + '/api/hes-service/schedule/object/{}'.format(schedule_id)
            data = {"taskObjectType": "METER", "scheduleObjectList": [{"objectId": object_id, "objectNo": meter_no}]}
            re = requests.post(url, json=data, headers=token)

            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('执行任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {"scheduleId": schedule_id, "scheduleName": scheduleName,
                    "startTime": sstime, "endTime": eetime}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('查看生成任务是否正确'):
            url = gatewayURL + '/api/hes-service/schedule/task/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType='
            sql1 = "select * from H_CONFIG_PRODUCT_PROFILE where PROFILE_TYPE=5 and PRODUCT_CODE=(select PRODUCT_CODE from c_ar_meter where METER_NO='{}')".format(
                device['device_number'])
            obis = dbConnect.fetchall_dict(sql1)
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 20:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.json()['data']['totalRow'] == len(obis)
            # assert obis in re.json()['data']['pageData'][0]['remark']  可以添加采集profiel obis的对比

        with allure.step('查看任务执行状态'):
            url = gatewayURL + '/api/hes-service/schedule/task/history/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType=&startGenerateTime{}&endGenerateTime={}'.format(
                (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
                (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y'))
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 20:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['data']['pageData'][0]['taskStatus'] == 'SUCCESS'

    @asyncTest
    def test_meter_schedule_setting_st(self, dbConnect, token, gatewayURL, device):
        """
        验证Schedule Setting生成区域GPRS校时任务
        """
        count = 1
        with allure.step('添加电表日结采集任务'):
            scheduleName = "AutoHES-ST" + faker.name()
            url = gatewayURL + '/api/hes-service/schedule.json'
            sstime = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S')
            data = {
                "taskType": "SetTime",
                "scheduleType": "PERIODIC",
                "taskObjectType": "REGION",
                "deviceType": "GPRS_METER",
                "frequencyInterval": 1,
                "frequencyUnit": "DAY",
                "delayTimeHour": 2,
                "delayTimeMin": 10,
                "retryTimes": 3,
                "retryInterval": 1,
                "isAdd": "true",
                "taskTypeName": "Set Time",
                "taskTypeNameI18nCode": "view.set_time",
                "desc": "AutoTest",
                "delayExecutionTime": 130,
                "profileType": "SET_TIME",
                "scheduleName": scheduleName,
                "startTime": sstime  # "25/12/2021 00:00:00"
            }
            response = requests.post(url=url, headers=token, json=data)
            assert response.status_code == 200
            assert response.json()['code'] == 200

        with allure.step('获取任务schedule ID'):
            url = gatewayURL + '/api/hes-service/schedule.json'
            data = 'pageNo=1&pageSize=20&scheduleName={}'.format(scheduleName)
            re = requests.get(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            schedule_id = re.json()['data']['pageData'][0]['scheduleId']

        with allure.step('获取区域TR object ID'):
            sql = "select FUNC_GET_TR_REGION_ID(FULL_AREA_ID) ID from c_ar_meter_pnt where install_meter_no='{}'".format(
                device['device_number'])
            object_id = dbConnect.fetchall_dict(sql)[0]['id']

        with allure.step('添加TR到Task'):
            url = gatewayURL + '/api/hes-service/schedule/object/{}'.format(schedule_id)
            data = {"taskObjectType": "REGION", "scheduleObjectList": [{"objectId": object_id}]}
            re = requests.post(url, json=data, headers=token)

            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('执行任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {"scheduleId": schedule_id, "scheduleName": scheduleName,
                    "startTime": sstime}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('查看生成任务和执行结果'):
            sql1 = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='SetTime'".format(
                device['device_number'])
            db_queue = dbConnect.fetchall_dict(sql1)
            while len(db_queue) == 0 and count < 20:
                time.sleep(10)
                db_queue = dbConnect.fetchall_dict(sql1)
                print(db_queue)
                print('Waiting for Reg Tasks to Create...')
                count = count + 1

            sql2 = "select task_state from h_task_run_his where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
            db_queue = dbConnect.fetchall_dict(sql2)
            while len(db_queue) == 0 and count < 30:
                time.sleep(10)
                db_queue = dbConnect.fetchall_dict(sql2)
                print(db_queue)
                print('Waiting for Reg Tasks to finish...')
                count = count + 1
            assert db_queue[0]['task_state'] == 3

        with allure.step('停止周期任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

    @asyncTest
    def test_meter_schedule_setting_event(self, gatewayURL, dbConnect, token, get_event_standard,device):
        """
        验证Schedule Setting生成采集GPRS电表事件采集
        """
        count = 1
        with allure.step('添加电表事件采集任务'):
            scheduleName = "AutoHES-Event" + faker.name()
            url = gatewayURL + '/api/hes-service/schedule.json'
            etime = datetime.datetime.strptime(get_event_standard, "%y%m%d%H%M%S")
            sstime = (etime - datetime.timedelta(hours=12)).strftime('%d/%m/%Y %H:%M:%S')
            eetime = (etime).strftime('%d/%m/%Y %H:%M:%S')
            data = {
                "taskType": "ProfileRE",
                "scheduleType": "TEMPORARY",
                "taskObjectType": "METER",
                "deviceType": "METER",
                "frequencyInterval": 1,
                "frequencyUnit": "DAY",
                "delayTimeHour": 2,
                "delayTimeMin": 10,
                "retryTimes": 3,
                "retryInterval": 1,
                "isAdd": "true",
                "taskTypeName": "Read Event",
                "taskTypeNameI18nCode": "view.read_event",
                "desc": "AutoTest",
                "delayExecutionTime": 130,
                "profileType": "SIMPLE_EVENT",
                "scheduleName": scheduleName,
                "startTime": sstime,  # "25/12/2021 00:00:00"
                "endTime": eetime  # "27/12/2021 00:00:00"
            }
            response = requests.post(url=url, headers=token, json=data)
            assert response.status_code == 200
            assert response.json()['code'] == 200

        with allure.step('获取任务schedule ID'):
            url = gatewayURL + '/api/hes-service/schedule.json'
            data = 'pageNo=1&pageSize=20&scheduleName={}'.format(scheduleName)
            re = requests.get(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            schedule_id = re.json()['data']['pageData'][0]['scheduleId']

        with allure.step('获取电表object ID'):
            sql = "select  meter_id,install_meter_no from C_AR_METER_PNT where  DEV_STATUS=4 and FULL_AREA_ID is not null  and COMMUNICATION_TYPE !=0 and  install_meter_no='{}'".format(
                device['device_number'])
            object_id = dbConnect.fetchall_dict(sql)[0]['meter_id']
            meter_no = dbConnect.fetchall_dict(sql)[0]['install_meter_no']
            print(object_id, meter_no)

        with allure.step('添加设备到Task'):
            url = gatewayURL + '/api/hes-service/schedule/object/{}'.format(schedule_id)
            data = {"taskObjectType": "METER", "scheduleObjectList": [{"objectId": object_id, "objectNo": meter_no}]}
            re = requests.post(url, json=data, headers=token)

            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('执行任务'):
            url = gatewayURL + '/api/hes-service/schedule/status/{}'.format(schedule_id)
            data = {"scheduleId": schedule_id, "scheduleName": scheduleName,
                    "startTime": sstime, "endTime": eetime}
            re = requests.put(url, json=data, headers=token)
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['desc'] == 'OK'

        with allure.step('查看生成任务是否正确'):
            url = gatewayURL + '/api/hes-service/schedule/task/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType='
            sql1 = "select * from H_CONFIG_PRODUCT_PROFILE where PROFILE_TYPE=4 and PRODUCT_CODE=(select PRODUCT_CODE from c_ar_meter where METER_NO='{}')".format(
                device['device_number'])
            obis = dbConnect.fetchall_dict(sql1)
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 30:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.json()['data']['totalRow'] == len(obis) * 2
            # assert obis in re.json()['data']['pageData'][0]['remark']  可以添加采集profiel obis的对比

        with allure.step('查看任务执行状态'):
            url = gatewayURL + '/api/hes-service/schedule/task/history/{}.json'.format(schedule_id)
            data = 'taskStatus=&pageNo=1&pageSize=20&deviceType=METER&scheduleFilterDeviceType=&startGenerateTime{}&endGenerateTime={}'.format(
                (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
                (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y'))
            re = requests.get(url, json=data, headers=token)
            while re.json()['data']['pageData'] == [] and count < 45:
                re = requests.get(url, json=data, headers=token)
                time.sleep(10)
                count = count + 1
            assert re.status_code == 200
            assert re.json()['code'] == 200
            assert re.json()['data']['pageData'][0]['taskStatus'] == 'SUCCESS'
