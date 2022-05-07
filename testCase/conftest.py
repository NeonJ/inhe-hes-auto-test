import allure
import nacos
import pytest
import requests
import os,yaml

from common.DB import *


# def pytest_addoption(parser):  # 定义命令行参数,参数必须保持两个--
#     parser.addoption("--project", action="store", help="project")  # 服务名称
#     parser.addoption("--tag", action="store", help="case tag")  # marker，用例标签
#     parser.addoption("--path", action="store", help="report  path")
#     parser.addoption("--resume", action="store", help="continue last obis check")
#     parser.addoption("--retry", action="store", help='failed retries')
#     parser.addoption("--group", action="store", help='nacos group')
#
#
# @pytest.fixture(scope='session', autouse=True)
# def config(request):  # 获取参数值,与上述添加对应
#     config_dict = {}
#     config_dict['nacos_url'] = 'http://10.32.234.198:8848'
#     config_dict['project'] = request.config.getoption("--project")
#     config_dict['tag'] = request.config.getoption("--tag")
#     config_dict['path'] = request.config.getoption("--path")
#     config_dict['resume'] = request.config.getoption("--resume")
#     config_dict['retry'] = request.config.getoption("--retry")
#     config_dict['group'] = request.config.getoption("--group")
#     return config_dict


@pytest.fixture(scope='session', autouse=True)
def readConfig():
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + os.path.sep + 'config'),
                                    'settings.yaml')
    with open(config_file_path, 'r') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result


@pytest.fixture(scope='session', autouse=True)
def nacosData(readConfig):
    client = nacos.NacosClient(server_addresses=readConfig['nacos_url'], namespace='HES', username="nacos",
                               password="nacos")
    data_id = readConfig['project']
    group = readConfig['group']
    config = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
    return config


@allure.step("获取hes-api地址")
@pytest.fixture(scope='session')
def hesURL(nacosData):
    yield nacosData['URL']['hes_url']


@allure.step("RequestMessage")
@pytest.fixture(scope='session')
def requestMessage(nacosData):
    yield nacosData['URL']['hes_url'] + '/api/v1/Request/RequestMessage'


@allure.step("获取web网关地址")
@pytest.fixture(scope='session')
def gatewayURL(nacosData):
    yield nacosData['URL']['gateway_url']


@allure.step("获取kafka地址")
@pytest.fixture(scope='session')
def kafkaURL(nacosData):
    yield nacosData['URL']['kafka_url']


@allure.step("获取请求体")
@pytest.fixture(scope='session')
def caseData():
    def loadData(path):
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        with open(filepath, 'r', encoding='utf-8') as f:
            file = json.load(f)
        return file

    return loadData


@allure.step("获取数据库信息")
@pytest.fixture(scope='session')
def databaseConfig(nacosData):
    return nacosData['DATABASE']


@allure.step("获取数据库对象")
@pytest.fixture(scope='session')
def dbConnect(nacosData):
    database = DB(source=nacosData['DATABASE']['db_source'], host=nacosData['DATABASE']['db_host'],
                  database=nacosData['DATABASE']['db_database'], username=nacosData['DATABASE']['db_user'],
                  passwd=nacosData['DATABASE']['db_pwd'], port=nacosData['DATABASE']['db_port'],
                  sid=nacosData['DATABASE']['db_service'])
    return database


@allure.step("获取测试设备信息")
@pytest.fixture(scope='session')
def device(nacosData):
    return nacosData['Device']


@allure.step("获取日结操作信息")
@pytest.fixture(scope='session')
def daily(nacosData):
    return nacosData['Daily']


@allure.step("获取月结操作信息")
@pytest.fixture(scope='session')
def monthly(nacosData):
    return nacosData['Monthly']


@allure.step("获取能量曲线操作信息")
@pytest.fixture(scope='session')
def lp(nacosData):
    return nacosData['LP']


@allure.step("获取质量曲线操作信息")
@pytest.fixture(scope='session')
def pq(nacosData):
    return nacosData['PQ']


@allure.step("获取事件操作信息")
@pytest.fixture(scope='session')
def event(nacosData):
    return nacosData['Event']


@allure.step("获取拉合闸操作信息")
@pytest.fixture()
def relay(nacosData):
    return nacosData['Relay']


@allure.step("获取Web Token")
@pytest.fixture(scope='session')
def token(nacosData):
    re = requests.post(url=nacosData['URL']['gateway_url'] + '/api/gateway-service/tokens.json',
                       json={"language": "en", "username": nacosData['URL']['ami_user'],
                             "password": nacosData['URL']['ami_passwd']})
    access_token = re.json()['data']['access_token']
    yield {'Access-Token': access_token, 'Application-Id': 'AMI_WEB'}

# def caseData():
#     def loadData(path):
#         filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
#         with open(filepath, 'r', encoding='utf-8') as f:
#             file =  json.load(f)
#         # with open("config/hesCase.yaml", encoding="utf-8") as f:
#         #     config = yaml.load(f, Loader=yaml.FullLoader)
#         client = nacos.NacosClient(server_addresses=Project.nacos_url, namespace='HES', username="nacos", password="nacos")
#         data_id = Project.name
#         group = Project.group
#         config = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
#         return file, config
#     return loadData
