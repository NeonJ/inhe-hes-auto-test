# -*-coding:utf-8-*-
"""
# File       : test_meter_profile.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import pytest, allure, time, datetime, requests, random
from common.HESAPI import *
from common.marker import *
from config.settings import *


class Test_Meter_Monthly:

    @hesSyncTest
    def test_get_monthly_entries(self, caseData):
        """
        使用同步读取的方式去对电表进行日结entries数据对比
        """
        DeviceBusy = 1
        data = caseData('testData/HESAPI/MeterFrozenData/meter_monthly_data.json')['meter_monthly_entries']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504 or json.loads(response.text).get('payload')[0].get(
                    'desc') == 'Device Busying !':
                print('504 Error and try again')
                time.sleep(3)
                response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         json=requestData, timeout=40)
                continue
            if json.loads(response.text).get('reply')['replyCode'] != 200:
                assert False
            else:
                DeviceBusy = 0
                assert int(json.loads(response.text).get('payload')[0].get('data')[0].get('resultValue').get(
                    'dataItemValue')) == setting[Project.name]['monthly_entries']

    @hesSyncTest
    def test_get_monthly_date(self, caseData):
        """
        使用同步读取的方式去对电表进行月结读取 - 按照Entry+Date方式进行并进行数据项对比
         """

        print("Step 1 : 获取当前电表第一条月结数据")
        startTime = None
        DeviceBusy = 1
        data = caseData('testData/HESAPI/MeterFrozenData/meter_monthly_data.json')['meter_monthly_data']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504 or json.loads(response.text).get('payload')[0].get(
                    'desc') == 'Device Busying !':
                print('504 Error and try again')
                time.sleep(3)
                response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         json=requestData, timeout=40)
                continue
            if json.loads(response.text).get('reply')['replyCode'] != 200:
                assert False
            else:
                DeviceBusy = 0
                assert len(json.loads(response.text).get('payload')[0].get('data')) == setting[Project.name][
                    'monthly_len']
                startTime = json.loads(response.text).get('payload')[0].get('data')[0].get('dataTime')

        print(f"Step 2 : 按照时间获取月结数据")
        """
        使用同步读取的方式去对电表进行月结读取 - 按照Entry+Date方式进行并进行数据项对比
         """
        DeviceBusy = 1
        data = caseData('testData/HESAPI/MeterFrozenData/meter_monthly_data.json')['meter_monthly_data']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        requestData['payload'][0]['data'][0]['parameter']['dataFetchMode'] = 1
        requestData['payload'][0]['data'][0]['parameter']['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter']['endTime'] = startTime

        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504 or json.loads(response.text).get('payload')[0].get(
                    'desc') == 'Device Busying !':
                print('504 Error and try again')
                time.sleep(3)
                response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         json=requestData, timeout=40)
                continue
            if json.loads(response.text).get('reply')['replyCode'] != 200:
                assert False
            else:
                DeviceBusy = 0
                assert len(json.loads(response.text).get('payload')[0].get('data')) == setting[Project.name][
                    'monthly_len']