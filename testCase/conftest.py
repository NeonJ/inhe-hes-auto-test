# import allure
# import pytest, json, os
#
# from config.settings import *
#
#
# @allure.step("获取服务端网关地址")
# @pytest.fixture(scope='session', autouse=True)
# def url():
#     yield setting[Project.name]['api_url']
#
#
#
# @allure.step("获取TestData")
# @pytest.fixture()
# def caseData():
#     def loadData(path):
#         filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
#         with open(filepath, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     return loadData
#
#
#
# @allure.step("项目名称")
# @pytest.fixture(scope='session', autouse=True)
# def project():
#     yield Project.name
import pytest

#
# @pytest.fixture(scope='session', autouse=True)
# def project():
#     print(1111)