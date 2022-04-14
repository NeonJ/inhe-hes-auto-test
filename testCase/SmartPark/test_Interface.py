# -*-coding:utf-8-*-
"""
# File       : test_interface.py
# Time       ：2022/2/9 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""
import time

import requests

from common.UtilTools import compareJson
from common.marker import *
from config.settings import *


class Test_Interface:

    @interfaceTest
    def test_install_meter_third_party(self, token,caseData):
        """
        正常接口安装电表
        """
        data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['install_meter_request']
        resp_data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['install_response']
        data['regionNo'] = setting[Project.name]['meter_no']
        data['deviceNo'] = setting[Project.name]['meter_no']
        data['deviceType'] = 1
        data['installDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['installOperatorName'] = "AutoTest"
        data['totalUsage'] = 11.11
        data['unit'] = "kWh"
        print(data)
        print(token)
        print(HESAPI(Address=setting[Project.name]['api_url']).installAddress())
        response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).installAddress(),headers=token,
                                 json=data)
        print(response.text)
        assert response.status_code == 200
        assert compareJson(response.text, resp_data)

    # @interfaceTest
    def test_uninstall_meter_third_party(self, caseData):
        """
        正常接口卸载电表
        """
        data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['uninstall_meter_request']
        resp_data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['uninstall_response']
        data['deviceNo'] = setting[Project.name]['meter_no']
        data['deviceType'] = 1
        data['removeDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['removeOperatorName'] = "AutoTest"
        data['totalUsage'] = 12.12
        data['unit'] = "kWh"
        print(data)
        response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).installAddress(),
                                 json=data)
        assert response.status_code == 200
        assert compareJson(response.text, resp_data)

    # # @interfaceTest
    # @pytest.mark.parametrize('regionNo,deviceNo,deviceType,installDate,installOperatorName,totalUsage,unit',
    #                          [('', '1234567891', 10, '2021-11-16 18:00:00', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', '', 10, '2021-11-16 18:00:00', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', '1234567891', None, '2021-11-16 18:00:00', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', '1234567891', 10, '', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', '1234567891', 10, '2021-11-16 18:00:00', '', 11.11, 'kWh'),
    #                           ('1234567910', '1234567891', 10, '2021-11-16 18:00:00', 'AutoTest', None, 'kWh'),
    #                           ('1234567910', '1234567891', 10, '2021-11-16 18:00:00', 'AutoTest', 11.11, '')])
    # def test_install_meter_third_party_abnormal(self, regionNo, deviceNo, deviceType, installDate, installOperatorName,
    #                                             totalUsage, unit, caseData):
    #     """
    #     异常请求安装电表
    #     """
    #     data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['install_meter_request']
    #     resp_data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['install_response']
    #     data['regionNo'] = regionNo
    #     data['deviceNo'] = deviceNo
    #     data['deviceType'] = deviceType
    #     data['installDate'] = installDate
    #     data['installOperatorName'] = installOperatorName
    #     data['totalUsage'] = totalUsage
    #     data['unit'] = unit
    #     print(data)
    #     response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).installAddress(),
    #                              json=data)
    #     assert response.status_code == 200
    #     assert 'error' in response.text
    #
    # # @interfaceTest
    # @pytest.mark.parametrize('deviceNo,deviceType,removeDate,removeOperatorName,totalUsage,unit',
    #                          [('', 10, '2021-11-16 18:00:00', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', '', '2021-11-16 18:00:00', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', 10, '', 'AutoTest', 11.11, 'kWh'),
    #                           ('1234567910', 10, '2021-11-16 18:00:00', '', 11.11, 'kWh'),
    #                           ('1234567910', 10, '2021-11-16 18:00:00', 'AutoTest', '', 'kWh'),
    #                           ('1234567910', 10, '2021-11-16 18:00:00', 'AutoTest', 11.11, '')])
    # def test_uninstall_meter_third_party_abnormal(self, caseData):
    #     """
    #     正常接口卸载电表
    #     """
    #     data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['uninstall_meter_request']
    #     resp_data = caseData('testData/{}/InstallUninstallMeter.json'.format(Project.name))['uninstall_response']
    #     data['deviceNo'] = setting[Project.name]['meter_no']
    #     data['deviceType'] = 1
    #     data['removeDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     data['removeOperatorName'] = "AutoTest"
    #     data['totalUsage'] = 12.12
    #     data['unit'] = "kWh"
    #     print(data)
    #     response = requests.post(url=HESAPI(Address=setting[Project.name]['api_url']).installAddress(),
    #                              json=data)
    #     assert response.status_code == 200
    #     assert compareJson(response.text, resp_data)
