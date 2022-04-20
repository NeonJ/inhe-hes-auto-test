import allure
import pytest
import requests

from common.DB import *
from config.settings import *


@allure.step("获取服务端网关地址")
@pytest.fixture(scope='session')
def url():
    yield setting[Project.name]['api_url']


@allure.step("获取TestData")
@pytest.fixture(scope='session')
def caseData():
    def loadData(path):
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        with open(filepath, 'r', encoding='utf-8') as f:
            file =  json.load(f)
        with open("config/hesCase.yaml", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return file, config
    return loadData


@allure.step("项目名称")
@pytest.fixture(scope='session')
def project():
    yield Project.name


@allure.step("Web Token")
@pytest.fixture(scope='session')
def token():
    re = requests.post(url=setting[Project.name]['web_url'] + '/api/gateway-service/tokens.json',
                       json={"language": "en", "username": setting[Project.name]['ami_user'],
                             "password": setting[Project.name]['ami_passwd']})
    access_token = re.json()['data']['access_token']

    yield {'Access-Token': access_token, 'Application-Id': 'AMI_WEB'}
