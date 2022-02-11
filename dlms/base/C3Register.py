# -*- coding: UTF-8 -*-

from libs.Singleton import Singleton

from dlms.DlmsClass import *


class C3Register(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "value",
        3: "scaler_unit"
    }

    action_index_dict = {
        1: "reset"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=3)

    # Attribute of logical_name (No.1)
    @formatResponse
    def get_logical_name(self, dataType=False, response=None):
        """
        获取 logical_name 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            点分十进制形式的OBIS值
        """
        if response is None:
            response = self.getRequest(1)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]
        if dataType:
            return hex_toOBIS(ret[0]), ret[1]
        return hex_toOBIS(ret[0])

    @formatResponse
    def check_logical_name(self, ck_data):
        """
        检查 logical_name 的值

        :param ck_data:     期望值 (非16进制的各种形式的OBIS)
        :return:            KFResult 对象
        """
        ret = self.get_logical_name()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_logical_name(self, data):
        """
        设置 logical_name 的值

        :param data:        期望值 (非16进制的各种形式的OBIS)
        :return:            返回一个KFResult对象
        """
        return self.setRequest(1, obis_toHex(data), "OctetString", data)

    # Attribute of value (No.2)
    @formatResponse
    def get_value(self, dataType=False, response=None, obis=None):
        """
        获取 value 的值

        :param obis:        可以获取指定obis的值
        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个数值
        """
        obis = obis if obis is not None else self.obisList[0]

        if response is None:
            response = self.getRequestWithObis(2, obis)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
        if len(ret[0]) == 0:
            return ret
        try:
            if dataType:
                return hex_toDec(ret[0]), ret[1]
            return hex_toDec(ret[0])
        except ValueError:
            if dataType:
                return ret
            return ret[0]

    @formatResponse
    def check_value(self, ck_data):
        """
        检查 value 的值

        :param ck_data:     期望值 (数值）
        :return:            返回一个KFResult对象
        """
        ret = self.get_value()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_value(self, data):
        """
        设置 value 的值

        :param data:        期望值 (数值）
        :return:            返回一个KFResult对象
        """
        attributeType = getClassAttributeType(self.classId, self.obisList[0], Singleton().Project)
        if attributeType == "dlu":  # DoubleLongUnsigned
            return self.setRequest(2, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)
        elif attributeType == "lu":  # LongUnsigned
            return self.setRequest(2, dec_toHexStr(data, 4), "LongUnsigned", data)
        elif attributeType == "u":  # Unsigned
            return self.setRequest(2, dec_toHexStr(data, 2), "Unsigned", data)
        elif attributeType == "l":
            return self.setRequest(2, dec_toHexStr(data, 4), "Long", data)

        raise Exception("not specified attributeType")

    # Attribute of scaler_unit (No.3)
    @formatResponse
    def get_scaler_unit(self, dataType=False, response=None):
        """
        获取 scaler_unit 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个字典
        """
        if response is None:
            response = self.getRequest(3)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for key, value in response[0].items():
            for index, item in enumerate(value):
                value[index] = hex_toDec(item, response[1][key][index])
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_scaler_unit(self, ck_data):
        """
        检查 capture_objects 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0 : [0, 7]
        }
        """
        for value in ck_data.values():
            for index, item in enumerate(value):
                if item in [-1, -2, -3]:
                    value[index] = item + 256
        return checkResponsValue(self.get_scaler_unit(), ck_data)

    @formatResponse
    def set_scaler_unit(self, data):
        """
        设置 capture_objects 的值

        :param data:         接收一个字典参数
        :return              返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0 : [0, 7]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    # 负数处理
                    if subItem < 0:
                        subItem = 255 - abs(subItem) + 1
                        etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                    else:
                        etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(3, struct, "Struct", data)

    # Method of reset
    @formatResponse
    def act_reset(self, data=0):
        """
        Forces a reset of the object. By invoking this method, the value is set to the default value.
        The default value is an instance specific constant.

        :param data:                设置一个十进制数
        :return:                    返回一个 KFResult 对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)

    # ==================================================================================================#

    @formatResponse
    def get_value_with_list(self):
        """
        批量获取 class 3 的value值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            response[index] = self.get_value(obis=obis)
        return response

    @formatResponse
    def check_value_with_list(self, ck_data, initial=None):
        """
        批量检查 class 3 的value值 (先减去期望值, 再与预期值对比)

        :param ck_data:       期望值
        :param initial:       初始值
        :return:              KFResult 对象
        """
        response = list()
        result = self.get_value_with_list()

        if initial is None:
            initial = dict()
        try:
            for key, value in ck_data.items():
                # 如果increment字典中特定的Key没有对应的值, 则赋值为0
                if int(key) not in initial:
                    initial[key] = 0

                # ck_data 中包含范围时
                if isinstance(value, list):
                    if not int(value[0]) <= (int(result[key]) - int(initial[key])) <= int(value[-1]):
                        response.append(f"'response[{key}]={result[key]}' not in range of 'ck_data[{key}]={value}'")
                else:
                    if int(value) != int(result[key]) - int(initial[key]):
                        response.append(f"'response[{key}]={result[key]}' not equal to 'ck_data[{key}]={value}'")
            if len(response) == 0:
                return KFResult(True, '')
            else:
                return KFResult(False, "; ".join(response))

        except Exception as ex:
            error(ex)
