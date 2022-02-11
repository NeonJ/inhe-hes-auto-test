# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C11SpecialDaysTable(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "entries"
    }

    action_index_dict = {
        1: "insert",
        2: "delete"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=11)

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

    # Attribute of entries (No.2)
    @formatResponse
    def get_entries(self, dataType=False, response=None):
        """
        获取 entries 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个字典
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
                if index == 1 and len(item) > 0:
                    value[index] = hex_toDateString(item)
                else:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_entries(self, ck_data):
        """
        检查 entries 的值

        :param ck_data:     期望值 (字典)
        :return:            KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [0, '2029-12-26-255', 18]
        }
        """

        return checkResponsValue(self.get_entries(), ck_data)

    @formatResponse
    def set_entries(self, data):
        """
        设置 entries 的值

        :param data:     期望值 (字典)
        :return:         KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [0, '2029-12-26-255', 18]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                elif subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", date_toHex(subItem))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(2, array, "Array", data)

    # Method of insert (No.1)
    @formatResponse
    def act_insert(self, data=None):
        """
        insert entry

        :param data:   期望值 (字典)
        :return:       KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [0, '2029-12-26-255', 18]
        }
        """

        if data is None:
            data = {}
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                elif subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", date_toHex(subItem))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.actionRequest(1, array, "Array", data)

    # Method of delete (No.2)
    @formatResponse
    def act_delete(self, data=0):
        """
        delete entry

        :param data:         十进制数（ex. 1）
        :return              KFResult对象
        """
        return self.actionRequest(2, dec_toHexStr(data, 4), "LongUnsigned", data)
