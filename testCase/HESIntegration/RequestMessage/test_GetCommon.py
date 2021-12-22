# -*- coding: utf-8 -*-
# @Time : 2021/12/9 9:21
# @Author : JingYang
# @File : test_GetCommon.py
import sys

import allure, pytest, requests,logging
from common.UtilTools import *

class Test_GetCommon:

    # Search register_id  9300

    def test_GET_COMMOM(self,url,caseData):

        testUrl = url +'/api/v1/Request/RequestMessage'
        data = caseData('testData/HESAPI/RequestMessage/getCommon.json')['test_GET_COMMOM']
        requestData = data['request']
        expectResJson = data['response']
        response = requests.post(url=testUrl,json=requestData)



        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True

