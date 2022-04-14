# -*- coding:utf-8 -*-

import json
import os
import time

import requests
from DB import DB
from HESAPI import *
from libs.Singleton import Singleton


# from common import *


@tag('hes_register_check')
def hes_register_check_001():
    """
    根据转化后的Register进行OBIS Check,并将结果输出到数据库结果表
    """
    # 是否继续上一次未完成的用例
    continue_last_check = False

    start_time = time.time()
    file_path = os.path.abspath("config/DefaultValue/{}/user.yaml".format(Singleton().Project))
    user_config = DB.read_config(file_path)
    database = DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
                  database=user_config['Database']['database'], username=user_config['Database']['username'],
                  passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
                  sid=user_config['Database']['sid'])
    if continue_last_check:
        table_name = database.find_last_result()[0]
    else:
        table_name = database.initial_result(meter_no=user_config['Request']['deviceNo'])

    print('Result Table Name: ', table_name)
    sql = user_config['Register']['sql1'] + ' {} '.format(table_name) + user_config['Register']['sql2'] + "'{}'".format(
        user_config['Request']['deviceNo']) + user_config['Register']['sql3']
    db_queue = database.fetchall_dict(sql)

    i = 1
    for queue in db_queue:
        print('------', i, '/', db_queue.__len__(), '------')
        DeviceBusy = 1
        print(
            "Register_ID:{register_id}, Class_ID:{class_id}, Attribute_id:{attribute_id}, Is_method:{is_method}, RW:{rw}, Desc:{register_desc}".format(
                **queue))
        if queue.get('rw') == 'r':
            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='GET_COMMON',
                                          businessType='GET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('register_id'),
                                          transactionId=user_config['Request']['transactionId'],
                                          jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
                                          parameter=user_config['Request']['parameter'],
                                          accessSelector=user_config['Request']['accessSelector']).request_json()
            while DeviceBusy == 1:
                response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         data=json.dumps(RequestQueue, indent=4), timeout=66)
                if response.status_code == 504:
                    print('504 Error and try again')
                    time.sleep(5)
                    continue
                for payload in response.get('payload'):
                    for data in payload.get('data'):
                        print('Read Result: ', data.get('resultDesc'))
                        if data.get('resultDesc') == 'Device Busying !':
                            DeviceBusy = 1
                            print('Device Busy and try again')
                        else:
                            DeviceBusy = 0

            for payload in response.get('payload'):
                for data in payload.get('data'):
                    print('Get Value: ', data.get('resultValue'))
                    database.save_result(table_name, 'get_result', data.get('resultDesc'),
                                         queue.get('register_id'))
                    database.save_result(table_name, 'get_value', data.get('resultValue'),
                                         queue.get('register_id'))
        elif queue.get('rw') == 'w':
            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='SET_COMMON',
                                          businessType='SET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('register_id'),
                                          transactionId=user_config['Request']['transactionId'],
                                          jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
                                          parameter=user_config['Request']['parameter'],
                                          accessSelector=user_config['Request']['accessSelector']).request_json()
            while DeviceBusy == 1:
                response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         data=json.dumps(RequestQueue, indent=4), timeout=66)
                if response.status_code == 504:
                    print('504 Error and try again')
                    time.sleep(5)
                    continue
                for payload in response.get('payload'):
                    for data in payload.get('data'):
                        print('Action Result: ', data.get('resultDesc'))
                        if data.get('resultDesc') == 'Device Busying !':
                            DeviceBusy = 1
                            print('Device Busy and try again')
                        else:
                            DeviceBusy = 0
                print(response.json())

            for payload in response.get('payload'):
                for data in payload.get('data'):
                    print('Action Value: ', data.get('resultValue'))
                    database.save_result(table_name, 'action_result', data.get('resultDesc'),
                                         queue.get('register_id'))
                    database.save_result(table_name, 'action_value', data.get('resultValue'),
                                         queue.get('register_id'))
        elif queue.get('rw') == 'rw':
            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='GET_COMMON',
                                          businessType='GET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('register_id'),
                                          transactionId=user_config['Request']['transactionId'],
                                          jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
                                          parameter=user_config['Request']['parameter'],
                                          accessSelector=user_config['Request']['accessSelector']).request_json()
            # response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
            #                          headers={"Content-Type": "application/json"},
            #                          data=json.dumps(RequestQueue, indent=4), timeout=66)
            # for payload in response.get('payload'):
            #     for data in payload.get('data'):
            #         print('Read Result: ', data.get('resultDesc'))
            while DeviceBusy == 1:
                response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         data=json.dumps(RequestQueue), timeout=66)
                if response.status_code == 504:
                    print('504 Error and try again')
                    time.sleep(5)
                    continue
                for payload in response.get('payload'):
                    for data in payload.get('data'):
                        print('Read Result: ', data.get('resultDesc'))
                        if data.get('resultDesc') == 'Device Busying !':
                            DeviceBusy = 1
                            print('Device Busy and try again')
                        else:
                            DeviceBusy = 0

            for payload in response.get('payload'):
                for data in payload.get('data'):
                    print('Get Value: ', data.get('resultValue'))
                    parameter = data.get('resultValue')
                    database.save_result(table_name, 'get_result', data.get('resultDesc'),
                                         queue.get('register_id'))
                    database.save_result(table_name, 'get_value', data.get('resultValue'),
                                         queue.get('register_id'))

            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='SET_COMMON',
                                          businessType='SET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('register_id'),
                                          transactionId=user_config['Request']['transactionId'],
                                          jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
                                          parameter=parameter,
                                          accessSelector=user_config['Request']['accessSelector']).request_json()
            DeviceBusy = 1
            while DeviceBusy == 1:
                response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                         headers={"Content-Type": "application/json"},
                                         data=json.dumps(RequestQueue), timeout=66)
                if response.status_code == 504:
                    print('504 Error and try again')
                    time.sleep(5)
                    continue
                for payload in response.get('payload'):
                    for data in payload.get('data'):
                        print('Set Result: ', data.get('resultDesc'))
                        if data.get('resultDesc') == 'Device Busying !':
                            DeviceBusy = 1
                            print('Device Busy and try again')
                        else:
                            DeviceBusy = 0
            for payload in response.get('payload'):
                for data in payload.get('data'):
                    print('Set Value: ', data.get('resultValue'))
                    database.save_result(table_name, 'set_result', data.get('resultDesc'),
                                         queue.get('register_id'))
                    database.save_result(table_name, 'set_value', data.get('resultValue'),
                                         queue.get('register_id'))
        i += 1
    end_time = time.time()
    info(f"Total cost {end_time - start_time} seconds")

    return 0
