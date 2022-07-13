# _*_ coding: utf-8 _*_
# @Time      : 2022/7/13 8:40
# @Author    : Jiannan Cao
# @FileName  : test_version_read.py
import datetime

from kafka import KafkaConsumer

from common.HESRequest import *
from common.marker import *


class Test_Get_Meter_Version:

    @asyncTest
    def test_get_meter_app_version(self, caseData, requestMessage, device, kafkaURL):
        """
        使用接口去读取电表的App Version版本
        """
        data = caseData('testData/Upgrade/meter_version.json')
        requestData = data['app_version']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        sstime = (datetime.datetime.now() - datetime.timedelta(hours=0.5)).strftime('%y%m%d%H%M%S')
        eetime = (datetime.datetime.now() + datetime.timedelta(hours=0.5)).strftime('%y%m%d%H%M%S')
        requestData['payload'][0]['startTime'] = sstime
        requestData['payload'][0]['endTime'] = eetime
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert response.get('reply')['replyCode'] == 200

        #异步kafka任务结果检查
        consumer = KafkaConsumer('hes-read-version-dev', group_id='tester',
                                 bootstrap_servers=kafkaURL)
        count = 1
        fetch_data_list = []
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
        assert 'OK' in fetch_data_list.__str__()

    @asyncTest
    def test_get_meter_legal_version(self, caseData, requestMessage, device, kafkaURL):
        """
        使用接口去读取电表的Legal Version版本
        """
        data = caseData('testData/Upgrade/meter_version.json')
        requestData = data['legal_version']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        sstime = (datetime.datetime.now() - datetime.timedelta(hours=0.5)).strftime('%y%m%d%H%M%S')
        eetime = (datetime.datetime.now() + datetime.timedelta(hours=0.5)).strftime('%y%m%d%H%M%S')
        requestData['payload'][0]['startTime'] = sstime
        requestData['payload'][0]['endTime'] = eetime
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert response.get('reply')['replyCode'] == 200

        #异步kafka任务结果检查
        consumer = KafkaConsumer('hes-read-version-dev', group_id='tester',
                                 bootstrap_servers=kafkaURL)
        count = 1
        fetch_data_list = []
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
        assert 'OK' in fetch_data_list.__str__()

    @asyncTest
    def test_get_meter_module_version(self, caseData, requestMessage, device, kafkaURL):
        """
        使用接口去读取电表的Module Version版本
        """
        data = caseData('testData/Upgrade/meter_version.json')
        requestData = data['module_version']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S', time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        sstime = (datetime.datetime.now() - datetime.timedelta(hours=0.5)).strftime('%y%m%d%H%M%S')
        eetime = (datetime.datetime.now() + datetime.timedelta(hours=0.5)).strftime('%y%m%d%H%M%S')
        requestData['payload'][0]['startTime'] = sstime
        requestData['payload'][0]['endTime'] = eetime
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ', response)
        assert response.get('reply')['replyCode'] == 200

        #异步kafka任务结果检查
        consumer = KafkaConsumer('hes-read-version-dev', group_id='tester',
                                 bootstrap_servers=kafkaURL)
        count = 1
        fetch_data_list = []
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
        assert 'OK' in fetch_data_list.__str__()
