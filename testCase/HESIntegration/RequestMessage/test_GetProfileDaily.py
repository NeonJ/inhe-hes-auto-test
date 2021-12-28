# -*- coding: utf-8 -*-
# @Time : 2021/12/14 14:04
# @Author : JingYang
# @File : test_GetProfileDaily.py


import allure, pytest, requests,logging
from common.UtilTools import *

class Test_GetProfileDaily:

    def test_GetProfileDaily(self, url, caseData):
        testUrl = url + '/api/v1/Request/RequestMessage'
        data = caseData('testData/HESAPI/RequestMessage/getProfile_Daily.json')['test_GetProfileDaily']
        requestData = data['request']
        expectResJson = data['response']
        response = requests.post(url=testUrl, json=requestData)
        print(response.json())
        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True