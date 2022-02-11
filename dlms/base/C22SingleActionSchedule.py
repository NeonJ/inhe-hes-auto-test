# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C22SingleActionSchedule(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "executed_script",
        3: "type",
        4: "execution_time"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=22)

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

    # Attribute of executed_script (No.2)
    @formatResponse
    def get_executed_script(self, dataType=False, response=None):
        """
        获取 executed_script 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(2)

        response = getStrucDataFromGetResp(response)
        if isinstance(response[0], dict):
            for value in response[0].values():
                for index, item in enumerate(value):
                    if index == 0 and len(item) > 0:
                        value[index] = hex_toOBIS(item)
                    if index == 1 and len(item) > 0:
                        value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_executed_script(self, ck_data):
        """
        检查 executed_script 的值

        :param ck_data:     字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: ["0-0:10.0.109.255", 1]
        }
        """
        return checkResponsValue(self.get_executed_script(), ck_data)

    @formatResponse
    def set_executed_script(self, data):
        """
        设置 executed_script 的值

        :param data:        字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            0: ["0-0:10.0.109.255", 1]
        }
        """
        if data is None or len(data) == 0:
            struct = etree.Element("Structure")
            struct.set("Qty", "0000")
            return self.setRequest(2, struct, "struct")

        struct = etree.Element("Structure")
        struct.set("Qty", "0002")
        etree.SubElement(struct, "OctetString").set("Value", obis_toHex(data[0][0]))
        etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(data[0][1], 4))
        return self.setRequest(2, struct, "struct", data)

    # Attribute of type (No.3)
    @formatResponse
    def get_type(self, dataType=False, response=None):
        """
        获取 type 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            Enum
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
    def check_type(self, ck_data):
        """
        检查 type 的值

        :param ck_data:     Enum
        :return:            返回一个KFResult对象
        """
        ret = self.get_type()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_type(self, data):
        """
        设置 type 的值

        :param data:        Enum
        :return:            返回一个KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of execution_time (No.4)
    @formatResponse
    def get_execution_time(self, dataType=False, response=None):
        """
        获取 execution_time 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(4)

        response = getStrucDataFromGetResp(response)
        if isinstance(response[0], dict):
            for value in response[0].values():
                for index, item in enumerate(value):
                    if index == 0 and len(item) > 0:
                        value[index] = hex_toTimeString(item)
                    if index == 1 and len(item) > 0:
                        value[index] = hex_toDateString(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_execution_time(self, ck_data):
        """
        检查 execution_time 的值

        :param ck_data:     字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            time: octet-string,
            date: octet-string
        }
        """
        # 处理{0: ['00000000', 'FFFFFF01FF']}格式数据
        for value in ck_data.values():
            for index, item in enumerate(value):
                if index == 0 and str(item).find(":") == -1:
                    value[index] = hex_toTimeString(item)
                if index == 1 and str(item).find("-") == -1:
                    value[index] = hex_toDateString(item)
        return checkResponsValue(self.get_execution_time(), ck_data)

    @formatResponse
    def set_execution_time(self, data, isDownloadMode=True):
        """
        设置 execution_time 的值

        :param data:        字典
        :return:            返回一个KFResult对象

        ck_data 的数据格式为:
        {
            time: octet-string,
            date: octet-string
        }
        """
        if data is None or len(data) == 0:
            array = etree.Element("Array")
            array.set("Qty", "0000")
            return self.setRequest(4, array, "array")

        for value in data.values():
            for index, item in enumerate(value):
                if index == 0 and str(item).find(":") == -1:
                    value[index] = hex_toTimeString(item)
                if index == 1 and str(item).find("-") == -1:
                    value[index] = hex_toDateString(item)
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "OctetString").set("Value", time_toHex(item))
                if index == 1:
                    etree.SubElement(struct, "OctetString").set("Value", date_toHex(item))
        return self.setRequest(4, array, "Array", data)
