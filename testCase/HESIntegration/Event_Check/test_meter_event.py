"""
# File       : test_meter_event.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

from common.HESRequest import *
from common.marker import *


class Test_Meter_Event:

    @smokeTest
    def test_get_standard_event_entries(self, caseData, requestMessage, device, event):
        """
        使用同步读取的方式去对电表进行日事件entries数据对比
        """
        data = caseData('testData/MeterFrozenData/meter_event_data.json')
        requestData = data['meter_daily_event_entries']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = event['entries_register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert int(
            response.get('payload')[0].get('data')[0].get('resultValue').get('dataItemValue')) != len(
            event['entries_register_id'])

    @smokeTest
    def test_get_standard_event(self, caseData, requestMessage, device, event):
        """
        使用同步读取的方式去对电表进行standard event读取 - 按照Entry+Date方式进行并进行数据项对比
         """
        print("Step 1 : 获取当前电表第一条standard event数据")
        data = caseData('testData/MeterFrozenData/meter_event_data.json')
        requestData = data['meter_standard_event']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        requestData['payload'][0]['data'][0]['registerId'] = event['standard_register_id']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        if response.get('reply')['replyCode'] != 200:
            print(response.get('payload')[0]['desc'])
            assert False
        else:
            # assert len(response.get('payload')[0].get('data')) == 64
            startTime = response.get('payload')[0].get('data')[0].get('dataTime')

        print(f"Step 2 : 按照时间获取冻结事件数据")
        requestData['payload'][0]['data'][0]['parameter']['dataFetchMode'] = 1
        requestData['payload'][0]['data'][0]['parameter']['startTime'] = startTime
        requestData['payload'][0]['data'][0]['parameter']['endTime'] = startTime
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        if response.get('reply')['replyCode'] != 200:
            assert False
        else:
            assert len(response.get('payload')[0].get('data')) == event['len']
