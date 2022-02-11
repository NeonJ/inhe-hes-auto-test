# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C29AutoConnect(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "mode",
        3: "repetitions",
        4: "repetition_delay",
        5: "calling_window",
        6: "destination_list"
    }

    action_index_dict = {
        1: "connect"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=29)

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

    # Attribute of mode
    @formatResponse
    def get_mode(self, dataType=False, response=None):
        """
        获取 mode 的值

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
    def check_mode(self, ck_data):
        """
        检查 mode 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_mode()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_mode(self, data):
        """
        设置 mode 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(2, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of repetitions
    @formatResponse
    def get_repetitions(self, dataType=False, response=None):
        """
        获取 repetitions 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(3)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_repetitions(self, ck_data):
        """
        检查 repetitions 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_repetitions()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_repetitions(self, data):
        """
        设置 repetitions 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of repetition_delay
    @formatResponse
    def get_repetition_delay(self, dataType=False, response=None):
        """
        获取 repetition_delay 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(4)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_repetition_delay(self, ck_data):
        """
        检查 repetition_delay 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_repetition_delay()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_repetition_delay(self, data):
        """
        设置 repetition_delay 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(4, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of calling_window
    @formatResponse
    def get_calling_window(self, dataType=False, response=None):
        """
        获取 calling_window 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:
        :return:            字典
        """
        if response is None:
            response = self.getRequest(5)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_calling_window(self, ck_data):
        """
        检查 calling_window 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            0: ['2019-05-1 14:24:45', '2019-05-1 14:34:45']
        }
        """
        return checkResponsValue(self.get_calling_window(), ck_data)

    @formatResponse
    def set_calling_window(self, data):
        """
        设置 calling_window 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            0: ['2019-05-1 14:24:45', '2019-05-1 14:34:45']
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(subItem))
        return self.setRequest(5, array, "Array", data)

    # Attribute of destination_list
    @formatResponse
    def get_destination_list(self, dataType=False, response=None):
        """
        获取 destination_list 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(6)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_destination_list(self, ck_data):
        """
        检查 destination_list 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
           0: ['2019-05-1 14:24:45']
        }
        """
        return checkResponsValue(self.get_destination_list(), ck_data)

    @formatResponse
    def set_destination_list(self, data):
        """
        设置 destination_list 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
           0: ['2019-05-1 14:24:45']
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(6, array, "Array", data)

    # Method of connect
    @formatResponse
    def act_connect(self, data=0):
        """
        Initiates the connection process to the communication network according to the
        rules defined via the mode attribute.

        :param data:  十进制数
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)
