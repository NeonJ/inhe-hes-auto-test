# -*- coding: UTF-8 -*-

try:
    import dlms.diamond
except ImportError:
    pass

try:
    from projects.diamond import OBIS
except ImportError:
    pass
