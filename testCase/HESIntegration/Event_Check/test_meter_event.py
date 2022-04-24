"""
# File       : test_meter_event.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

from common.HESRequest import *
from common.marker import *
from config.settings import *


class Test_Meter_Event:

    @smokeTest
    def test_get_daily_event_entries(self, caseData):
        """
        使用同步读取的方式去对电表进行日事件entries数据对比
        """
        data, user_config = caseData('testData/empower/MeterFrozenData/meter_event_data.json')
        requestData = data['meter_daily_event_entries']['request']
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        requestData['payload'][0]['data'][0]['registerId'] = user_config['DailyEvent']['entries_register_id']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        print(response)
        assert int(
            response.get('payload')[0].get('data')[0].get('resultValue').get('dataItemValue')) != len(user_config['DailyEvent'][
                   'entries_register_id'])

    @smokeTest
    def test_get_daily_event(self, caseData):
        """
        使用同步读取的方式去对电表进行daily event读取 - 按照Entry+Date方式进行并进行数据项对比
         """
        print("Step 1 : 获取当前电表第一条daily event数据")
        data, user_config = caseData('testData/empower/MeterFrozenData/meter_event_data.json')
        requestData = data['meter_daily_event']['request']
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        requestData['payload'][0]['data'][0]['registerId'] = user_config['DailyEvent']['daily_event_register_id']
        response = HESRequest().post(url=Project.request_url, params=requestData)
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
        response = HESRequest().post(url=Project.request_url, params=requestData)
        if response.get('reply')['replyCode'] != 200:
            assert False
        else:
            assert len(response.get('payload')[0].get('data')) == 0