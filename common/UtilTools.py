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
    def readJson(self,path,jsonName):
        f = open(path, 'r')
        ret = f.read()
        json_str = json.loads(ret)
        expectResJson = json_str[jsonName]
        return expectResJson


class AssertIn:

    '''所有数据类型的断言'''

    def __init__(self):
        ## 初始化set类型
        self.result = set()

    def _getKeys(self,data):

        ## 等于dict类型
        if type(data) == dict:
            ## 循环走起
            for key,value in data.items():

                ## 若循环的value值为list类型，继续调用
                ## 各个为空处理
                if type(value) == list:
                    if value == []:
                        self.result.add(key)
                        self.result.add(value)
                    else:
                        self._getKeys(value)

                if type(value) == dict:
                    ## 如果dict为空处理
                    if value == {}:
                        self.result.add(key)
                        self.result.add(value)
                    else:
                        self._getKeys(value)
                ## 同list
                if type(value) == tuple:
                    if value == ():
                        self.result.add(key)
                        self.result.add(value)
                    else:
                        self._getKeys(value)
                    self._getKeys(value)

                ## 如果循环的value类型为基本类型，直接添加
                if type(value) in (str,int,float,set):
                    self.result.add(key)
                    self.result.add(value)

        ## 若传入类型为list或者tuple
        if type(data) in (list,tuple):
            ## 依旧循环走起
            for value in data:
                ## list时继续调用
                if type(value) == list:
                    self._getKeys(value)

                ## dict时也继续调用
                if type(value) == dict:
                    self._getKeys(value)

                ## tuple时继续调用
                if type(value) == tuple:
                    self._getKeys(value)

                ## 若为这些类型，直接添加
                if type(value) in (str, int, float, set):
                    self.result.add(value)

        ## 若传入为set类型，直接添加
        if type(data) is set:
            for value in data:
                self.result.add(value)

        return self.result


    def checkIn(self,src,dest):

        ## 比较必须保障类型一致
        try:

            assert type(src) == type(dest)
        except  Exception:

            raise Exception('数据类型不一致')

        ## 赋值第一个参数
        fir = self._getKeys(src)
        ## 重置一下结果
        self._clear()
        ## 赋值第二个参数
        sec = self._getKeys(dest)
        ## 也重置一下吧
        self._clear()

        ## 断言
        if fir.issubset(sec):
            return True
        else:
            return False

    def _clear(self):
        self.result = set()
