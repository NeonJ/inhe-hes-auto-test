# -*- coding:utf-8 -*-

import datetime
import json
import os
import time

import requests
from DB import DB
from HESAPI import *
from libs.Singleton import Singleton

# from common import *
from .comm import *


@tag('meter_daily_check')
def meter_daily_check_004():
    """
    使用异步读取的方式去对电表取 - 按照Core的方式对设备进行数据项采集和对比
    """

    start_time = time.time()
    file_path = os.path.abspath("config/DefaultValue/{}/user.yaml".format(Singleton().Project))
    user_config = DB.read_config(file_path)
    database = DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
                  database=user_config['Database']['database'], username=user_config['Database']['username'],
                  passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
                  sid=user_config['Database']['sid'])
    profile_len = user_config['Profile']['daily_len']
    startTime = None

    transactionId = "test-transactionid" + random.randint(0, 1000000).__str__()

    info(f"Step 1 Read the latest entries")
    RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                  messageId=user_config['Request']['messageId'],
                                  createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
                                  serviceType="GET_PROFILE",
                                  source="MDM",
                                  businessType="GET_PROFILE",
                                  replyAddress=None,
                                  asyncReplyFlag="false",
                                  deviceNo=user_config['Request']['deviceNo'],
                                  deviceType=1,
                                  retryCount=2,
                                  startTime=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
                                      "%y%m%d%H%M%S"),
                                  endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                                      "%y%m%d%H%M%S"),
                                  transactionId=transactionId,
                                  parameter={"dataFetchMode": 2, "readTarget": 0, "startTime": "", "endTime": "",
                                             "fromEntry": "1", "toEntry": "1", "fromSelectedValue": 1,
                                             "toSelectedValue": 0},
                                  registerId=user_config['Profile']['daily_obis'], jobUniqueFlag="false",
                                  accessSelector=1).request_json()
    response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(RequestQueue, indent=4), timeout=66)
    if response.status_code == 504:
        print('504 Error and try again')
        time.sleep(5)
        response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(RequestQueue, indent=4), timeout=66)
    if response.get('reply')['replyCode'] != 200:
        # print(response.get('reply')['replyDesc'])
        error(f"** Read Failed **")
        return -1
    else:
        # print(response.get('reply')['replyDesc'])
        info(f"** Read Successfully **")
        if check_len(response.get('payload')[0].get('data'), profile_len):
            info(f"** Profile length matches with config successfully {profile_len} **")
            startTime = response.get('payload')[0].get('data')[0].get('dataTime')
        elif len(response.get('payload')[0].get('data')) == 0:
            info("No Profile Data!")
        else:
            error(f"Profile length matches with config failed {profile_len} **")
            return -1

    info(f"Step 2 Create Core Task and Check Results")
    RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                  messageId=user_config['Request']['messageId'],
                                  createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
                                  serviceType="GET_PROFILE",
                                  source="MDM",
                                  businessType="GET_PROFILE",
                                  replyAddress=None,
                                  asyncReplyFlag="false",
                                  deviceNo=user_config['Request']['deviceNo'],
                                  jobType="ProfileRD",
                                  deviceType=1,
                                  retryCount=2,
                                  startTime=startTime,
                                  endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                                      "%y%m%d%H%M%S"),
                                  transactionId=transactionId,
                                  parameter={"dataFetchMode": 2, "readTarget": 0, "startTime": "", "endTime": "",
                                             "fromEntry": "1", "toEntry": "1", "fromSelectedValue": 1,
                                             "toSelectedValue": 0},
                                  registerId=user_config['Profile']['daily_obis'], jobUniqueFlag="false",
                                  accessSelector=1).createTask()
    response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).taskAddress(),
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(RequestQueue, indent=4), timeout=66)
    if response.status_code == 504:
        print('504 Error and try again')
        time.sleep(5)
        response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(RequestQueue, indent=4), timeout=66)
    if response.get('code') != '200':
        # print(response.get('reply')['replyDesc'])
        error(f"** Create Task Failed **")
        return -1
    else:
        # print(response.get('reply')['replyDesc'])
        info(f"** Create Task Successfully **")
        sql = "select task_state from h_task_run_his where INSTANCE_ID='{}'".format(transactionId)
        db_queue = database.orcl_fetchall_dict(sql)

        while len(db_queue) == 0:
            time.sleep(8)
            db_queue = database.orcl_fetchall_dict(sql)
            info('Waiting for Read Tasks to finish...')
        end_time = time.time()
        info(f"Total cost {end_time - start_time} seconds")

        if db_queue[0]['task_state'] == 3:
            return 0
        else:
            error("Read Task Failed!")
            return -1
