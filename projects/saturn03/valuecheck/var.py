# -*- coding:utf-8 -*-
# @Time     :2020/12/8
# @Author   :yimou
# @Version  :v1
# @Updated  :0000/00/00
# @RunTime  :
import re

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

# 过滤不支持的OBIS
supported_objects = ["", "nan", 'NA']

all_data_type = ["null_data", "boolean", "bit_string", "double_long",
                 "double_long_unsigned", "octet_string", "visible_string",
                 "utf8_string", "bcd", "integer", "long", "unsigned",
                 "long_unsigned", "long64", "long64_unsigned", "enum",
                 "float32", "float64", "date_time", "date", "time"]
