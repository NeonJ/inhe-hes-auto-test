# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C27PSTNModemConfiguration(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "comm_speed",
        3: "initialization_string",
        4: "modem_profile"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=27)

    # Attribute of logical_name
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

    # Attribute of comm_speed
    @formatResponse
    def get_comm_speed(self, dataType=False, response=None):
        """
        获取 comm_speed 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_comm_speed(self, ck_data):
        """
        检查 comm_speed 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_comm_speed()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_comm_speed(self, data):
        """
        设置 comm_speed 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(2, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of initialization_string
    @formatResponse
    def get_initialization_string(self, dataType=False, response=None):
        """
        获取 initialization_string 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(3)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_initialization_string(self, ck_data):
        """
        检查 initialization_string 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象

        ck_data数据格式为：
        array initialization_string_element
        initialization_string_element ::= structure
        {
            request: octet-string,
            response: octet-string
        }
        """
        return checkResponsValue(self.get_initialization_string(), ck_data)

    @formatResponse
    def set_initialization_string(self, data):
        """
        设置 initialization_string 的值

        :param data:        十进制数
        :return:            KFResult 对象

        data数据格式为：
        array initialization_string_element
        initialization_string_element ::= structure
        {
            request: octet-string,
            response: octet-string
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(3, array, "Array", data)

    # Attribute of modem_profile
    @formatResponse
    def get_modem_profile(self, dataType=False, response=None):
        """
        获取 modem_profile 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:
        :return:            字典
        """
        if response is None:
            response = self.getRequest(4)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_modem_profile(self, ck_data):
        """
        检查 modem_profile 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象

        ck_data数据格式为：
        array modem_profile_element
        modem_profile_element: octet-string
        """
        return checkResponsValue(self.get_modem_profile(), ck_data)

    @formatResponse
    def set_modem_profile(self, data):
        """
        设置 modem_profile 的值

        :param data:        十进制数
        :return:            KFResult 对象

        data数据格式为：
        array modem_profile_element
        modem_profile_element: octet-string
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            for subIndex, subItem in enumerate(value):
                etree.SubElement(array, "OctetString").set("Value", subItem)
        return self.setRequest(5, array, "Array", data)
