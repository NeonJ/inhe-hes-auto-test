# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C21RegisterMonitor(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "thresholds",
        3: "monitored_value",
        4: "actions"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=21)

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

    # Attribute of thresholds (No.2)
    @formatResponse
    def get_thresholds(self, dataType=False, response=None):
        """
        获取 thresholds 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(2)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_thresholds(self, ck_data):
        """
        检查 thresholds 的值

        :param ck_data:     字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: 0,
        }
        """
        return checkResponsValue(self.get_thresholds(), ck_data)

    @formatResponse
    def set_thresholds(self, data):
        """
        设置 thresholds 的值

        :param data:        字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: 0,
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            for index, item in enumerate(value):
                etree.SubElement(array, "DoubleLongUnsigned").set("Value", dec_toHexStr(item, 8))
        return self.setRequest(2, array, "Array", data)

    # Attribute of monitored_value (No.3)
    @formatResponse
    def get_monitored_value(self, dataType=False, response=None):
        """
        获取 monitored_value 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(3)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                if index == 1 and len(item) > 0:
                    value[index] = hex_toOBIS(item)
                else:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_monitored_value(self, ck_data):
        """
        检查 monitored_value 的值

        :param ck_data:     字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: [0, '', 8]
        }
        """
        return checkResponsValue(self.get_monitored_value(), ck_data)

    @formatResponse
    def set_monitored_value(self, data):
        """
        设置 monitored_value 的值

        :param data:        字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: [0, '', 8]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                if subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
                if subIndex == 2:
                    etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(3, struct, "Struct", data)

    # Attribute of actions (No.4)
    @formatResponse
    def get_actions(self, dataType=False, response=None):
        """
        获取 actions 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(4)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for item in value:
                for index, sub_item in enumerate(item):
                    if index == 0 and len(sub_item) > 0:
                        item[index] = hex_toOBIS(sub_item)
                    else:
                        item[index] = hex_toDec(sub_item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_actions(self, ck_data):
        """
        检查 actions 的值

        :param ck_data:     字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: [['0-0:10.0.108.255', 4], ['0-0:10.0.108.255', 0]]
        }
        """
        return checkResponsValue(self.get_actions(), ck_data)

    @formatResponse
    def set_actions(self, data):
        """
        设置 actions 的值

        :param data:        字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: [['0-0:10.0.108.255', 4], ['0-0:10.0.108.255', 0]]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for sub_value in value:
                sub_struct = etree.SubElement(struct, "Structure")
                sub_struct.set("Qty", dec_toHexStr(len(sub_value), 4))
                for subIndex, subItem in enumerate(sub_value):
                    if subIndex == 0:
                        etree.SubElement(sub_struct, "OctetString").set("Value", obis_toHex(subItem))
                    if subIndex == 1:
                        etree.SubElement(sub_struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(4, array, "Array", data)
