# -*-coding:utf-8-*-
"""
# File       : test_meter_daily.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import pytest, allure, time, datetime, requests, random
from common.HESAPI import *
from common.marker import *
from config.settings import *


class Test_Meter_Daily:

    @hesSyncTest
    def test_get_daily_entries(self, caseData):
        """
        使用同步读取的方式去对电表进行日结entries数据对比
        """
        DeviceBusy = 1
        data = caseData('testData/HESAPI/MeterDailyData/meter_daily_data.json')['meter_daily_entries']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504:
                print('504 Error and try again')
                time.sleep(3)
                response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         json=requestData, timeout=40)
            if json.loads(response.text).get('reply')['replyCode'] != 200:
                assert False
            else:
                DeviceBusy == 0
                assert int(json.loads(response.text).get('payload')[0].get('data')[0].get('resultValue').get(
                    'dataItemValue')) == setting[Project.name]['daily_entries']

    @hesSyncTest
    def test_get_daily_date(self, caseData):
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
         """

        print("Step 1 : 获取当前电表第一条日结数据")
        startTime = None
        DeviceBusy = 1
        data = caseData('testData/HESAPI/MeterDailyData/meter_daily_data.json')['meter_daily_data']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504:
                print('504 Error and try again')
                time.sleep(3)
                response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         json=requestData, timeout=40)
                if json.loads(response.text).get('reply')['replyCode'] != 200:
                    assert False
                else:
                    DeviceBusy == 0
                    assert int(json.loads(response.text).get('payload')[0].get('data')[0].get('resultValue').get(
                        'dataItemValue')) == setting[Project.name]['daily_entries']
                    assert len(json.loads(response.text).get('payload')[0].get('data')) != 0
                    assert json.loads(response.text).get('payload')[0].get('data') == setting[Project.name]['daily_len']
                    startTime = json.loads(response.text).get('payload')[0].get('data')[0].get('dataTime')

        print(f"Step 2 : 按照时间获取日结数据")
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
         """

        print("Step 1 : 获取当前电表第一条日结数据")
        DeviceBusy = 1
        data = caseData('testData/HESAPI/MeterDailyData/meter_daily_data.json')['meter_daily_data']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        requestData['payload'][0]['data'][0]['parameter'][0]['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter'][0]['endTime'] = startTime

        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504:
                print('504 Error and try again')
                time.sleep(3)
                response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         json=requestData, timeout=40)
                if json.loads(response.text).get('reply')['replyCode'] != 200:
                    assert False
                else:
                    DeviceBusy == 0
                    assert int(json.loads(response.text).get('payload')[0].get('data')[0].get('resultValue').get(
                        'dataItemValue')) == setting[Project.name]['daily_entries']
                    assert len(json.loads(response.text).get('payload')[0].get('data')) != 0
                    assert json.loads(response.text).get('payload')[0].get('data') == setting[Project.name]['daily_len']


    # def test_get_daily_date_asyn(self, get_project_config):
    #     """
    #     使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
    #      """
    #     startTime = None
    #     print(f"Step 1 Read daily data entries")
    #     transactionId = "test-transactionid" + random.randint(0, 1000000).__str__()
    #     RequestQueue = RequestMessage(correlationId=get_project_config['Request']['correlationId'],
    #                                   messageId=get_project_config['Request']['messageId'],
    #                                   createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
    #                                   serviceType="GET_COMMON",
    #                                   source="MDM",
    #                                   businessType="GET_COMMON",
    #                                   replyAddress=None,
    #                                   asyncReplyFlag="false",
    #                                   deviceNo=get_project_config['Request']['deviceNo'],
    #                                   deviceType=1,
    #                                   retryCount=2,
    #                                   startTime=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
    #                                       "%y%m%d%H%M%S"),
    #                                   endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
    #                                       "%y%m%d%H%M%S"),
    #                                   transactionId=transactionId,
    #                                   parameter={},
    #                                   registerId=get_project_config['Profile']['daily_entries_obis'],
    #                                   jobUniqueFlag="false",
    #                                   accessSelector=1).request_json()
    #     # print(json.dumps(RequestQueue, indent=4))
    #     response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
    #                              headers={"Content-Type": "application/json"},
    #                              data=json.dumps(RequestQueue, indent=4), timeout=40)
    #     # print(response.json())
    #     if response.status_code == 504:
    #         print('504 Error and try again')
    #         time.sleep(5)
    #         response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
    #                                  headers={"Content-Type": "application/json"},
    #                                  data=json.dumps(RequestQueue, indent=4), timeout=40)
    #     if json.loads(response.text).get('reply')['replyCode'] != 200:
    #         # print(json.loads(response.text).get('reply')['replyDesc'])
    #         error(f"** Read Failed **")
    #         return -1
    #     else:
    #         # print(json.loads(response.text).get('reply')['replyDesc'])
    #         print(f"** Read Successfully **")
    #         if int(json.loads(response.text).get('payload')[0].get('data')[0].get('resultValue').get(
    #                 'dataItemValue')) == get_project_config['Profile']['daily_entries']:
    #             print("** Match with Config!")
    #         else:
    #             print("** Mismatch with Config!")
    #
    #     print(f"Step 2 Read the latest entries")
    #     RequestQueue = RequestMessage(correlationId=get_project_config['Request']['correlationId'],
    #                                   messageId=get_project_config['Request']['messageId'],
    #                                   createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
    #                                   serviceType="GET_PROFILE",
    #                                   source="MDM",
    #                                   businessType="GET_PROFILE",
    #                                   replyAddress=None,
    #                                   asyncReplyFlag="false",
    #                                   deviceNo=get_project_config['Request']['deviceNo'],
    #                                   deviceType=1,
    #                                   retryCount=2,
    #                                   startTime=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
    #                                       "%y%m%d%H%M%S"),
    #                                   endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
    #                                       "%y%m%d%H%M%S"),
    #                                   transactionId=transactionId,
    #                                   parameter={"dataFetchMode": 2, "readTarget": 0, "startTime": "", "endTime": "",
    #                                              "fromEntry": "1", "toEntry": "1", "fromSelectedValue": 1,
    #                                              "toSelectedValue": 0},
    #                                   registerId=get_project_config['Profile']['daily_obis'], jobUniqueFlag="false",
    #                                   accessSelector=1).request_json()
    #     response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
    #                              headers={"Content-Type": "application/json"},
    #                              data=json.dumps(RequestQueue, indent=4), timeout=40)
    #     if response.status_code == 504:
    #         print('504 Error and try again')
    #         time.sleep(5)
    #         response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
    #                                  headers={"Content-Type": "application/json"},
    #                                  data=json.dumps(RequestQueue, indent=4), timeout=40)
    #
    #         assert json.loads(response.text).get('reply')['replyCode'] == 200
    #         assert len(json.loads(response.text).get('payload')[0].get('data')) != 0
    #         assert json.loads(response.text).get('payload')[0].get('data') == get_project_config['Profile']['daily_len']
    #         startTime = json.loads(response.text).get('payload')[0].get('data')[0].get('dataTime')
    #
    #     info(f"Step 3 Read the data by date")
    #     RequestQueue = RequestMessage(correlationId=get_project_config['Request']['correlationId'],
    #                                   messageId=get_project_config['Request']['messageId'],
    #                                   createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
    #                                   serviceType="GET_PROFILE",
    #                                   source="MDM",
    #                                   businessType="GET_PROFILE",
    #                                   replyAddress=None,
    #                                   asyncReplyFlag="false",
    #                                   deviceNo=get_project_config['Request']['deviceNo'],
    #                                   deviceType=1,
    #                                   retryCount=2,
    #                                   startTime=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
    #                                       "%y%m%d%H%M%S"),
    #                                   endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
    #                                       "%y%m%d%H%M%S"),
    #                                   transactionId=transactionId,
    #                                   parameter={"dataFetchMode": 1, "readTarget": 0, "startTime": startTime,
    #                                              "endTime": startTime,
    #                                              "fromEntry": "1", "toEntry": "2", "fromSelectedValue": 1,
    #                                              "toSelectedValue": 0},
    #                                   registerId=get_project_config['Profile']['daily_obis'], jobUniqueFlag="false",
    #                                   accessSelector=1).request_json()
    #     response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
    #                              headers={"Content-Type": "application/json"},
    #                              data=json.dumps(RequestQueue, indent=4), timeout=40)
    #     if response.status_code == 504:
    #         print('504 Error and try again')
    #         time.sleep(5)
    #         response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
    #                                  headers={"Content-Type": "application/json"},
    #                                  data=json.dumps(RequestQueue, indent=4), timeout=40)
    #
    #     assert json.loads(response.text).get('reply')['replyCode'] == 200
    #     assert len(json.loads(response.text).get('payload')[0].get('data')) != 0
    #     assert json.loads(response.text).get('payload')[0].get('data') == get_project_config['Profile']['daily_len']
