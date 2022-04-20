# -*- coding: utf-8 -*-
# @Time : 2021/12/22 9:52
# @Author : JingYang
# @File : test_GetProfileMonthly.py


import requests


class Test_GetProfileMonthly:

    def test_GetProfileMonthly(self, url, caseData):
        testUrl = url + '/api/v1/Request/RequestMessage'
        data, user_config = caseData('testData/HESAPI/RequestMessage/getProfile_Monthly.json')['test_GetProfileMonthly']
        requestData = data['request']
        expectResJson = data['response']
        response = requests.post(url=testUrl, json=requestData)

        assert response.status_code == 200
        assert AssertIn().checkIn(expectResJson, response.json()) is True