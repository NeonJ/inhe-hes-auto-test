# -*-coding:utf-8-*-
"""
# File       : test_hes_regsiter_check.py
# Time       ：2021/5/12 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

from common.DB import *
from common.HESRequest import HESRequest
from common.marker import *
from config.settings import *


class Test_HES_Register_Check:
    """
    根据转化后的Register进行OBIS Check,并将结果输出到数据库结果表
    """

    def read_config(file_path):
        """读取配置文件内容"""
        with open(file_path, encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config

    def get_db_register(project, action):
        register_list = []
        database = DB(source=setting[project]['db_source'], host=setting[project]['db_host'],
                      database=setting[project]['db_database'], username=setting[project]['db_user'],
                      passwd=setting[project]['db_pwd'], port=setting[project]['db_port'],
                      sid=setting[project]['db_service'])
        table_name = database.orcl_find_last_result()[0]
        user_config = read_config("config/hesCase.yaml")
        obis_sql1 = "select register_id, class_id, index_id, register_type,data_type_int, rw from "
        obis_sql2 = " where PTL_TYPE = (select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no = '{}'))".format(
            user_config['Device']['device_number'])
        print('Result Table Name: ', table_name)
        sql = obis_sql1 + '{}'.format(table_name) + obis_sql2.format()
        db_queue = database.orcl_fetchall_dict(sql)
        for queue in db_queue:
            if queue.get('RW') == action:
                register_list.append(queue.get('REGISTER_ID'))
        return register_list

    @OBISTest
    @pytest.mark.parametrize('register_get', get_db_register(Project.name, 'r'))
    def test_register_get(self, register_get, get_database, get_result_table, caseData):
        print("Register_ID:{}".format(register_get))
        data, user_config = caseData('testData/empower/OBISCheck/register_get.json'.format(Project.name))[
            'register_get']
        requestData = data['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_get
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        for payload in response.get('payload'):
            if payload.get('data') == []:
                print("RegisterID ERROR", response.get('payload'))
                assert False
            else:
                continue
        for payload in response.get('payload'):
            for data in payload.get('data'):
                print('Get Value: ', data.get('resultValue'))
                get_database.save_result(get_result_table, 'get_result', data.get('resultDesc'), register_get)
                get_database.save_result(get_result_table, 'get_value', data.get('resultValue'), register_get)
            assert data.get('resultDesc') == 'OK'

    @OBISTest
    @pytest.mark.parametrize('register_set', get_db_register(Project.name, 'rw'))
    def test_register_set(self, register_set, get_database, get_result_table, caseData):
        print("Register_ID:{}".format(register_set))
        data, user_cofnig = caseData('testData/empower/OBISCheck/register_get.json')
        requestData = data['register_get']['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_set
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        response = HESRequest().post(url=Project.request_url, params=requestData)
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
                get_database.save_result(get_result_table, 'get_result', data.get('resultDesc'),
                                         register_set)
                get_database.save_result(get_result_table, 'get_value', data.get('resultValue'),
                                         register_set)

        data, user_config = caseData('testData/empower/OBISCheck/register_set.json')
        requestData = data['register_set']['request']
        requestData['payload'][0]['data'][0]['registerId'] = register_set
        requestData['payload'][0]['data'][0]['parameter'] = parameter
        requestData['payload'][0]['deviceNo'] = user_config['Device']['device_number']
        response = HESRequest().post(url=Project.request_url, params=requestData)
        for payload in response.get('payload'):
            for data in payload.get('data'):
                print('Set Value: ', data.get('resultValue'))
                get_database.save_result(get_result_table, 'set_result', data.get('resultDesc'),
                                         register_set)
                get_database.save_result(get_result_table, 'set_value', data.get('resultValue'),
                                         register_set)
                assert data.get('resultDesc') == 'OK'

    def test_register_action(self, register_action, get_project_config, get_database, get_result_table):
        pass
