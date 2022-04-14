# -*- coding: UTF-8 -*-


# 根据项目名动态加载dlms库
from libs.Singleton import Singleton
project = Singleton().Project



try:
    from dlms.base import *

    mod = __import__(f'dlms.{project}', fromlist=['all'])
    for c in [cls for cls in dir(mod) if not cls.startswith('__')]:
        globals()[c] = getattr(mod, c)
except ModuleNotFoundError:
    pass


try:
    from api.base import *

    mod = __import__(f'api.{project}', fromlist=['all'])
    for c in [cls for cls in dir(mod) if not cls.startswith('__')]:
        globals()[c] = getattr(mod, c)

except ModuleNotFoundError:
    pass
