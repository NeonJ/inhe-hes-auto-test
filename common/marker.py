"""
# File       : marker.py
# Time       ：2021/5/13 9:18
# Author     ：黄大彬
# version    ：python 3.7
"""

import pytest

smokeTest = pytest.mark.smokeTest  # 版本发布冒烟测试

fullTest = pytest.mark.fullTest  # 全量测试

hesSyncTest = pytest.mark.hesSyncTest  # HES同步功能测试

hesAsyncTest = pytest.mark.hesAsyncTest  # HES异步功能测试

OBISTest = pytest.mark.OBISTest  # HES接口检查电表OBIS

hesSyncTest1 = pytest.mark.hesSyncTest1

hesAsyncTest1 = pytest.mark.hesAsyncTest1
