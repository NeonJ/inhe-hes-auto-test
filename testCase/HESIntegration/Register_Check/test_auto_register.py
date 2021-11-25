"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import pytest, allure, time, datetime, requests,random
from common.HESAPI import *
from common.marker import *
from common.KFLog import *

@hesTest
class Test_Auto_Register:
    """
    验证GPRS电表是否支持系统的自动注册功能
    """

    def tess_meter_register(self, get_project_config, get_database):
        transactionId = "test-transactionid" + random.randint(0, 1000000).__str__()
        RequestQueue = RequestMessage(correlationId=get_project_config['CreateTask']['correlationId'],
                                      messageId=get_project_config['CreateTask']['messageId'],
                                      createTime=datetime.datetime.now().strftime("%y%m%d%H%M%S"),
                                      serviceType="CMD_COMMON",
                                      source="REG",
                                      businessType="REG_CHECK_COMM",
                                      replyAddress="TEST_COMMUNICATION_RESULT_FROM_HES",
                                      asyncReplyFlag="true",
                                      deviceNo=get_project_config['CreateTask']['deviceNo'],
                                      deviceType=1,
                                      retryCount=2,
                                      startTime=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(
                                          "%y%m%d%H%M%S"),
                                      endTime=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                                          "%y%m%d%H%M%S"),
                                      transactionId=get_project_config['CreateTask']['transactionId'],
                                      data=get_project_config['TaskData']['REG_CHECK_COMM'],
                                      registerId=None, parameter=None, jobUniqueFlag=None,
                                      accessSelector=None).create_task_json()
        response = requests.post(url=HESAPI(Address=get_project_config['HESAPI']['url']).requestAddress(),
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(RequestQueue, indent=4), timeout=40)
        if response.status_code == 504:
            print('504 Error and try again')
            time.sleep(4)
        if json.loads(response.text).get('reply')['replyCode'] != 200:
            print(json.loads(response.text).get('reply')['replyDesc'])
            error(f"** Create Task Failed **")

        sql = "select TASK_STATE from h_task_run_his where INSTANCE_ID='{}'".format(transactionId)
        db_queue = get_database.orcl_fetchall_dict(sql)

        while len(db_queue) == 0:
            time.sleep(8)
            db_queue = get_database.orcl_fetchall_dict(sql)
            print('Waiting for Reg Tasks to finish...')

        assert db_queue[0]['TASK_STATE'] == 3