# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C71Limiter(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "monitored_value",
        3: "threshold_active",
        4: "threshold_normal",
        5: "threshold_emergency",
        6: "min_over_threshold_duration",
        7: "min_under_threshold_duration",
        8: "emergency_profile",
        9: "emergency_profile_group_id_list",
        10: "emergency_profile_active",
        11: "actions"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=71)

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

    # Attribute of monitored_value
    @formatResponse
    def get_monitored_value(self, dataType=False, response=None):
        """
        获取 monitored_value 的值

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
                if index == 0:
                    value[index] = hex_toDec(item)
                elif index == 1:
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

        :param ck_data:      字典
        :return:             KFResult对象

        ck_data格式：
        {
            0: [1, '0-0:97.98.21.255', 2]
        }
        """
        return checkResponsValue(self.get_monitored_value(), ck_data)

    @formatResponse
    def set_monitored_value(self, data):
        """
        设置 monitored_value 的值

        :param data:         字典
        :return:             KFResult对象

        data格式：
        {
            0: [1, '0-0:97.98.21.255', 2]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                elif subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
                else:
                    etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(2, struct, "Struct", data)

    # Attribute of threshold_active
    @formatResponse
    def get_threshold_active(self, dataType=False, response=None):
        """
        获取 threshold_active 的值

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
    def check_threshold_active(self, ck_data):
        """
        检查 threshold_active 的值

        :param ck_data:          十进制数
        :return:                 KFResult对象
        """
        ret = self.get_threshold_active()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_threshold_active(self, data):
        """
        设置 threshold_active 的值

        :param data:         十进制数
        :return:             KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of threshold_normal
    @formatResponse
    def get_threshold_normal(self, dataType=False, response=None):
        """
        获取 threshold_normal 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
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
    def check_threshold_normal(self, ck_data):
        """
        检查 threshold_normal 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        ret = self.get_threshold_normal()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_threshold_normal(self, data):
        """
        设置 threshold_normal 的值

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.setRequest(4, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of threshold_emergency
    @formatResponse
    def get_threshold_emergency(self, dataType=False, response=None):
        """
        获取 threshold_emergency 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(5)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_threshold_emergency(self, ck_data):
        """
        检查 threshold_emergency 的值

        :param ck_data:          十进制数
        :return:                 KFResult对象
        """
        ret = self.get_threshold_emergency()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_threshold_emergency(self, data):
        """
        设置 threshold_emergency 的值

        :param data:             十进制数
        :return:                 KFResult对象
        """
        return self.setRequest(5, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of min_over_threshold_duration
    @formatResponse
    def get_min_over_threshold_duration(self, dataType=False, response=None):
        """
        获取 min_over_threshold_duration 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(6)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_min_over_threshold_duration(self, ck_data):
        """
        检查 min_over_threshold_duration 的值

        :param ck_data:         十进制数
        :return:                KFResult对象
        """
        ret = self.get_min_over_threshold_duration()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_min_over_threshold_duration(self, data):
        """
        设置 min_over_threshold_duration 的值

        :param data:          十进制数
        :return:              KFResult对象
        """
        return self.setRequest(6, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of min_under_threshold_duration
    @formatResponse
    def get_min_under_threshold_duration(self, dataType=False, response=None):
        """
        获取 min_under_threshold_duration 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(7)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_min_under_threshold_duration(self, ck_data):
        """
        检查 min_under_threshold_duration 的值

        :param ck_data:         十进制数
        :return:                KFResult对象
        """
        ret = self.get_min_under_threshold_duration()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_min_under_threshold_duration(self, data):
        """
        设置 min_under_threshold_duration 的值

        :param data:           十进制数
        :return:               KFResult对象
        """
        return self.setRequest(7, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of emergency_profile
    @formatResponse
    def get_emergency_profile(self, dataType=False, response=None):
        """
        获取 emergency_profile 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(8)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                if index == 0:
                    value[index] = hex_toDec(item)
                elif index == 1:
                    if item != "FFFFFFFFFFFFFFFFFFFFFFFF":
                        value[index] = hex_toDateTimeString(item)
                else:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_emergency_profile(self, ck_data):
        """
        检查 emergency_profile 的值

        :param ck_data:          字典
        :return:                 KFResult对象

        ck_data格式：
        {
            0: [0, '65535-255-255 255:255:255 0xFF,0xFFFF,0xFF', 3600]
        }
        """
        return checkResponsValue(self.get_emergency_profile(), ck_data)

    @formatResponse
    def set_emergency_profile(self, data):
        """
        设置 emergency_profile 的值

        :param data:             字典
        :return:                 KFResult对象

        data：
        {
            0: [0, '65535-255-255 255:255:255 0xFF,0xFFFF,0xFF', 3600]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                elif subIndex == 1:
                    if subItem == "FFFFFFFFFFFFFFFFFFFFFFFF":
                        etree.SubElement(struct, "OctetString").set("Value", subItem)
                    else:
                        etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(subItem))
                else:
                    etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(subItem, 8))
        return self.setRequest(8, struct, "Struct", data)

    # Attribute of emergency_profile_group_id_list
    @formatResponse
    def get_emergency_profile_group_id_list(self, dataType=False, response=None):
        """
        获取 emergency_profile_group_id_list 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(9)

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
    def check_emergency_profile_group_id_list(self, ck_data):
        """
        检查 emergency_profile_group_id_list 的值

        :param ck_data:         字典
        :return:                KFResult对象

        ck_data 数据格式
        {
            0: 3,
            1: 4
        }
        """
        ret = self.get_emergency_profile_group_id_list()
        if sorted(ck_data.values()) == sorted(ret.values()):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_emergency_profile_group_id_list(self, data):
        """
        设置 emergency_profile_group_id_list 的值

        :param data:            字典
        :return:                KFResult对象

        data 数据格式
        {
            0: 3,
            1: 4
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            for index, item in enumerate(value):
                etree.SubElement(array, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
        return self.setRequest(9, array, "Struct", data)

    # Attribute of emergency_profile_active
    @formatResponse
    def get_emergency_profile_active(self, dataType=False, response=None):
        """
        获取 emergency_profile_active 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(10)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_emergency_profile_active(self, ck_data):
        """
        检查 emergency_profile_active 的值

        :param ck_data:     十进制数
        :return:            KFResult值
        """
        ret = self.get_emergency_profile_active()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_emergency_profile_active(self, data):
        """
        设置 emergency_profile_active 的值

        :param data:  十进制数
        :return:      KFResult对象
        """
        return self.setRequest(10, dec_toHexStr(data, 2), "Bool", data)

    # Attribute of actions
    @formatResponse
    def get_actions(self, dataType=False, response=None):
        """
        获取 actions 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(11)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                if index == 0:
                    value[index] = hex_toOBIS(item)
                elif index == 1:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_actions(self, ck_data):
        """
        检查 actions 的值

        :param ck_data:  字典
        :return:         KFResult对象

        ck_data格式:
        {
            0: ['0-0:10.0.106.255', 1],
            1: ['0-0:10.0.106.255', 0]
        }
        """
        return checkResponsValue(self.get_actions(), ck_data)

    @formatResponse
    def set_actions(self, data):
        """
        设置 actions 的值

        :param data:     字典
        :return:         KFResult对象

        ck_data格式:
        {
            0: ['0-0:10.0.106.255', 1],
            1: ['0-0:10.0.106.255', 0]
        }
        """
        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            sub_struct = etree.SubElement(struct, "Structure")
            sub_struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(sub_struct, "OctetString").set("Value", obis_toHex(subItem))
                elif subIndex == 1:
                    etree.SubElement(sub_struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(11, struct, "Struct", data)
