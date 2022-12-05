# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import json
import time

import nacos
import redis as redis
import yaml
import re

from common.DB import *
from common.HESRequest import *
from common.YamlConfig import *
from common.marker import *


class Test_HES_Register_Check:
    """
    根据转化后的Register进行OBIS Check,并将结果输出到数据库结果表, 0 Get，2-Set, 1-Action
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
        items_sql1 = "select ITEM_ID,OBIS,CLASS_ID,INDEX_ID,INDEX_TYPE from "
        items_sql2 = " where PTL_CODE = (select PTL_CODE from (select substr(MODEL_CODE_PTL, 0, instr(MODEL_CODE_PTL, '_', 1) - 1) as model_code, PTL_CODE from HES_PARSE_DLMS_PTL) ptl where ptl.model_code = (select METER_MODEL from AM_DEVICE d where d.DEVICE_ADDRESS = '{}'))".format(
            config['Device']['device_number'])
        sql = items_sql1 + '{}'.format(table_name) + items_sql2.format()
        print(sql)
        db_queue = database.fetchall_dict(sql)
        # print(db_queue)
        # for queue in db_queue:
        #     print(type(queue.get('INDEX_TYPE')))
        for queue in db_queue:
            if queue.get('INDEX_TYPE') == action:
                register_list.append(queue.get('ITEM_ID'))
        return register_list

    @obisTest
    @pytest.mark.parametrize('register_get', get_db_register(0), indirect=False)
    def test_register_get(self, register_get, dbConnect, caseData, device, realExec, realGet):
        """Get Register Check"""
        print("Register_ID:{}".format(register_get))

        data = f"dev={device['device_number']}&field={register_get}&invalid_time=2022-11-19%2000%3A00%3A00&operator=neon&module_type=1&save_flag=1"
        response = requests.get(url=realExec, params=data)
        table_name = dbConnect.last_result(device['device_number'])[0]
        print('Result Table Name: ', table_name)
        assert json.loads(response.text).get('message') == 'SUCCESS'
        cmdID = json.loads(response.text).get('result')
        print(cmdID)
        data = 'cmd=' + cmdID
        for i in range(15):
            if i == 14:
                print('the command was executed over 30s')
                dbConnect.save_result(table_name, 'get_result', 'time out', 'get_value',
                                      '30s', 0, register_get)
                assert False
            get_result = requests.get(url=realGet, params=data)
            if json.loads(get_result.text).get('message') == 'SUCCESS':
                if json.loads(get_result.text).get('result').get('result') == 'S':
                    result_data = json.loads(get_result.text).get('result').get('data')
                    print('Command executed successfully: ', result_data)
                    re_result = re.findall('(?<==).*$', result_data)
                    print(re_result)
                    dbConnect.save_result(table_name, 'get_result', 'Success', 'get_value',
                                          re_result, 0, register_get)
                    assert len(re_result) != 0
                    break
                elif json.loads(get_result.text).get('result').get('result') == 'W':
                    time.sleep(2)
                    i = + 1
                    continue
                elif json.loads(get_result.text).get('result').get('result') == 'F':
                    if '-' in json.loads(get_result.text).get('result').get('data'):
                        pool = redis.ConnectionPool(host='1.14.167.253', port=6379, db=0, password='test123')
                        r = redis.Redis(connection_pool=pool)
                        keys = 'h:ApiResponse:' + cmdID
                        p = eval(json.dumps(r.get(keys).decode('utf-8')))
                        if json.loads(p).get('RetType') == -99999:
                            print('Running...')
                            time.sleep(2)
                            i = + 1
                            continue
                        elif json.loads(p).get('RetType') == 0:
                            print('Running...')
                            continue
                        else:
                            print('[Error Type]', json.loads(p).get('RetType'))
                            print('[Error Data]', json.loads(p).get('RetData'))
                            dbConnect.save_result(table_name, 'get_result', json.loads(p).get('RetType'), 'get_value',
                                                  json.loads(p).get('RetData'), 0, register_get)
                            assert False
                else:
                    time.sleep(2)
                    i = + 1

            else:
                assert json.loads(get_result.text).get('message') == 'SUCCESS'


    @obisTest
    @pytest.mark.parametrize('register_set', get_db_register(2), indirect=False)
    def test_register_set(self, register_set, dbConnect, caseData, device, realExec, realGet):
        """Setp 1 Get Value"""
        print("Register_ID:{}".format(register_set))
        register = register_set.replace('W','')
        data = f"dev={device['device_number']}&field={register}&invalid_time=2022-11-19%2000%3A00%3A00&operator=neon&module_type=1&save_flag=1"
        response = requests.get(url=realExec, params=data)
        table_name = dbConnect.last_result(device['device_number'])[0]
        print('Result Table Name: ', table_name)
        assert json.loads(response.text).get('message') == 'SUCCESS'
        cmdID = json.loads(response.text).get('result')
        print(cmdID)
        data = 'cmd=' + cmdID
        for i in range(15):
            if i == 14:
                print('the command was executed over 30s')
                dbConnect.save_result(table_name, 'get_result', 'time out', 'get_value',
                                      '30s', 0, register_set)
                assert False
            get_result = requests.get(url=realGet, params=data)
            if json.loads(get_result.text).get('message') == 'SUCCESS':
                if json.loads(get_result.text).get('result').get('result') == 'S':
                    result_data = json.loads(get_result.text).get('result').get('data')
                    print('Command executed successfully: ', result_data)
                    re_result = re.findall('(?<==).*$', result_data)
                    print(re_result)
                    dbConnect.save_result(table_name, 'get_result', 'Success', 'get_value',
                                          re_result, 0, register_set)
                    assert len(re_result) != 0
                    break
                elif json.loads(get_result.text).get('result').get('result') == 'W':
                    time.sleep(2)
                    i = + 1
                    continue
                elif json.loads(get_result.text).get('result').get('result') == 'F':
                    if '-' in json.loads(get_result.text).get('result').get('data'):
                        pool = redis.ConnectionPool(host='1.14.167.253', port=6379, db=0, password='test123')
                        r = redis.Redis(connection_pool=pool)
                        keys = 'h:ApiResponse:' + cmdID
                        p = eval(json.dumps(r.get(keys).decode('utf-8')))
                        if json.loads(p).get('RetType') == -99999:
                            print('Running...')
                            time.sleep(2)
                            i = + 1
                            continue
                        elif json.loads(p).get('RetType') == 0:
                            print('Running...')
                            continue
                        else:
                            print('[Error Type]', json.loads(p).get('RetType'))
                            print('[Error Data]', json.loads(p).get('RetData'))
                            dbConnect.save_result(table_name, 'get_result', json.loads(p).get('RetType'), 'get_value',
                                                  json.loads(p).get('RetData'), 0, register_set)
                            assert False
                else:
                    time.sleep(2)
                    i = + 1

            else:
                assert json.loads(get_result.text).get('message') == 'SUCCESS'
            print(i)
            if i == 14:
                print('the command was executed over 30s')
                dbConnect.save_result(table_name, 'get_result', 'time out', 'get_value',
                                      '30s', 0, register_set)
                assert False

        """Setp 2 Set Value"""
        set_value = strToBase64(''.join(re_result))
        data = f"dev={device['device_number']}&field={register_set}&invalid_time=2022-11-19%2000%3A00%3A00&operator=neon&module_type=1&save_flag=1&value={set_value}"
        response = requests.get(url=realExec, params=data)
        assert json.loads(response.text).get('message') == 'SUCCESS'
        cmdID = json.loads(response.text).get('result')
        print(cmdID)
        data = 'cmd=' + cmdID
        for i in range(15):
            if i == 14:
                print('the command was executed over 30s')
                dbConnect.save_result(table_name, 'get_result', 'time out', 'get_value',
                                      '30s', 0, register_set)
                assert False
            get_result = requests.get(url=realGet, params=data)
            if json.loads(get_result.text).get('message') == 'SUCCESS':
                if json.loads(get_result.text).get('result').get('result') == 'S':
                    result_data = json.loads(get_result.text).get('result').get('data')
                    print('Command executed successfully: ', result_data)
                    re_result = re.findall('(?<==).*$', result_data)
                    print(re_result)
                    dbConnect.save_result(table_name, 'set_result', 'Success', 'set_value',
                                          re_result, 0, register_set)
                    assert len(re_result) != 0
                    break
                elif json.loads(get_result.text).get('result').get('result') == 'W':
                    time.sleep(2)
                    i = + 1
                    continue
                elif json.loads(get_result.text).get('result').get('result') == 'F':
                    if '-' in json.loads(get_result.text).get('result').get('data'):
                        pool = redis.ConnectionPool(host='1.14.167.253', port=6379, db=0, password='test123')
                        r = redis.Redis(connection_pool=pool)
                        keys = 'h:ApiResponse:' + cmdID
                        p = eval(json.dumps(r.get(keys).decode('utf-8')))
                        if json.loads(p).get('RetType') == -99999:
                            print('Running...')
                            time.sleep(2)
                            i = + 1
                            continue
                        elif json.loads(p).get('RetType') == 0:
                            print('Running...')
                            continue
                        else:
                            print('[Error Type]', json.loads(p).get('RetType'))
                            print('[Error Data]', json.loads(p).get('RetData'))
                            dbConnect.save_result(table_name, 'set_result', json.loads(p).get('RetType'), 'set_value',
                                                  json.loads(p).get('RetData'), 0, register_set)
                            assert False
                else:
                    time.sleep(2)
                    i = + 1

            else:
                assert json.loads(get_result.text).get('message') == 'SUCCESS'
            print(i)
            if i == 14:
                print('the command was executed over 30s')
                dbConnect.save_result(table_name, 'set_result', 'time out', 'set_value',
                                      '30s', 0, register_set)
                assert False
