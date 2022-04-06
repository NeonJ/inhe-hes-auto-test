# -*-coding:utf-8-*-
"""
# File       : test_meter_daily.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

from common.marker import *
from config.settings import *



class Test_Meter_Daily:

    @hesSyncTest
    def test_get_daily_entries(self, caseData):
        """
        使用同步读取的方式去对电表进行日结entries数据对比
        """
        data = caseData('testData/{}/MeterFrozenData/meter_daily_data.json'.format(Project.name))['meter_daily_entries']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        assert response.get('reply')['replyCode'] == 200
        assert int(response.get('payload')[0].get('data')[0].get('resultValue').get(
            'dataItemValue')) == setting[Project.name]['daily_entries']

    @hesSyncTest
    def test_get_daily_date(self, caseData):
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
        """
        print("Step 1 : 获取当前电表第一条日结数据")
        startTime = None
        data = caseData('testData/{}/MeterFrozenData/meter_daily_data.json'.format(Project.name))['meter_daily_data']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        print(response)
        assert len(response.get('payload')[0].get('data')) == setting[Project.name][
            'daily_len']
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')

        print(f"Step 2 : 按照时间获取日结数据")
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
        """
        data = caseData('testData/{}/MeterFrozenData/meter_daily_data.json'.format(Project.name))['meter_daily_data']
        requestData = data['request']
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        requestData['payload'][0]['data'][0]['parameter']['dataFetchMode'] = 1
        requestData['payload'][0]['data'][0]['parameter']['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter']['endTime'] = startTime

        response = HESRequest.post(url=Project.request_url, params=requestData)
        assert len(response.get('payload')[0].get('data')) == setting[Project.name]['daily_len']
