"""
# File       : marker.py
# Time       ：2021/5/13 9:18
# Author     ：黄大彬
# version    ：python 3.7
"""

import pytest

smokeTest = pytest.mark.smokeTest  # 版本发布冒烟测试

fullTest = pytest.mark.fullTest  # 全量测试

hesTest = pytest.mark.hesTest