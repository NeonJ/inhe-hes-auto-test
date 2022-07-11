# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import nacos
import yaml

from common.DB import *
from common.HESRequest import *
from common.YamlConfig import readConfig
from common.marker import *


class Test_HES_Register_Check:
    """
    根据转化后的Register进行OBIS Check,并将结果输出到数据库结果表
    """

    def get_db_register(action):
        register_list = []
        client = nacos.NacosClient(server_addresses=readConfig()['nacos_url'], namespace='HES', username="nacos",
                                   password="nacos")
        data_id = readConfig()['project']
        group = readConfig()['group']
        config = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
        database = DB(source=config['DATABASE']['db_source'], host=config['DATABASE']['db_host'],
                      database=config['DATABASE']['db_database'], username=config['DATABASE']['db_user'],
                      passwd=config['DATABASE']['db_pwd'], port=config['DATABASE']['db_port'],
                      sid=config['DATABASE']['db_service'])
        print(config['Device']['device_number'])
        if readConfig()['resume'] == 'True':
            table_name = database.last_result(config['Device']['device_number'])[0]
        else:
            try:
                table_name = database.initial_result(meter_no=config['Device']['device_number'])
                table_name = database.last_result(config['Device']['device_number'])[0]
            except:
                table_name = database.last_result(config['Device']['device_number'])[0]
                print("The OBIS inspection result table already exists on the day: ", table_name)
        print('Result Table Name: ', table_name)
        obis_sql1 = "select register_id, class_id, index_id, register_type,data_type_int, rw from "
        obis_sql2 = " where  PTL_TYPE = (select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no = '{}'))".format(
            config['Device']['device_number'])
        sql = obis_sql1 + '{}'.format(table_name) + obis_sql2.format()
        db_queue = database.fetchall_dict(sql)
        for queue in db_queue:
            if queue.get('RW') == action:
                register_list.append(queue.get('REGISTER_ID'))
        return register_list

    # @obisTest
    @pytest.mark.parametrize('register_get', get_db_register('r'), indirect=False)
    def test_register_get(self, register_get, dbConnect, caseData, device, requestMessage):
        """Get Register Check"""
        print("Register_ID:{}".format(register_get))
        data = caseData('testData/OBISCheck/register_get.json'.format(readConfig()['project']))[
            'register_get']
        requestData = data['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_get
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        table_name = dbConnect.last_result(device['device_number'])[0]
        print('Result Table Name: ', table_name)
        for payload in response.get('payload'):
            if payload.get('data') == []:
                print("RegisterID ERROR", response.get('payload'))
                assert False
            else:
                continue
        for payload in response.get('payload'):
            for data in payload.get('data'):
                print('Get Value: ', data.get('resultValue'))
                # dbConnect.save_result(table_name, 'get_result', data.get('resultDesc'),
                #                       register_get)
                # dbConnect.save_result(table_name, 'get_value', data.get('resultValue'),
                #                       register_get)
                dbConnect.save_result(table_name, 'get_result', data.get('resultDesc'), 'get_value',
                                      data.get('resultValue'), elapsed, register_get)
                assert data.get('resultDesc') == 'OK'

    # @obisTest
    @pytest.mark.parametrize('register_set', get_db_register('rw'))
    def test_register_set(self, register_set, dbConnect, caseData, device, requestMessage):
        """Set Register Check"""
        print("Register_ID:{}".format(register_set))
        data = caseData('testData/OBISCheck/register_get.json')
        requestData = data['register_get']['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_set
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        table_name = dbConnect.last_result(device['device_number'])[0]
        print('Result Table Name: ', table_name)
        for payload in response.get('payload'):
            if payload.get('data') == []:
                print("RegisterID ERROR", response.get('payload'))
                assert False
            else:
                continue
        for payload in response.get('payload'):
            for data in payload.get('data'):
                print('Get Value: ', data.get('resultValue'))
                parameter = data.get('resultValue')
                # dbConnect.save_result(table_name, 'get_result', data.get('resultDesc'),
                #                       register_set)
                # dbConnect.save_result(table_name, 'get_value', data.get('resultValue'),
                #                       register_set)
                dbConnect.save_result(table_name, 'get_result', data.get('resultDesc'), 'get_value',
                                      data.get('resultValue'), elapsed, register_set)

        data = caseData('testData/OBISCheck/register_set.json')
        requestData = data['register_set']['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_set
        requestData['payload'][0]['data'][0]['parameter'] = parameter
        requestData['payload'][0]['deviceNo'] = device['device_number']
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        for payload in response.get('payload'):
            for data in payload.get('data'):
                print('Set Value: ', data.get('resultValue'))
                # dbConnect.save_result(table_name, 'set_result', data.get('resultDesc'),
                #                       register_set)
                # dbConnect.save_result(table_name, 'set_value', data.get('resultValue'),
                #                       register_set)
                dbConnect.save_result(table_name, 'set_result', data.get('resultDesc'), 'set_value',
                                      data.get('resultValue'), elapsed, register_set)
                assert data.get('resultDesc') == 'OK'

    def test_register_action(self, register_action, get_project_config, get_database, get_result_table):
        pass
