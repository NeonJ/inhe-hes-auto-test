# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check_short.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import time

from kafka import KafkaProducer, KafkaConsumer
from common.marker import *

from common.UtilTools import *
from config.settings import *


class Test_Auto_Register_Short:

    # @hesAsyncTest
    def test_meter_register_short(self, get_database, caseData, meter_init):
        """
        验证GPRS服务端短连接电表正常自动注册流程
        """
        count = 1
        data, user_config = caseData('testData/empower/AutoRegistration/register-event-process.json'.format(Project.name))['short_meter']
        requestData = data['pl']
        requestData[0]['dn'] = user_config['Device']['device_number']
        producer = KafkaProducer(bootstrap_servers=setting[Project.name]['kafka_url'])
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        time.sleep(5)
        sql1 = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
            user_config['Device']['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql1)
        while len(db_queue) == 0 and count < 10:
            time.sleep(6)
            db_queue = get_database.orcl_fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')
            count = count + 1

        sql2 = "select TASK_STATE from h_task_run_his where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql2)
        while len(db_queue) == 0 and count < 20:
            time.sleep(8)
            db_queue = get_database.orcl_fetchall_dict(sql2)
            print(db_queue)
            print('Waiting for Reg Tasks to finish...')
            count = count + 1
        assert db_queue[0]['TASK_STATE'] == 3

        sql3 = "select DEV_STATUS from c_ar_meter where METER_NO='{}'".format(user_config['Device']['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql3)
        print(db_queue)
        assert db_queue[0]['DEV_STATUS'] == 4

    # @hesAsyncTest
    def test_meter_register_short_exception_1(self, get_database, caseData, meter_init_except_1):
        """
        验证GPRS电表未安装不会自动注册
        """
        count = 1
        data, user_config = caseData('testData/empower/AutoRegistration/register-event-process.json'.format(Project.name))['short_meter']
        requestData = data['pl']
        requestData[0]['dn'] = user_config['Device']['device_number']
        producer = KafkaProducer(bootstrap_servers=setting[Project.name]['kafka_url'])
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        sql1 = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
            user_config['Device']['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql1)
        while len(db_queue) == 0 and count < 2:
            time.sleep(5)
            db_queue = get_database.orcl_fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')
            count = count + 1
        fetch_data_list = []
        consumer = KafkaConsumer('comm-event-process', group_id='tester',
                                 bootstrap_servers=setting[Project.name]['kafka_url'])
        while count < 10:
            fetch_data_dict = consumer.poll(timeout_ms=2000, max_records=20)
            for keys, values in fetch_data_dict.items():
                for i in values:
                    print(i.value)
                    print(i.key)
                    print(i.topic)
                    print(i.partition)
            time.sleep(2)
            count = count + 1
            fetch_data_list.append(fetch_data_dict)
        assert 'AR_UNINSTALLED_REG_DEVICE' in fetch_data_list.__str__()

    # @hesAsyncTest
    def test_meter_register_short_exception_2(self, get_database, caseData, meter_init_except_2):
        """
        验证系统档案中电表档案不是GPRS电表但是通过了FEP请求注册,会将设备档案修改conn_type=1, communication_type=2后进行自动注册
        如果之前是已经注册到DCU下的电表还会生成REG_DEL_ARCHIVES删除集中器内档案任务和修改master_no=null,meter_seq=null
        """
        count = 1
        data, user_config = caseData('testData/empower/AutoRegistration/register-event-process.json'.format(Project.name))['short_meter']
        requestData = data['pl']
        requestData[0]['dn'] = user_config['Device']['device_number']
        producer = KafkaProducer(bootstrap_servers=setting[Project.name]['kafka_url'])
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        sql1 = "select AUTO_RUN_ID from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
            user_config['Device']['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql1)
        while len(db_queue) == 0 and count < 10:
            time.sleep(6)
            db_queue = get_database.orcl_fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')
            count = count + 1

        sql2 = "select TASK_STATE from h_task_run_his where AUTO_RUN_ID='{}'".format(db_queue[0]['AUTO_RUN_ID'])
        db_queue = get_database.orcl_fetchall_dict(sql2)
        while len(db_queue) == 0 and count < 20:
            time.sleep(8)
            db_queue = get_database.orcl_fetchall_dict(sql2)
            print(db_queue)
            print('Waiting for Reg Tasks to finish...')
            count = count + 1
        assert db_queue[0]['TASK_STATE'] == 3

        sql3 = "select DEV_STATUS,CONN_TYPE,COMMUNICATION_TYPE,MASTER_NO,METER_SEQ from c_ar_meter where METER_NO='{}'".format(
            user_config['Device']['device_number'])
        db_queue = get_database.orcl_fetchall_dict(sql3)

        assert db_queue[0]['DEV_STATUS'] == 4
        assert db_queue[0]['CONN_TYPE'] == 1
        assert db_queue[0]['COMMUNICATION_TYPE'] == 2
        assert db_queue[0]['MASTER_NO'] == None
        assert db_queue[0]['METER_SEQ'] == None