"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import re
import os
import time
import json
import requests
from common import *

import pytest, allure, time, requests
from common.HESAPI import *
from common.marker import *
from common.KFLog import *

@hesTest
class Test_HES_Register_Check:
    """
    根据转化后的Register进行OBIS Check,并将结果输出到数据库结果表
    """

    @pytest.mark.skip
    def test_register_get(self, register_get, get_project_config, get_database, get_result_table):
        DeviceBusy = 1
        print("Register_ID:{}".format(register_get))
        RequestQueue = RequestMessage(correlationId=get_project_config['Request']['correlationId'],
                                      messageId=get_project_config['Request']['messageId'],
                                      source=get_project_config['Request']['source'],
                                      serviceType='GET_COMMON',
                                      businessType='GET_COMMON',
                                      messageType=get_project_config['Request']['messageType'],
                                      asyncReplyFlag=get_project_config['Request']['asyncReplyFlag'],
                                      deviceNo=get_project_config['Request']['deviceNo'],
                                      deviceType=get_project_config['Request']['deviceType'],
                                      registerId=register_get,
                                      transactionId=get_project_config['Request']['transactionId'],
                                      jobUniqueFlag=get_project_config['Request']['jobUniqueFlag'],
                                      parameter=get_project_config['Request']['parameter'],
                                      jobType=None,
                                      accessSelector=get_project_config['Request']['accessSelector']).request_json()
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps(RequestQueue, indent=4), timeout=40)
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
    def test_register_set(self, register_set, get_project_config, get_database, get_result_table):
        DeviceBusy = 1
        print("Register_ID:{}".format(register_set))
        RequestQueue = RequestMessage(correlationId=get_project_config['Request']['correlationId'],
                                      messageId=get_project_config['Request']['messageId'],
                                      source=get_project_config['Request']['source'],
                                      serviceType='GET_COMMON',
                                      businessType='GET_COMMON',
                                      messageType=get_project_config['Request']['messageType'],
                                      asyncReplyFlag=get_project_config['Request']['asyncReplyFlag'],
                                      deviceNo=get_project_config['Request']['deviceNo'],
                                      deviceType=get_project_config['Request']['deviceType'],
                                      registerId=register_set,
                                      transactionId=get_project_config['Request']['transactionId'],
                                      jobUniqueFlag=get_project_config['Request']['jobUniqueFlag'],
                                      parameter=get_project_config['Request']['parameter'],
                                      jobType=None,
                                      accessSelector=get_project_config['Request']['accessSelector']).request_json()
        # response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
        #                          headers={"Content-Type": "application/json"},
        #                          data=json.dumps(RequestQueue, indent=4), timeout=40)
        # for payload in json.loads(response.text).get('payload'):
        #     for data in payload.get('data'):
        #         print('Read Result: ', data.get('resultDesc'))
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps(RequestQueue), timeout=40)
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

        RequestQueue = RequestMessage(correlationId=get_project_config['Request']['correlationId'],
                                      messageId=get_project_config['Request']['messageId'],
                                      source=get_project_config['Request']['source'],
                                      serviceType='SET_COMMON',
                                      businessType='SET_COMMON',
                                      messageType=get_project_config['Request']['messageType'],
                                      asyncReplyFlag=get_project_config['Request']['asyncReplyFlag'],
                                      deviceNo=get_project_config['Request']['deviceNo'],
                                      deviceType=get_project_config['Request']['deviceType'],
                                      registerId=register_set,
                                      transactionId=get_project_config['Request']['transactionId'],
                                      jobUniqueFlag=get_project_config['Request']['jobUniqueFlag'],
                                      parameter=parameter,
                                      jobType=None,
                                      accessSelector=get_project_config['Request']['accessSelector']).request_json()
        DeviceBusy = 1
        while DeviceBusy == 1:
            response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps(RequestQueue), timeout=40)
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
