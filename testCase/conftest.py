import allure
import nacos
import pytest
import requests

from common.DB import *
from config.settings import *


def nacosData():
    client = nacos.NacosClient(server_addresses=Project.nacos_url, namespace='HES', username="nacos", password="nacos")
    data_id = Project.name
    group = Project.group
    config = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
    return config


@allure.step("获取hes-api地址")
@pytest.fixture(scope='session')
def hesURL():
    yield nacosData()['URL']['hes_url']


@allure.step("RequestMessage")
@pytest.fixture(scope='session')
def requestMessage():
    yield nacosData()['URL']['hes_url'] + '/api/v1/Request/RequestMessage'


@allure.step("获取web网关地址")
@pytest.fixture(scope='session')
def gatewayURL():
    yield nacosData()['URL']['gateway_url']


@allure.step("获取kafka地址")
@pytest.fixture(scope='session')
def kafkaURL():
    yield nacosData()['URL']['kafka_url']


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
def databaseConfig():
    return nacosData()['DATABASE']



@allure.step("获取数据库对象")
@pytest.fixture(scope='session')
def dbConnect():
    database = DB(source=nacosData()['DATABASE']['db_source'], host=nacosData()['DATABASE']['db_host'],
                  database=nacosData()['DATABASE']['db_database'], username=nacosData()['DATABASE']['db_user'],
                  passwd=nacosData()['DATABASE']['db_pwd'], port=nacosData()['DATABASE']['db_port'],
                  sid=nacosData()['DATABASE']['db_service'])
    return database


@allure.step("获取测试设备信息")
@pytest.fixture(scope='session')
def device():
    return nacosData()['Device']


@allure.step("获取日结操作信息")
@pytest.fixture(scope='session')
def daily():
    return nacosData()['Daily']


@allure.step("获取月结操作信息")
@pytest.fixture(scope='session')
def monthly():
    return nacosData()['Monthly']


@allure.step("获取能量曲线操作信息")
@pytest.fixture(scope='session')
def lp():
    return nacosData()['LP']


@allure.step("获取质量曲线操作信息")
@pytest.fixture(scope='session')
def pq():
    return nacosData()['PQ']


@allure.step("获取事件操作信息")
@pytest.fixture(scope='session')
def event():
    return nacosData()['Event']


@allure.step("获取拉合闸操作信息")
@pytest.fixture()
def relay():
    return nacosData()['Relay']


@allure.step("项目名称")
@pytest.fixture(scope='session')
def project():
    yield Project.name


@allure.step("获取Web Token")
@pytest.fixture(scope='session')
def token():
    re = requests.post(url=nacosData()['URL']['gateway_url'] + '/api/gateway-service/tokens.json',
                       json={"language": "en", "username": nacosData()['URL']['ami_user'],
                             "password": nacosData()['URL']['ami_passwd']})
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
