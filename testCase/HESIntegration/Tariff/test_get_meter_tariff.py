# -*- coding: utf-8 -*-
# @Time : 2021/12/22 17:30
# @Author : JingYang
# @File : test_GetMeterTariff.py
from common.HESRequest import HESRequest
from common.marker import *
from config.settings import *


class Test_Get_Meter_Tariff:

    @smokeTest
    def test_GetMeterTariff_Active(self, url, caseData):
        url = url + '/Tariff/GetMeterTariff'
        print("get request data")
        # active request parameter
        data, user_config = caseData('testData/empower/Tariff/getMeterTariff.json')
        requestData = data['test_GetMeterTariff_Active']
        requestData['meterNo'] = setting[Project.name]['meter_no']

        expectResJson = data['response']
        response = HESRequest().get(url=url, params=requestData)
        print(response)
        assert 'activeTariff' in str(response)
        # assert AssertIn().checkIn(expectResJson,response.json()) is True

    @smokeTest
    def test_GetMeterTariff_Passive(self, url, caseData):
        url = url + '/Tariff/GetMeterTariff'
        print("get request data")
        # passive request parameter
        data, user_config = caseData('testData/empower/Tariff/getMeterTariff.json')
        requestData = data['test_GetMeterTariff_Passive']
        requestData['meterNo'] = setting[Project.name]['meter_no']

        response = HESRequest().get(url=url, params=requestData)
        print(response)

        assert 'Neon' in str(response)
        # assert AssertIn().checkIn(expectResJson, response.json()) is True

    @smokeTest
    def test_GetMeterTariff_All(self, url, caseData):
        url = url + '/Tariff/GetMeterTariff'
        print("get request data")
        # request parameter:get all tariff
        data, user_config = caseData('testData/empower/Tariff/getMeterTariff.json')
        requestData = data['test_GetMeterTariff_All']
        requestData['meterNo'] = setting[Project.name]['meter_no']

        response = HESRequest().get(url=url, params=requestData)
        print(response)

        assert 'Neon' in str(response)
        # assert AssertIn().checkIn(expectResJson, response.json()) is True