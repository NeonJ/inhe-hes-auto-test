# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import time

from kafka import KafkaProducer, KafkaConsumer

from common.DB import *
from common.YamlConfig import nacosConfig
from common.YamlConfig import readConfig
from common.marker import *


@pytest.mark.skipif(nacosConfig()['Device']['connect_type'] == 'Short', reason='Test meter is short connection')
class Test_Auto_Register:

    @asyncTest
    def test_meter_register(self, caseData, device, dbConnect, kafkaURL):
        """
        验证GPRS电表正常自动注册流程
        """
        dbConnect.meter_init(device['device_number'])

        count = 1
        data = caseData('testData/AutoRegistration/register-event-process.json')['gprs_meter']
        requestData = data['pl']
        requestData[0]['dn'] = device['device_number']
        conf = {'bootstrap.servers': kafkaURL}
        # confuluentKafka = confluent_kafka.Producer(**conf)
        # confuluentKafka.produce('register-event-process',key=b'KafkaBatchPush',value=json.dumps(data).encode())
        # confuluentKafka.poll(0)
        producer = KafkaProducer(bootstrap_servers=kafkaURL)
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        time.sleep(5)
        sql1 = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
            device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql1)
        while len(db_queue) == 0 and count < 10:
            time.sleep(6)
            db_queue = dbConnect.fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')
            count = count + 1

        sql2 = "select task_state from h_task_run_his where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
        db_queue = dbConnect.fetchall_dict(sql2)
        while len(db_queue) == 0 and count < 20:
            time.sleep(8)
            db_queue = dbConnect.fetchall_dict(sql2)
            print(db_queue)
            print('Waiting for Reg Tasks to finish...')
            count = count + 1
        assert db_queue[0]['task_state'] == 3

        sql3 = "select DEV_STATUS from c_ar_meter where METER_NO='{}'".format(device['device_number'])
        db_queue = dbConnect.fetchall_dict(sql3)
        print(db_queue)
        assert db_queue[0]['DEV_STATUS'] == 4

    @asyncTest
    def test_meter_register_exception_1(self, caseData, device, databaseConfig, kafkaURL):
        """
        验证GPRS电表未安装不会自动注册
        """
        database = DB(source=databaseConfig['db_source'], host=databaseConfig['db_host'],
                      database=databaseConfig['db_database'], username=databaseConfig['db_user'],
                      passwd=databaseConfig['db_pwd'], port=databaseConfig['db_port'],
                      sid=databaseConfig['db_service'])
        database.meter_init_except_1(device['device_number'])

        count = 1
        data = caseData('testData/AutoRegistration/register-event-process.json'.format(readConfig()['project']))[
            'gprs_meter']
        requestData = data['pl']
        requestData[0]['dn'] = device['device_number']
        producer = KafkaProducer(bootstrap_servers=kafkaURL)
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        sql1 = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
            device['device_number'])
        db_queue = database.fetchall_dict(sql1)
        while len(db_queue) == 0 and count < 2:
            time.sleep(5)
            db_queue = database.fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')
            count = count + 1
        fetch_data_list = []
        consumer = KafkaConsumer('comm-event-process', group_id='tester',
                                 bootstrap_servers=kafkaURL)
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

    @asyncTest
    def test_meter_register_exception_2(self, caseData, device, databaseConfig, kafkaURL):
        """
        验证系统档案中电表档案不是GPRS电表但是通过了FEP请求注册,会将设备档案修改conn_type=1, communication_type=2后进行自动注册
        如果之前是已经注册到DCU下的电表还会生成REG_DEL_ARCHIVES删除集中器内档案任务和修改master_no=null,meter_seq=null
        """
        database = DB(source=databaseConfig['db_source'], host=databaseConfig['db_host'],
                      database=databaseConfig['db_database'], username=databaseConfig['db_user'],
                      passwd=databaseConfig['db_pwd'], port=databaseConfig['db_port'],
                      sid=databaseConfig['db_service'])
        database.meter_init_except_2(device['device_number'])

        count = 1
        data = caseData('testData/AutoRegistration/register-event-process.json'.format(readConfig()['project']))[
            'gprs_meter']
        requestData = data['pl']
        requestData[0]['dn'] = device['device_number']
        producer = KafkaProducer(bootstrap_servers=kafkaURL)
        producer.send('register-event-process', key=b'KafkaBatchPush', value=json.dumps(data).encode())
        producer.close()
        sql1 = "select auto_run_id from H_TASK_RUNNING where NODE_NO='{}' and JOB_TYPE='DeviceRegist'".format(
            device['device_number'])
        db_queue = database.fetchall_dict(sql1)
        while len(db_queue) == 0 and count < 10:
            time.sleep(6)
            db_queue = database.fetchall_dict(sql1)
            print(db_queue)
            print('Waiting for Reg Tasks to Create...')
            count = count + 1

        sql2 = "select task_state from h_task_run_his where auto_run_id='{}'".format(db_queue[0]['auto_run_id'])
        db_queue = database.fetchall_dict(sql2)
        while len(db_queue) == 0 and count < 20:
            time.sleep(8)
            db_queue = database.fetchall_dict(sql2)
            print(db_queue)
            print('Waiting for Reg Tasks to finish...')
            count = count + 1
        assert db_queue[0]['task_state'] == 3

        sql3 = "select DEV_STATUS,CONN_TYPE,COMMUNICATION_TYPE,MASTER_NO,METER_SEQ from c_ar_meter where METER_NO='{}'".format(
            device['device_number'])
        db_queue = database.fetchall_dict(sql3)

        assert db_queue[0]['DEV_STATUS'] == 4
        assert db_queue[0]['CONN_TYPE'] == 1
        assert db_queue[0]['COMMUNICATION_TYPE'] == 2
        assert db_queue[0]['MASTER_NO'] == None
        assert db_queue[0]['METER_SEQ'] == None
