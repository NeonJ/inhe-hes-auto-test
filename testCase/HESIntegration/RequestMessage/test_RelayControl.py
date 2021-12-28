# -*- coding: utf-8 -*-
# @Time : 2021/12/8 14:25
# @Author : JingYang
# @File : Test_RelayControl.py

import allure, pytest, requests
from common.UtilTools import *

class Test_RelayControl:


    # Step1:relayStatus= on,
    # Step1:relayStatus= off,
    def test_RELAY_CONTROL_RELAYON(self,url,caseData):

        url = url +'/api/v1/Request/RequestMessage'

        data = caseData('testData/HESAPI/RequestMessage/relayControl.json')['test_RELAY_CONTROL_RELAYON']
        requestData = data['request']
        expectResJson = data['response']
        response = requests.post(url=url,json=requestData)
        print(response.json())

        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True


    def test_RELAY_CONTROL_RELAYOFF(self,url,caseData):

        url = url +'/api/v1/Request/RequestMessage'

        data = caseData('testData/HESAPI/RequestMessage/relayControl.json')['test_RELAY_CONTROL_RELAYOFF']
        requestData = data['request']
        expectResJson = data['response']
        response = requests.post(url=url,json=requestData)
        print(response.json())

        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True

