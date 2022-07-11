"""
# File       : marker.py
# Time       ：2021/5/13 9:18
# Author     ：黄大彬
# version    ：python 3.7
"""

import pytest

smokeTest = pytest.mark.smokeTest  # 版本发布冒烟测试

fullTest = pytest.mark.fullTest  # 全量测试

smokeTest = pytest.mark.smokeTest  # HES同步功能测试

asyncTest = pytest.mark.asyncTest  # HES异步功能测试

obisTest = pytest.mark.obisTest  # HES接口检查电表OBIS

smokeTest1 = pytest.mark.smokeTest1

asyncTest1 = pytest.mark.asyncTest1

RoseIECWebService = pytest.mark.RoseIECWebService

interfaceTest = pytest.mark.interfaceTest