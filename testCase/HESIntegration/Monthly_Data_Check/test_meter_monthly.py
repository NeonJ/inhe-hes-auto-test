# -*-coding:utf-8-*-
"""
# File       : test_meter_profile.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
from common.HESRequest import *
from common.marker import *


class Test_Meter_Monthly:

    @smokeTest
    def test_get_monthly_entries(self, caseData, requestMessage, device, monthly):
        """
        使用同步读取的方式去对电表进行月结entries数据对比
        """
        data = caseData('testData/MeterFrozenData/meter_monthly_data.json')
        requestData = data['meter_monthly_entries']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = monthly['entries_register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        if response.get('reply')['replyCode'] != 200:
            assert False
        else:
            assert int(response.get('payload')[0].get('data')[0].get('resultValue').get(
                'dataItemValue')) == monthly['entries']

    @smokeTest
    def test_get_monthly_date(self, caseData, requestMessage, device, monthly):
        """
        使用同步读取的方式去对电表进行月结读取 - 按照Entry+Date方式进行并进行数据项对比
         """

        print("Step 1 : 获取当前电表第一条月结数据")
        data = caseData('testData/MeterFrozenData/meter_monthly_data.json')
        requestData = data['meter_monthly_data']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = monthly['register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        if response.get('reply')['replyCode'] != 200:
            assert False
        else:
            assert len(response.get('payload')[0].get('data')) == monthly['len']
            startTime = response.get('payload')[0].get('data')[0].get('dataTime')

        print("Step 2 : 按照时间获取月结数据")
        requestData['payload'][0]['data'][0]['parameter']['dataFetchMode'] = 1
        requestData['payload'][0]['data'][0]['parameter']['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter']['endTime'] = startTime
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        if response.get('reply')['replyCode'] != 200:
            assert False
        else:
            assert len(response.get('payload')[0].get('data')) == monthly['len']
