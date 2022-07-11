# _*_ coding: utf-8 _*_
# @Time      : 2022/7/11 9:08
# @Author    : Jiannan Cao
# @FileName  : test_get_meter_tariff_new.py
from common.HESRequest import *
from common.marker import *
from common.YamlConfig import nacosConfig

class Test_Get_Meter_Tariff_New:

    @smokeTest
    def test_get_tariff_new_all(self, caseData, requestMessage, device):
        """
        使用RequestMessage请求Active和Passive费率
        """
        data = caseData('testData/Tariff/tariff.json')
        requestData = data['get_tariff']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        requestData['payload'][0]['data'][0]['parameter']['tariffType'] = 0
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ',response)
        assert response.get('reply')['replyCode'] == 200
        assert 'activeTariff' in str(response)

    @smokeTest
    def test_get_tariff_new_active(self, caseData, requestMessage, device):
        """
        使用RequestMessage请求Active费率
        """
        data = caseData('testData/Tariff/tariff.json')
        requestData = data['get_tariff']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        requestData['payload'][0]['data'][0]['parameter']['tariffType'] = 1
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ',response)
        assert response.get('reply')['replyCode'] == 200
        assert 'activeTariff' in str(response)

    @smokeTest
    def test_get_tariff_new_passive(self, caseData, requestMessage, device):
        """
        使用RequestMessage请求Passive费率
        """
        data = caseData('testData/Tariff/tariff.json')
        requestData = data['get_tariff']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        requestData['payload'][0]['data'][0]['parameter']['tariffType'] = 2
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ',response)
        assert response.get('reply')['replyCode'] == 200
        assert 'passive' in str(response)