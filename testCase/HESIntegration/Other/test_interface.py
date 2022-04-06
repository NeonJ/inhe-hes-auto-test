# -*-coding:utf-8-*-
"""
# File       : test_interface.py
# Time       ：2021/12/21 14:18
# Author     ：cao jiann
# version    ：python 3.7
"""

from common.marker import *
from config.settings import *
import requests


class Test_Meter_Status:

    @hesSyncTest
    def test_get_meter_status(self):
        """
        验证接口获取电表状态字
        """
        data = "/Mdm/GetMeterStatus?MeterNo={}".format(setting[Project.name]['meter_no'])
        response = HESRequest().get(url=setting[Project.name]['api_url'] + data, params=None)
        assert response['code'] == 200

    @hesSyncTest
    def test_get_device_online1(self):
        """
        验证接口获取电表和DCU上下线状态 GetOnlineDevice
        """
        data = "/OnlineDevice/GetOnlineDevice?deviceNo={}".format(setting[Project.name]['meter_no'])
        response = HESRequest().get(url=setting[Project.name]['api_url'] + data, params=None)
        assert response['DeviceNo'] == setting[Project.name]['meter_no']

    @hesSyncTest
    def test_get_device_online2(self):
        """
        验证接口获取电表和DCU上下线状态 getMeterOnlineStatus
        """
        data = "/Mdm/getMeterOnlineStatus?meterNo={}".format(setting[Project.name]['meter_no'])
        response = HESRequest().get(url=setting[Project.name]['api_url'] + data, params=None)
        assert response['desc'] == "Online"

    @hesSyncTest
    def test_get_device_online3(self):
        """
        验证接口获取电表和DCU上下线状态 getDeviceNoOnlineStatus
        """
        data = "/Mdm/getDeviceNoOnlineStatus?deviceNo={}".format(setting[Project.name]['meter_no'])
        response = HESRequest().get(url=setting[Project.name]['api_url'] + data, params=None)
        assert response['desc'] == "Online"

    @hesSyncTest
    def test_MasterCoreState(self):
        """
        验证接口获取MasterCore任务状态
        """
        data = "/Monitor/GetMasterCoreState"
        response = HESRequest().get(url=setting[Project.name]['api_url'] + data, params=None)
        print(response)
        assert response['CurrentTime'] != ''

    @hesSyncTest
    def test_SuspendMasterCoreTask1(self):
        """
        验证接口暂停和启动MasterCore任务生成，加载，分发
        """
        data = "/Monitor/SuspendMasterCoreTask?signal=2"  # 暂停
        response = requests.get(url=setting[Project.name]['api_url'] + data)
        assert 'Suspend' in response.text

    @hesSyncTest
    def test_SuspendMasterCoreTask2(self):
        """
        验证接口暂停和启动MasterCore任务生成，加载，分发
        """
        data = "/Monitor/SuspendMasterCoreTask?signal=1"  # 启动
        response = requests.get(url=setting[Project.name]['api_url'] + data)
        assert 'Start' in response.text

