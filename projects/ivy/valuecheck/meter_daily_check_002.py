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


@tag('meter_daily_check1')
def meter_daily_check_002():
    """
    使用同步读取的方式去对电表进行日结读取 - 按照Entry+Date方式进行并进行数据项对比
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

    info(f"Step 1 Read daily data entries")
    transactionId = "test-transactionid" + random.randint(0, 1000000).__str__()
    RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
                                  messageId=user_config['Request']['messageId'],
                                  createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
                                  serviceType="GET_COMMON",
                                  source="MDM",
                                  businessType="GET_COMMON",
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
                                  parameter={},
                                  registerId=user_config['Profile']['daily_entries_obis'], jobUniqueFlag="false",
                                  accessSelector=1).request_json()
    # print(json.dumps(RequestQueue, indent=4))
    response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(RequestQueue, indent=4), timeout=40)
    # print(response.json())
    if response.status_code == 504:
        print('504 Error and try again')
        time.sleep(5)
        response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(RequestQueue, indent=4), timeout=40)
    if json.loads(response.text).get('reply')['replyCode'] != 200:
        # print(json.loads(response.text).get('reply')['replyDesc'])
        error(f"** Read Failed **")
        return -1
    else:
        # print(json.loads(response.text).get('reply')['replyDesc'])
        info(f"** Read Successfully **")
        if int(json.loads(response.text).get('payload')[0].get('data')[0].get('resultValue').get('dataItemValue')) == \
                user_config['Profile']['daily_entries']:
            info("** Match with Config!")
        else:
            error("** Mismatch with Config!")

    info(f"Step 2 Read the latest entries")
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
                             data=json.dumps(RequestQueue, indent=4), timeout=40)
    if response.status_code == 504:
        print('504 Error and try again')
        time.sleep(5)
        response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(RequestQueue, indent=4), timeout=40)
    if json.loads(response.text).get('reply')['replyCode'] != 200:
        # print(json.loads(response.text).get('reply')['replyDesc'])
        error(f"** Read Failed **")
        return -1
    else:
        # print(json.loads(response.text).get('reply')['replyDesc'])
        info(f"** Read Successfully **")
        if check_len(json.loads(response.text).get('payload')[0].get('data'), profile_len):
            info(f"** Profile length matches with config successfully {profile_len} **")
            startTime = json.loads(response.text).get('payload')[0].get('data')[0].get('dataTime')
        elif len(json.loads(response.text).get('payload')[0].get('data')) == 0:
            info("No Profile Data!")
        else:
            error(f"Profile length matches with config failed {profile_len} **")
            return -1

    info(f"Step 3 Read the data by date")
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
                                  parameter={"dataFetchMode": 1, "readTarget": 0, "startTime": startTime,
                                             "endTime": startTime,
                                             "fromEntry": "1", "toEntry": "2", "fromSelectedValue": 1,
                                             "toSelectedValue": 0},
                                  registerId=user_config['Profile']['daily_obis'], jobUniqueFlag="false",
                                  accessSelector=1).request_json()
    response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(RequestQueue, indent=4), timeout=40)
    if response.status_code == 504:
        print('504 Error and try again')
        time.sleep(5)
        response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(RequestQueue, indent=4), timeout=40)
    if json.loads(response.text).get('reply')['replyCode'] != 200:
        # print(json.loads(response.text).get('reply')['replyDesc'])
        error(f"** Read Failed **")
        return -1
    else:
        # print(json.loads(response.text).get('reply')['replyDesc'])
        info(f"** Read Successfully **")
        if check_len(json.loads(response.text).get('payload')[0].get('data'), profile_len):
            info(f"** Profile length matches with config successfully {profile_len} **")
            return 0
        elif len(json.loads(response.text).get('payload')[0].get('data')) == 0:
            info("No Profile Data!")
        else:
            error(f"Profile length matches with config failed {profile_len} **")
            return -1
