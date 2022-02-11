# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C28AutoAnswer(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "mode",
        3: "listening_window",
        4: "status",
        5: "number_of_calls",
        6: "number_of_rings",
        7: "list_of_allowed_callers",
        8: "list_of_callers_and_actions",
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=28)

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
            response = self.getRequest(3)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_listening_window(self, ck_data):
        """
        检查 listening_window 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象

        ck_data数据格式为：
        array window_element
        window_element ::= structure
        {
            start _time: octet-string,
            end_time: octet-string
        }
        """
        return checkResponsValue(self.get_listening_window(), ck_data)

    @formatResponse
    def set_listening_window(self, data):
        """
        设置 listening_window 的值

        :param data:        十进制数
        :return:            KFResult 对象

        data数据格式为：
            array window_element
            window_element ::= structure
            {
                start _time: octet-string,
                end_time: octet-string
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

    # Attribute of status
    @formatResponse
    def get_status(self, dataType=False, response=None):
        """
        获取 status 的值

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
    def check_status(self, ck_data):
        """
        检查 status 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_status()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_status(self, data):
        """
        设置 status 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(4, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of number_of_calls
    @formatResponse
    def get_number_of_calls(self, dataType=False, response=None):
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
    def check_number_of_calls(self, ck_data):
        """
        检查 number_of_calls 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        """
        ret = self.get_number_of_calls()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_number_of_calls(self, data):
        """
        设置 number_of_calls 的值

        :param data:        字典
        :return:            KFResult 对象
        """
        return self.setRequest(5, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of number_of_rings
    @formatResponse
    def get_number_of_rings(self, dataType=False, response=None):
        """
        获取 number_of_rings 的值

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
    def check_number_of_calls(self, ck_data):
        """
        检查 number_of_calls 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        """
        ret = self.get_number_of_calls()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_number_of_calls(self, data):
        """
        设置 number_of_calls 的值

        :param data:        字典
        :return:            KFResult 对象
        """
        return self.setRequest(5, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of number_of_rings
    @formatResponse
    def get_number_of_rings(self, dataType=False, response=None):
        """
        获取 number_of_rings 的值

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
    def check_number_of_rings(self, ck_data):
        """
        检查 number_of_rings 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        nr_rings_type ::= structure
        {
            nr_rings_in_window: unsigned, (0: no connect in window)
            nr_rings_out_of_window: unsigned (0: no connect out of window)
        }
        """
        return checkResponsValue(self.get_number_of_rings(), ck_data)

    @formatResponse
    def set_number_of_rings(self, data):
        """
        设置 number_of_rings 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        nr_rings_type ::= structure
        {
            nr_rings_in_window: unsigned, (0: no connect in window)
            nr_rings_out_of_window: unsigned (0: no connect out of window)
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem))
        return self.setRequest(6, struct, "struct", data)

    # Attribute of list_of_allowed_callers
    @formatResponse
    def get_list_of_allowed_callers(self, dataType=False, response=None):
        """
        获取 list_of_allowed_callers 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(7)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_list_of_allowed_callers(self, ck_data):
        """
        检查 list_of_allowed_callers 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        list_of_allowed_callers ::= array list_of_allowed_callers_element
        list_of_allowed_callers_element ::= structure
        {
        caller_id: octet-string,
        call_type: enum
        }
        """
        return checkResponsValue(self.get_list_of_allowed_callers(), ck_data)

    @formatResponse
    def set_list_of_allowed_callers(self, data):
        """
        设置 list_of_allowed_callers 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        list_of_allowed_callers ::= array list_of_allowed_callers_element
        list_of_allowed_callers_element ::= structure
        {
        caller_id: octet-string,
        call_type: enum
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                else:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(7, array, "Array", data)

    # Attribute of list_of_callers_and_actions
    @formatResponse
    def get_list_of_callers_and_actions(self, dataType=False, response=None):
        """
        获取 list_of_allowed_callers 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(8)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_list_of_callers_and_actions(self, ck_data):
        """
        检查 list_of_allowed_callers 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        list_of_allowed_callers ::= array list_of_allowed_callers_element
        list_of_allowed_callers_element ::= structure
        {
        caller_id: octet-string,
        call_type: enum
        }
        """
        return checkResponsValue(self.get_list_of_callers_and_actions(), ck_data)

    @formatResponse
    def set_list_of_callers_and_actions(self, data):
        """
        设置 list_of_allowed_callers 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        list_of_allowed_callers ::= array list_of_allowed_callers_element
        list_of_allowed_callers_element ::= structure
        {
        caller_id: octet-string,
        call_type: enum
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                else:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(8, array, "Array", data)
