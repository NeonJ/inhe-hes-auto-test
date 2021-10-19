# -*- coding:utf-8 -*-

import re
import os
import time
import datetime
import json
import requests
import socket
from binascii import hexlify, unhexlify
# from comms import *
import yaml
from convertdate import persian
from .comm import *

from HESAPI import *
from DB import DB
from libs.Singleton import Singleton


@tag('meter_daily_check1')
def meter_daily_check_001():
    """
    使用同步读取的方式去对电表进行采集日结并校验
    """

    start_time = time.time()
    file_path = os.path.abspath("conf/DefaultValue/{}/user.yaml".format(Singleton().Project))
    user_config = DB.read_config(file_path)
    database = DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
                  database=user_config['Database']['database'], username=user_config['Database']['username'],
                  passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
                  sid=user_config['Database']['sid'])
    # if continue_last_check:
    #     table_name = database.orcl_find_last_result()[0]
    # else:
    #     table_name = database.initial_result(meter_no=user_config['Request']['deviceNo'])
    #
    # print('Result Table Name: ', table_name)
    # sql = user_config['Register']['sql1'] + ' {} '.format(table_name) + user_config['Register']['sql2'] + "'{}'".format(
    #     user_config['Request']['deviceNo']) + user_config['Register']['sql3']
    # db_queue = database.orcl_fetchall_dict(sql)
    transactionId = "test-transactionid" + random.randint(0, 1000000).__str__()
    RequestQueue = RequestMessage(correlationId=user_config['CreateTask']['correlationId'],
                                  messageId=user_config['CreateTask']['messageId'],
                                  createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
                                  serviceType="GET_PROFILE",
                                  source="REG",
                                  businessType="GET_PROFILE",
                                  replyAddress=None,
                                  asyncReplyFlag="false",
                                  deviceNo=user_config['CreateTask']['deviceNo'],
                                  deviceType=1,
                                  retryCount=2,
                                  startTime=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
                                      "%y%m%d%H%M%S"),
                                  endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                                      "%y%m%d%H%M%S"),
                                  transactionId=transactionId,
                                  parameter=user_config['TaskData']['REG_CHECK_COMM'],
                                  registerId=None, jobUniqueFlag=None,
                                  accessSelector=None).create_task_json()
    response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(RequestQueue, indent=4), timeout=40)
    if response.status_code == 504:
        print('504 Error and try again')
        time.sleep(5)
    if json.loads(response.text).get('reply')['replyCode'] != 200:
        print(json.loads(response.text).get('reply')['replyDesc'])
        error(f"** Create Task Failed **")
        return -1

    sql = "select TASK_STATE from h_task_run_his where INSTANCE_ID='{}'".format(transactionId)
    db_queue = database.orcl_fetchall_dict(sql)

    while len(db_queue) == 0:
        time.sleep(8)
        db_queue = database.orcl_fetchall_dict(sql)
        info('Waiting for Reg Tasks to finish...')
    end_time = time.time()
    info(f"Total cost {end_time - start_time} seconds")

    if db_queue[0]['TASK_STATE'] == 3:
        return 0
    else:
        return -1


def meter_daily_check_002():
    """
    使用创建异步任务的方式去对电表进行采集日结并校验
    """
    # 是否继续上一次未完成的用例
    continue_last_check = True

    start_time = time.time()
    file_path = os.path.abspath("conf/DefaultValue/{}/user.yaml".format(Singleton().Project))
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
    end_time = time.time()
    info(f"Total cost {end_time - start_time} seconds")

    return 0
