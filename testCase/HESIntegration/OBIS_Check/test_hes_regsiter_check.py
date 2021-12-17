"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import pytest, allure, time, requests
from common.HESAPI import *
from common.marker import *
from config.settings import *


class Test_HES_Register_Check:
    """
    根据转化后的Register进行OBIS Check,并将结果输出到数据库结果表
    """

    # @pytest.mark.skip
    @hesTest
    def test_register_get(self, register_get, get_database, get_result_table, caseData):
        DeviceBusy = 1
        print("Register_ID:{}".format(register_get))
        data = caseData('testData/HESAPI/OBISCheck/register_get.json')['register_get']
        requestData = data['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_get
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504:
                print('504 Error and try again')
                time.sleep(3)
                continue
            for payload in json.loads(response.text).get('payload'):
                for data in payload.get('data'):
                    print('Read Result: ', data.get('resultDesc'))
                    if data.get('resultDesc') == 'Device Busying !':
                        DeviceBusy = 1
                        print('Device Busy and try again')
                    else:
                        DeviceBusy = 0

        for payload in json.loads(response.text).get('payload'):
            for data in payload.get('data'):
                print('Get Value: ', data.get('resultValue'))
                get_database.save_result(get_result_table, 'get_result', data.get('resultDesc'), register_get)
                get_database.save_result(get_result_table, 'get_value', data.get('resultValue'), register_get)
                assert data.get('resultDesc') == 'OK'

    # @pytest.mark.skip
    @hesTest
    def test_register_set(self, register_set, get_database, get_result_table, caseData):
        DeviceBusy = 1
        print("Register_ID:{}".format(register_set))
        data = caseData('testData/HESAPI/OBISCheck/register_get.json')['register_get']
        requestData = data['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_set
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504:
                print('504 Error and try again')
                time.sleep(3)
                continue
            for payload in json.loads(response.text).get('payload'):
                for data in payload.get('data'):
                    print('Read Result: ', data.get('resultDesc'))
                    if data.get('resultDesc') == 'Device Busying !':
                        DeviceBusy = 1
                        print('Device Busy and try again')
                    else:
                        DeviceBusy = 0

        for payload in json.loads(response.text).get('payload'):
            for data in payload.get('data'):
                print('Get Value: ', data.get('resultValue'))
                parameter = data.get('resultValue')
                get_database.save_result(get_result_table, 'get_result', data.get('resultDesc'),
                                         register_set)
                get_database.save_result(get_result_table, 'get_value', data.get('resultValue'),
                                         register_set)

        data = caseData('testData/HESAPI/OBISCheck/register_set.json')['register_set']
        requestData = data['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_set
        requestData['payload'][0]['data'][0]['parameter'] = parameter
        requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
        DeviceBusy = 1
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     json=requestData, timeout=40)
            time.sleep(1)
            if response.status_code == 504:
                print('504 Error and try again')
                time.sleep(3)
                continue
            for payload in json.loads(response.text).get('payload'):
                for data in payload.get('data'):
                    print('Set Result: ', data.get('resultDesc'))
                    if data.get('resultDesc') == 'Device Busying !':
                        DeviceBusy = 1
                        print('Device Busy and try again')
                    else:
                        DeviceBusy = 0
        for payload in json.loads(response.text).get('payload'):
            for data in payload.get('data'):
                print('Set Value: ', data.get('resultValue'))
                get_database.save_result(get_result_table, 'set_result', data.get('resultDesc'),
                                         register_set)
                get_database.save_result(get_result_table, 'set_value', data.get('resultValue'),
                                         register_set)
                assert data.get('resultDesc') == 'OK'

    @pytest.mark.skip
    def test_register_action(self, register_action, get_project_config, get_database, get_result_table):
        pass