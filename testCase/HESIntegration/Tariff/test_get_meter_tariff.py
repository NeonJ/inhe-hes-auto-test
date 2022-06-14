# -*- coding: utf-8 -*-
# @Time : 2021/12/22 17:30
# @Author : JingYang
# @File : test_GetMeterTariff.py
from common.HESRequest import *
from common.marker import *


class Test_Get_Meter_Tariff:

    @smokeTest
    def test_GetMeterTariff_Active(self, hesURL, device, caseData):
        url = hesURL + '/Tariff/GetMeterTariff'
        data = caseData('testData/Tariff/getMeterTariff.json')
        requestData = data['test_GetMeterTariff_Active']
        requestData['meterNo'] = device['device_number']

        expectResJson = requestData['response']
        response, elapsed = HESRequest().get(url=url, params=requestData)
        print('Response --- ', response)
        assert 'activeTariff' in str(response)
        # assert AssertIn().checkIn(expectResJson,response.json()) is True

    @smokeTest
    def test_GetMeterTariff_Passive(self, hesURL, device, caseData):
        url = hesURL + '/Tariff/GetMeterTariff'
        data = caseData('testData/Tariff/getMeterTariff.json')
        requestData = data['test_GetMeterTariff_Passive']
        requestData['meterNo'] = device['device_number']

        expectResJson = requestData['response']
        response, elapsed = HESRequest().get(url=url, params=requestData)
        print('Response --- ', response)
        assert 'scriptSelector' in str(response)
        # assert AssertIn().checkIn(expectResJson, response.json()) is True

    @smokeTest
    def test_GetMeterTariff_All(self,  hesURL, device, caseData):
        url = hesURL + '/Tariff/GetMeterTariff'
        print("get request data")
        # request parameter:get all tariff
        data = caseData('testData/Tariff/getMeterTariff.json')
        requestData = data['test_GetMeterTariff_All']
        requestData['meterNo'] = device['device_number']


        expectResJson = requestData['response']
        response, elapsed = HESRequest().get(url=url, params=requestData)
        print('Response --- ', response)
        assert 'scriptSelector' in str(response)
        # assert AssertIn().checkIn(expectResJson, response.json()) is True
