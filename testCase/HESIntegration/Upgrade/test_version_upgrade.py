# _*_ coding: utf-8 _*_
# @Time      : 2022/7/13 8:41
# @Author    : Jiannan Cao
# @FileName  : test_version_upgrade.py
import datetime

from kafka import KafkaConsumer

from common.HESRequest import *
from common.marker import *


class Test_Meter_Upgrade:

    @asyncTest
    def test_meter_app_upgrade(self, caseData, requestMessage, device, kafkaURL):
        """
        模拟页面对测试电表进行APP升级
        """
        pass

    @asyncTest
    def test_meter_legal_upgrade(self, caseData, requestMessage, device, kafkaURL):
        """
        模拟页面对测试电表进行Legal升级
        """
        pass

    @asyncTest
    def test_meter_module_upgrade(self, caseData, requestMessage, device, kafkaURL):
        """
        模拟页面对测试电表进行Module升级
        """
        pass
