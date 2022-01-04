# -*- coding: utf-8 -*-
# @Time : 2021/12/22 17:30
# @Author : JingYang
# @File : test_GetMeterTariff.py

import allure, pytest, requests

from common.UtilTools import AssertIn
from common.marker import hesSyncTest
from config.settings import *


class Test_GetMeterTariff:

    @hesSyncTest
    def test_GetMeterTariff_Active(self, url, caseData):
        url = url + '/Tariff/GetMeterTariff'
        print("get request data")
        # active request parameter
        data = caseData('testData/HESAPI/Tariff/getMeterTariff.json')['test_GetMeterTariff_Active']
        requestData = data['request']
        requestData['meterNo'] = setting[Project.name]['meter_no']

        expectResJson = data['response']
       # response = requests.get(url=url,  params={'meterNo': 'M202009040003', 'tariffType': 1})
        response = requests.get(url=url,  params=requestData)
        print(response.json())

        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson,response.json()) is True

    @hesSyncTest
    def test_GetMeterTariff_Passive(self, url, caseData):
        url = url + '/Tariff/GetMeterTariff'

        print("get request data")
        # passive request parameter
        data = caseData('testData/HESAPI/Tariff/getMeterTariff.json')['test_GetMeterTariff_Passive']
        requestData = data['request']
        requestData['meterNo'] = setting[Project.name]['meter_no']

        expectResJson = data['response']
        response = requests.get(url=url, params=requestData)
        print(response.json())

        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True

    @hesSyncTest
    def test_GetMeterTariff_All(self, url, caseData):
        url = url + '/Tariff/GetMeterTariff'

        print("get request data")
        # request parameter:get all tariff
        data = caseData('testData/HESAPI/Tariff/getMeterTariff.json')['test_GetMeterTariff_All']
        requestData = data['request']
        requestData['meterNo'] = setting[Project.name]['meter_no']

        expectResJson = data['response']
        response = requests.get(url=url, params=requestData)
        print(response.json())

        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True
