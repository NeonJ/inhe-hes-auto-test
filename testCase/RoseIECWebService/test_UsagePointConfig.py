# _*_ coding: utf-8 _*_
# @Time      : 2022/3/17 13:51
# @Author    : Jiannan Cao
# @FileName  : UsagePointConfig.py

import json
import time

import requests

from common.HESAPI import *
from common.marker import *
from config.settings import *


@RoseIECWebService
class Test_Meter_Daily:
    def test_(self, caseData):
        """
        创建测量点 - 正常创建 返回Success
        """

    def test_(self, caseData):
        """
        创建测量点 - 异常创建 The payload content is missing or wrong
         """

    def test_(self, caseData):
        """
        创建测量点 - 异常创建 Too many items in request(too many UsagePoint object)
         """

    def test_(self, caseData):
        """
        创建测量点 - 异常创建 Area Not Exist,the area must be transformer
         """

    def test_(self, caseData):
        """
        创建测量点 - 异常创建 ServerInnerError
         """

    def test_(self, caseData):
        """
        创建测量点 - 异常创建 The usagepoint is already exist in database, or there are repetition usagepoint number in the request.
         """

    def test_(self, caseData):
        """
        创建测量点 - 异常创建 Repeat object item in payload
         """