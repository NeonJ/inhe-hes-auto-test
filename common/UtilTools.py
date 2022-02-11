# -*- coding: utf-8 -*-
# @Time : 2021/12/8 15:22
# @Author : JingYang
# @File : UtilTools.py
import json


class ReadFile:
    '''
    read json from file
    path：json file path
    '''

    def readJson(self, path, jsonName):
        f = open(path, 'r')
        ret = f.read()
        json_str = json.loads(ret)
        expectResJson = json_str[jsonName]
        return expectResJson


def compareJson(small, big):
    # 判断两个json包含关系
    for skey in small:
        found = False
        for bkey in big:
            bval, sval = bkey, skey  # list values are the keys
            if isinstance(small, dict) and isinstance(big, dict):
                bval, sval = big[bkey], small[skey]  # replace values if dict
            if isinstance(sval, (dict, list)) and isinstance(bval, (dict, list)):
                found = compareJson(sval, bval)
            else:
                found = skey == bkey and sval == bval
            if found: break
        if not found: return False

    return True
