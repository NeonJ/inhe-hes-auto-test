# -*-coding:utf-8-*-
"""
# File       : test_interface.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

import requests,time

from common.HESRequest import *
from common.marker import *
from common.YamlConfig import nacosConfig


class Test_Meter_Status:

    @smokeTest
    def test_get_meter_status(self,device,hesURL):
        """
        验证接口获取电表状态字
        """
        data = "/Mdm/GetMeterStatus?MeterNo={}".format(device['device_number'])
        response, elapsed = HESRequest().get(url=hesURL + data, params=None)
        print(response)
        assert response['code'] == 200

    @smokeTest
    def test_get_meter_time(self, device, hesURL):
        """
        同步读取时间，同步修改时间
        """
        data = "/Mdm/getTime?deviceNo={}&deviceType=1&taskType=0".format(device['device_number'])
        response, elapsed = HESRequest().get(url=hesURL + data, params=None)
        assert response['code'] == 200
        assert response['data']['year'] == int(time.strftime("%Y"))
        assert response['data']['month'] == int(time.strftime("%m"))
        # assert response['data']['day'] == int(time.strftime("%d"))
        # assert response['data']['hour'] == int(time.strftime("%H"))
        # assert response['data']['minute'] == int(time.strftime("%M"))

        params = {
            'deviceNo': '{}'.format(device['device_number']),
            'transactionId': 'string',
            'deviceType': 1,
            'taskType': 0
        }
        params.update(response['data'])
        data = "/Mdm/setTime"
        response, elapsed = HESRequest().post(url=hesURL + data, params=params)
        assert response['code'] == 200

    @smokeTest
    @pytest.mark.skipif(nacosConfig()['Device']['connect_type'] == 'Short', reason='Short Meter no online status')
    def test_get_device_online1(self, device, hesURL):
        """
        验证接口获取电表和DCU上下线状态 GetOnlineDevice
        """
        data = "/OnlineDevice/GetOnlineDevice?deviceNo={}".format(device['device_number'])
        response = requests.get(url=hesURL + data, params=None)
        assert str(device['device_number']) in response.text

    @smokeTest
    @pytest.mark.skipif(nacosConfig()['Device']['connect_type'] == 'Short', reason='Short Meter no online status')
    def test_get_device_online2(self, device, hesURL):
        """
        验证接口获取电表和DCU上下线状态 getMeterOnlineStatus
        """
        data = "/Mdm/getMeterOnlineStatus?meterNo={}".format(device['device_number'])
        response = requests.get(url=hesURL + data, params=None)
        assert "Online" in response.text

    @smokeTest
    @pytest.mark.skipif(nacosConfig()['Device']['connect_type'] == 'Short', reason='Short Meter no online status')
    def test_get_device_online3(self, device, hesURL):
        """
        验证接口获取电表和DCU上下线状态 getDeviceNoOnlineStatus
        """
        data = "/Mdm/getDeviceNoOnlineStatus?deviceNo={}".format(device['device_number'])
        response = requests.get(url=hesURL + data, params=None)
        assert "Online" in response.text

    @smokeTest
    def test_MasterCoreState(self, hesURL):
        """
        验证接口获取MasterCore任务状态
        """
        data = "/Monitor/GetMasterCoreState"
        response = requests.get(url=hesURL + data)
        print('Response --- ', response.json())
        assert response.json()['CurrentTime'] != ''

    @smokeTest
    def test_SuspendMasterCoreTask1(self, hesURL):
        """
        验证接口暂停MasterCore任务生成，加载，分发
        """
        data = "/Monitor/SuspendMasterCoreTask?signal=2"  # 暂停
        response = requests.get(url=hesURL + data)
        print('Response --- ', response.text)
        assert 'Suspend' in response.text

    @smokeTest
    def test_SuspendMasterCoreTask2(self, hesURL):
        """
        验证接口启动MasterCore任务生成，加载，分发
        """
        data = "/Monitor/SuspendMasterCoreTask?signal=1"  # 启动
        response = requests.get(url=hesURL + data)
        print('Response --- ', response.text)
        assert 'Start' in response.text
