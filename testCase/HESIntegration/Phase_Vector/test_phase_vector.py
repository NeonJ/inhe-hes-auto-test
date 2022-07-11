# _*_ coding: utf-8 _*_
# @Time      : 2022/4/20 16:30
# @Author    : Jiannan Cao
# @FileName  : test_phase_vector.py.py

from common.HESRequest import *
from common.marker import *
from common.YamlConfig import nacosConfig

@pytest.mark.skipif(nacosConfig()['Device']['device_type'] == 'Single', reason='Test meter is single phase')
class Test_Phase_Vector:

    @smokeTest
    def test_get_vector(self, caseData, requestMessage, device):
        """
        使用同步读取三相表或者CT表相位夹角
        """
        data = caseData('testData/PhaseVector/phase_vector.json')
        requestData = data['vector']['request']
        requestData['payload'][0]['deviceNo'] = device['device_number']
        transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
        requestData['payload'][0]['transactionId'] = transactionId
        response, elapsed = HESRequest().post(url=requestMessage, params=requestData)
        print('Response --- ',response)
        assert response.get('reply')['replyCode'] == 200
        assert len(response.get('payload')[0].get('data')[0]) == 18