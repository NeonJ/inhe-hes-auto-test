# -*-coding:utf-8-*-
"""
# File       : test_meter_daily.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
from common.HESRequest import HESRequest
from common.marker import *
from config.settings import *


class Test_Meter_Daily:

    @smokeTest1
    def test_get_daily_entries(self, caseData):
        """
        使用同步读取的方式去对电表进行日结entries数据对比
        """
        data, user_config = caseData('testData/empower/MeterFrozenData/meter_daily_data.json')
        requestData = data['meter_daily_entries']['request']
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        requestData['payload'][0]['data'][0]['registerId'] = user_config['Daily']['entries_register_id']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        print(response)
        assert response.get('reply')['replyCode'] == 200
        assert int(response.get('payload')[0].get('data')[0].get('resultValue').get(
            'dataItemValue')) == user_config['Daily']['entries']

    @smokeTest
    def test_get_daily_date(self, caseData):
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
        """
        print("Step 1 : 获取当前电表第一条日结数据")
        data, user_config = caseData('testData/empower/MeterFrozenData/meter_daily_data.json')
        requestData = data['meter_daily_data']['request']
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        requestData['payload'][0]['data'][0]['registerId'] = user_config['Daily']['register_id']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        print(response)
        assert len(response.get('payload')[0].get('data')) == user_config['Daily']['len']
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')

        print(f"Step 2 : 按照时间获取日结数据")
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
        """
        requestData['payload'][0]['data'][0]['parameter']['dataFetchMode'] = 1
        requestData['payload'][0]['data'][0]['parameter']['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter']['endTime'] = startTime

        response = HESRequest().post(url=Project.request_url, params=requestData)
        assert len(response.get('payload')[0].get('data')) == user_config['Daily']['len']
