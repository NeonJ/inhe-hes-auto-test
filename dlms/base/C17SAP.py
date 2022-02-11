# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C17SAP(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "sap_assignment_list"
    }

    action_index_dict = {
        1: "connect_logical_device"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=17)

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

    # Attribute of SAP_assignment_list
    @formatResponse
    def get_sap_assignment_list(self, dataType=False, response=None):
        """
        获取 SAP_assignment_list 的值

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
                if index == 0 and len(item) > 0:
                    value[index] = int(item)
                if index == 1 and len(item) > 0:
                    value[index] = hex_toAscii(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_sap_assignment_list(self, ck_data):
        """
        检查 object_list 的值

        :param ck_data:     期望值 (字典)
        :return:            KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [1, "KFM1100100000110"]
        }
        """
        return checkResponsValue(self.get_sap_assignment_list(), ck_data)

    @formatResponse
    def set_sap_assignment_list(self, data):
        """
        设置 object_list 的值

        :param data:        期望值 (字典)
        :return:            KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [1, "KFM1100100000110"]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 2))
        for index in range(len(data)):
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(data[index]), 2))
            for subIndex, subItem in enumerate(data[index]):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                if subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", ascii_toHex(subItem))
        return self.setRequest(2, array, "Array", data)

    # Method of connect_logical_device
    @formatResponse
    def act_connect_logical_device(self, data=None):
        """
        Connects a logical device to a SAP. Connecting to SAP 0 will disconnect the device.
        More than one device cannot be connected to one SAP (exception SAP 0).

        :param data: 接收一个字典参数
        {
            0: [1, "KFM1100100000110"]
        }
        """
        # No response after set the data as structure according to blue book
        if data is None:
            data = {}
        struct = etree.Element("Structure")
        if len(data) == 0:
            struct.set("Qty", dec_toHexStr(0, 4))
        else:
            for value in data.values():
                struct.set("Qty", dec_toHexStr(len(value), 4))
                for subIndex, subItem in enumerate(value):
                    if subIndex == 0:
                        etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                    if subIndex == 1:
                        etree.SubElement(struct, "OctetString").set("Value", ascii_toHex(subItem))
        return self.actionRequest(1, struct, "Structure", data)
