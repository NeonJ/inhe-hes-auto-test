# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C60MessageHandler(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "listening_window",
        3: "list_of_allowed_senders",
        4: "list_of_senders_and_actions",
    }

    action_index_dict = {
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=60)

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

        :param ck_data:         点分十进制形式的OBIS值
        :return:                KFResult对象
        """
        ret = self.get_logical_name()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_logical_name(self, data):
        """
        设置 logical_name 的值

        :param data:         点分十进制形式的OBIS值
        :return:             KFResult对象
        """
        return self.setRequest(1, obis_toHex(data), "OctetString", data)

    # Attribute of listening_window
    @formatResponse
    def get_listening_window(self, dataType=False, response=None):
        """
        获取 listening_window 的值

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
                value[index] = hex_toDateTimeString(item)

        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_listening_window(self, ck_data):
        """
        检查 listening_window 的值

        :param ck_data:         字典
        :return:                KFResult对象
        """
        return checkResponsValue(self.get_listening_window(), ck_data)

    @formatResponse
    def set_listening_window(self, data):
        """
        设置 listening_window 的值

        :param data:         字典
        :return:             KFResult对象
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            for item in value:
                etree.SubElement(array, "OctetString").set("Value", dateTime_toHex(item))
        return self.setRequest(2, array, "Array", data)

    # Attribute of list_of_allowed_senders
    @formatResponse
    def get_list_of_allowed_senders(self, dataType=False, response=None):
        """
        获取 listening_window 的值

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

        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_list_of_allowed_senders(self, ck_data):
        """
        检查 listening_window 的值

        :param ck_data:         字典
        :return:                KFResult对象
        """
        return checkResponsValue(self.get_list_of_allowed_senders(), ck_data)

    @formatResponse
    def set_list_of_allowed_senders(self, data):
        """
        设置 listening_window 的值

        :param data:         字典
        :return:             KFResult对象
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            for item in value:
                etree.SubElement(array, "OctetString").set("Value", item)
        return self.setRequest(3, array, "Array", data)

    # Attribute of list_of_senders_and_actions
    @formatResponse
    def get_list_of_senders_and_actions(self, dataType=False, response=None):
        """
        获取 listening_window 的值

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
            for index, item in enumerate(value):
                if isinstance(item, list):
                    for subIndex, subItem in enumerate(item):
                        if subIndex == 0:
                            item[subIndex] = hex_toOBIS(subItem)
                        else:
                            item[subIndex] = hex_toDec(subItem)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_list_of_senders_and_actions(self, ck_data):
        """
        检查 listening_window 的值

        :param ck_data:         字典
        :return:                KFResult对象
        """
        return checkResponsValue(self.get_list_of_senders_and_actions(), ck_data)

    @formatResponse
    def set_list_of_senders_and_actions(self, data):
        """
        设置 listening_window 的值

        :param data:         字典
        :return:             KFResult对象
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for item in value:
                if isinstance(item, list):
                    subStruct = etree.SubElement(struct, "Structure")
                    subStruct.set("Qty", dec_toHexStr(len(item), 4))
                    for subIndex, subItem in enumerate(item):
                        if subIndex == 0:
                            etree.SubElement(subStruct, "OctetString").set("Value", obis_toHex(subItem))
                        else:
                            etree.SubElement(subStruct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", item)
        return self.setRequest(4, array, "Array", data)
