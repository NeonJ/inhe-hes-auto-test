# -*-coding:utf-8-*-
"""
# File       : test_meter_daily.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
from common.HESRequest import *
from common.YamlConfig import nacosConfig
from common.marker import *


class Test_Meter_Daily:

    @pytest.mark.skipif(nacosConfig()['Device']['connect_type'] == 'Long', reason='Short Meter no register')
    @smokeTest1
    def test_get_daily_entries1(self, caseData, requestMessage, device, daily):
        """
        使用同步读取的方式去对电表进行日结entries数据对比
        """
        data = caseData('testData/MeterFrozenData/meter_daily_data.json')
        requestData = data['meter_daily_entries']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = daily['entries_register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert response.get('reply')['replyCode'] == 200
        assert int(response.get('payload')[0].get('data')[0].get('resultValue').get(
            'dataItemValue')) == daily['entries']

    @smokeTest
    def test_get_daily_entries(self, caseData, requestMessage, device, daily):
        """
        使用同步读取的方式去对电表进行日结entries数据对比
        """
        data = caseData('testData/MeterFrozenData/meter_daily_data.json')
        requestData = data['meter_daily_entries']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = daily['entries_register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert response.get('reply')['replyCode'] == 200
        assert int(response.get('payload')[0].get('data')[0].get('resultValue').get(
            'dataItemValue')) == daily['entries']

    @smokeTest
    def test_get_daily_date(self, caseData, requestMessage, device, daily):
        """
        使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
        """
        print("Step 1 : 获取当前电表第一条日结数据")
        data = caseData('testData/MeterFrozenData/meter_daily_data.json')
        requestData = data['meter_daily_data']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = daily['register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert len(response.get('payload')[0].get('data')) == daily['len']
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')

        print(f"Step 2 : 按照时间获取日结数据")
        requestData['payload'][0]['data'][0]['parameter']['dataFetchMode'] = 1
        requestData['payload'][0]['data'][0]['parameter']['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter']['endTime'] = startTime

        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        assert len(response.get('payload')[0].get('data')) == daily['len']
