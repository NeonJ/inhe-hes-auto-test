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
    continue_last_check = True

    start_time = time.time()
    file_path = os.path.abspath("config/DefaultValue/{}/user.yaml".format(Singleton().Project))
    user_config = DB.read_config(file_path)
    database = DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
                  database=user_config['Database']['database'], username=user_config['Database']['username'],
                  passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
                  sid=user_config['Database']['sid'])
    if continue_last_check:
        table_name = database.orcl_find_last_result()[0]
    else:
        table_name = database.initial_result(meter_no=user_config['Request']['deviceNo'])

    print('Result Table Name: ', table_name)
    sql = user_config['Register']['sql1'] + ' {} '.format(table_name) + user_config['Register']['sql2'] + "'{}'".format(
        user_config['Request']['deviceNo']) + user_config['Register']['sql3']
    # print(sql)
    db_queue = database.orcl_fetchall_dict(sql)

    i = 1
    for queue in db_queue:
        print('------', i, '/', db_queue.__len__(), '------')
        DeviceBusy = 1
        print(
            "REGISTER_ID:{REGISTER_ID}, OBIS:{PROTOCOL_ID}, Class_ID:{CLASS_ID}, Attribute_id:{ATTRIBUTE_ID}, Is_method:{IS_METHOD}, RW:{RW}, Desc:{REGISTER_DESC}".format(
                **queue))
        if queue.get('RW') == 'r':
            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='GET_COMMON',
                                          businessType='GET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('REGISTER_ID'),
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
                    print('Read Value: ', data.get('resultValue'))
                    database.save_result(table_name, 'get_result', data.get('resultDesc'),
                                         queue.get('REGISTER_ID'))
                    database.save_result(table_name, 'get_value', data.get('resultValue'),
                                         queue.get('REGISTER_ID'))
        elif queue.get('RW') == 'w':
            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='SET_COMMON',
                                          businessType='SET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('REGISTER_ID'),
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
                                         queue.get('REGISTER_ID'))
                    database.save_result(table_name, 'action_value', data.get('resultValue'),
                                         queue.get('REGISTER_ID'))
        elif queue.get('RW') == 'rw':
            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='GET_COMMON',
                                          businessType='GET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('REGISTER_ID'),
                                          transactionId=user_config['Request']['transactionId'],
                                          jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
                                          parameter=user_config['Request']['parameter'],
                                          accessSelector=user_config['Request']['accessSelector']).request_json()
            response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps(RequestQueue, indent=4), timeout=66)
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
                    print('Read Value: ', data.get('resultValue'))
                    parameter = data.get('resultValue')
                    database.save_result(table_name, 'get_result', data.get('resultDesc'),
                                         queue.get('REGISTER_ID'))
                    database.save_result(table_name, 'get_value', data.get('resultValue'),
                                         queue.get('REGISTER_ID'))

            RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                          messageId=user_config['Request']['messageId'],
                                          source=user_config['Request']['source'],
                                          serviceType='SET_COMMON',
                                          businessType='SET_COMMON',
                                          messageType=user_config['Request']['messageType'],
                                          asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
                                          deviceNo=user_config['Request']['deviceNo'],
                                          deviceType=user_config['Request']['deviceType'],
                                          registerId=queue.get('REGISTER_ID'),
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
                                         queue.get('REGISTER_ID'))
                    database.save_result(table_name, 'set_value', data.get('resultValue'),
                                         queue.get('REGISTER_ID'))
        i += 1
    end_time = time.time()
    info(f"Total cost {end_time - start_time} seconds")

    return 0
