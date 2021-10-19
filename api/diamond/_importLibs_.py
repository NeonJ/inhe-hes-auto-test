# -*- coding: UTF-8 -*-

from api._importLibs_ import *


try:
    import dlms.diamond
except ImportError:
    pass

try:
    from projects.diamond import OBIS
except ImportError:
    pass