"""
# File       : conftest.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import time

import pytest

from common.DB import *
from common.HESRequest import *


# 用例执行间隔
@pytest.fixture(scope='function', autouse=True)
def slow_down_tests():
    yield
    time.sleep(1)


@pytest.fixture(scope='function')
def get_daily_date(caseData, device, requestMessage, daily):
    """
    使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
     """
    print("获取当前电表第一条日结数据")
    data = caseData('testData/MeterFrozenData/meter_daily_data.json')['meter_daily_data']
    requestData = data['request']
    requestData['payload'][0]['deviceNo'] = device['device_number']
    requestData['payload'][0]['data'][0]['registerId'] = daily['register_id']
    response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
    if response.get('reply')['replyCode'] != 200:
        print(response.get('payload')[0]['desc'])
        assert False
    else:
        assert len(response.get('payload')[0].get('data')) == daily['len']
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')
    return startTime


@pytest.fixture(scope='function')
def get_monthly_date(caseData, device, requestMessage, monthly):
    print("Step 1 : 获取当前电表第一条月结数据")
    data = caseData('testData/MeterFrozenData/meter_monthly_data.json')['meter_monthly_data']
    requestData = data['request']
    requestData['payload'][0]['deviceNo'] = device['device_number']
    requestData['payload'][0]['data'][0]['registerId'] = monthly['register_id']
    response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
    if response.get('reply')['replyCode'] != 200:
        print(response.get('payload')[0]['desc'])
        assert False
    else:
        assert len(response.get('payload')[0].get('data')) == monthly['len']
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')
    return startTime


@pytest.fixture(scope='function')
def get_lp_date(caseData, device, requestMessage, lp):
    print("Step 1 : 获取当前电表第一条lp数据")
    data = caseData('testData/MeterFrozenData/meter_profile_data.json')['meter_lp_data']
    requestData = data['request']
    requestData['payload'][0]['deviceNo'] = device['device_number']
    requestData['payload'][0]['data'][0]['registerId'] = lp['register_id']
    response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
    if response.get('reply')['replyCode'] != 200:
        print(response.get('payload')[0]['desc'])
        assert False
    else:
        assert len(response.get('payload')[0].get('data')) == lp['len']
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')
    return startTime


@pytest.fixture(scope='function')
def get_daily_event(caseData, device, requestMessage, event):
    print("Step 1 : 获取当前电表第一条daily event数据")
    data = caseData('testData/MeterFrozenData/meter_event_data.json')['meter_daily_event']
    requestData = data['request']
    requestData['payload'][0]['deviceNo'] = device['device_number']
    requestData['payload'][0]['data'][0]['registerId'] = event['register_id']
    response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
    if response.get('reply')['replyCode'] != 200:
        print(response.get('payload')[0]['desc'])
        assert False
    else:
        # assert len(response.get('payload')[0].get('data')) == 2   判断日结事件内容条数
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')
    return startTime


@pytest.fixture(scope='function')
def get_event_standard(caseData, device, requestMessage, event):
    print("Step 1 : 获取当前电表第一条standard event数据")
    data = caseData('testData/MeterFrozenData/meter_event_data.json')['meter_standard_event']
    requestData = data['request']
    requestData['payload'][0]['deviceNo'] = device['device_number']
    requestData['payload'][0]['data'][0]['registerId'] = event['register_id']
    response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
    if response.get('reply')['replyCode'] != 200:
        print(response.get('payload')[0]['desc'])
        assert False
    else:
        # assert len(response.get('payload')[0].get('data')) != 64
        startTime = response.get('payload')[0].get('data')[0].get('dataTime')
    return startTime