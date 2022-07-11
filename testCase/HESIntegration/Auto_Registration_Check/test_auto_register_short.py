# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check_short.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import time

import allure

from common.HESRequest import HESRequest
from common.marker import *
from common.YamlConfig import nacosConfig


@pytest.mark.skipif(nacosConfig()['Device']['connect_type'] == 'Long', reason='Test meter is long connection')
class Test_Auto_Register_Short:

    @asyncTest
    def test_meter_register_short(self, caseData, device, dbConnect, requestMessage):
        """
        验证GPRS电表正常自动注册流程，前提是短链接电表以及设置了push的前置机地址
        """

        count = 1
        with allure.step('查找项目中的push connectivity register_id'):
            sql = f"select REGISTER_ID from H_CONFIG_REGISTER where OBIS = '0.0.25.9.0.255' and REGISTER_TYPE = 1 and PTL_TYPE = (select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where METER_NO = '{device['device_number']}'))"
            push_register = dbConnect.fetchall_dict(sql)[0]
            print(push_register)

        with allure.step('电表档案初始化'):
            dbConnect.meter_init(device['device_number'])

        with allure.step('执行服务端电表的push connectivity的配置设置'):
            pass

        with allure.step('执行服务端电表push connectivity的命令触发'):
            data = caseData('testData/OBISCheck/register_set.json')
            requestData = data['register_set']['request']
            requestData['payload'][0]['data'][0]['registerId'] = push_register['register_id']
            requestData['payload'][0]['deviceNo'] = device['device_number']
            transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
            requestData['payload'][0]['transactionId'] = transactionId
            re, elapsed = HESRequest().post(url=requestMessage, params=requestData)
            print(re)
            assert re.get('reply')['replyCode'] == 200

        with allure.step('自动注册检查'):
            sql1 = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
                device['device_number'])
            db_queue = dbConnect.fetchall_dict(sql1)
            print(db_queue)
            while len(db_queue) == 0 and count < 20:
                time.sleep(6)
                db_queue = dbConnect.fetchall_dict(sql1)
                print(db_queue)
                print('Waiting for Reg Tasks to Create...')
                count = count + 1

            sql2 = "select task_state from h_task_run_his where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
            db_queue = dbConnect.fetchall_dict(sql2)
            while len(db_queue) == 0 and count < 30:
                time.sleep(8)
                db_queue = dbConnect.fetchall_dict(sql2)
                print(db_queue)
                print('Waiting for Reg Tasks to finish...')
                count = count + 1
            assert db_queue[0]['task_state'] == 3

            sql3 = "select DEV_STATUS,Conn_type from c_ar_meter where METER_NO='{}'".format(device['device_number'])
            db_queue = dbConnect.fetchall_dict(sql3)
            print(db_queue)
            assert db_queue[0]['dev_status'] == 4
            assert db_queue[0]['conn_type'] == 7
