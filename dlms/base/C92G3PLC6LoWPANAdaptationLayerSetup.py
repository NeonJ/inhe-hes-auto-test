# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C92G3PLC6LoWPANAdaptationLayerSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "adp_max_hops",
        3: "adp_weak_lqi_value",
        4: "adp_security_level",
        5: "adp_prefix_table",
        6: "adp_routing_configuration",
        7: "adp_broadcast_log_table_entry_ttl",
        8: "adp_routing_table",
        9: "adp_context_information_table",
        10: "adp_blacklist_table",
        11: "adp_broadcast_log_table",
        12: "adp_group_table",
        13: "adp_max_join_wait_time",
        14: "adp_path_discovery_time",
        15: "adp_active_key_index",
        16: "adp_metric_type",
        17: "adp_coord_short_address",
        18: "adp_disable_default_routing",
        19: "adp_device_type",
        20: "adp_default_coord_route_enabled",
        21: "adp_destination_address_set"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=92)

    # Common get/set/check method for number type
    def __get_attr(self, attr_id, dataType=False, response=None):
        if response is None:
            response = self.getRequest(attr_id)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    def __check_attr(self, ck_data, attr_id):
        ret = self.__get_attr(attr_id)
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    def __set_attr(self, data, attr_id, attr_type):
        if attr_type == "Unsigned":
            return self.setRequest(attr_id, dec_toHexStr(data, 2), "Unsigned", data)
        elif attr_type == "LongUnsigned":
            return self.setRequest(attr_id, dec_toHexStr(data, 4), "LongUnsigned", data)
        elif attr_type == "DoubleLongUnsigned":
            return self.setRequest(attr_id, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)
        elif attr_type == "Bool":
            return self.setRequest(attr_id, dec_toHexStr(data, 2), "Bool", data)
        elif attr_type == "Enum":
            return self.setRequest(attr_id, dec_toHexStr(data, 2), "Enum", data)

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
        return self.setRequest(1, obis_toHex(data), "OctetString")

    # Attribute of adp_max_hops
    @formatResponse
    def get_adp_max_hops(self, dataType=False, response=None):
        """
        获取 adp_max_hops 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(2, dataType=dataType, response=response)

    @formatResponse
    def check_adp_max_hops(self, ck_data):
        """
        检查 adp_max_hops 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 2)

    @formatResponse
    def set_adp_max_hops(self, data):
        """
        设置 adp_max_hops 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 2, "Unsigned")

    # Attribute of adp_weak_LQI_value
    @formatResponse
    def get_adp_weak_lqi_value(self, dataType=False, response=None):
        """
        获取 adp_weak_LQI_value 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(3, dataType=dataType, response=response)

    @formatResponse
    def check_adp_weak_lqi_value(self, ck_data):
        """
        检查 adp_weak_LQI_value 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 3)

    @formatResponse
    def set_adp_weak_lqi_value(self, data):
        """
        设置 adp_weak_LQI_value 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 3, "Unsigned")

    # Attribute of adp_security_level
    @formatResponse
    def get_adp_security_level(self, dataType=False, response=None):
        """
        获取 adp_security_level 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(4, dataType=dataType, response=response)

    @formatResponse
    def check_adp_security_level(self, ck_data):
        """
        检查 adp_security_level 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 4)

    @formatResponse
    def set_adp_security_level(self, data):
        """
        设置 adp_security_level 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 4, "Unsigned")

    # Attribute of adp_prefix_table
    @formatResponse
    def get_adp_prefix_table(self, dataType=False, response=None):
        """
        获取 adp_prefix_table 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(5)

        response = getStrucDataFromGetResp(response)
        # for value in response.values():
        #     for index, item in enumerate(value):
        #         if index == 0:
        #             value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_adp_prefix_table(self, ck_data):
        """
        检查 adp_prefix_table 的值

        :param ck_data:   字典
        :return:          KFResult对象
        """
        return checkResponsValue(self.get_adp_prefix_table(), ck_data)

    @formatResponse
    def set_adp_prefix_table(self, data):
        """
        设置 adp_prefix_table 的值

        :param data:      字典
        :return:          KFResult对象
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        # for value in data.values():
        #     struct = etree.SubElement(array, "Structure")
        #     struct.set("Qty", dec_toHexStr(len(value), 4))
        #     for subIndex, subItem in enumerate(value):
        #         if subIndex == 0:
        #             etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        #         else:
        #             etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(5, array, "Array")

    # Attribute of adp_routing_configuration
    @formatResponse
    def get_adp_routing_configuration(self, dataType=False, response=None):
        """
        获取 adp_routing_configuration 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(6)

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
    def check_adp_routing_configuration(self, ck_data):
        """
        检查 adp_routing_configuration 的值

        :param ck_data:    字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [30, 1440, 0, 0, 0, 10, 4, 0, 0, 30, 10, 1, 0, 0]
        }
        """
        return checkResponsValue(self.get_adp_routing_configuration(), ck_data)

    @formatResponse
    def set_adp_routing_configuration(self, data):
        """
        设置 adp_routing_configuration 的值

        :param data:       字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [30, 1440, 0, 0, 0, 10, 4, 0, 0, 30, 10, 1, 0, 0]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex in [1, 10]:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                elif subIndex in [11, 12]:
                    etree.SubElement(struct, "Bool").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(6, array, "Array")

    # Attribute of adp_broadcast_log_table_entry_TTL
    @formatResponse
    def get_adp_broadcast_log_table_entry_ttl(self, dataType=False, response=None):
        """
        获取 adp_broadcast_log_table_entry_TTL 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(7, dataType=dataType, response=response)

    @formatResponse
    def check_adp_broadcast_log_table_entry_ttl(self, ck_data):
        """
        检查 adp_broadcast_log_table_entry_TTL 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 7)

    @formatResponse
    def set_adp_broadcast_log_table_entry_ttl(self, data):
        """
        设置 adp_broadcast_log_table_entry_TTL 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 7, "LongUnsigned")

    # Attribute of adp_routing_table
    @formatResponse
    def get_adp_routing_table(self, dataType=False, response=None):
        """
        获取 adp_routing_table 的值

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
                value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_adp_routing_table(self, ck_data):
        """
        检查 adp_routing_table 的值

        :param ck_data:    字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [30, 12, 0, 0, 0, 10]
        }
        """
        return checkResponsValue(self.get_adp_routing_table(), ck_data)

    @formatResponse
    def set_adp_routing_table(self, data):
        """
        设置 adp_routing_table 的值

        :param data:       字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [30, 12, 0, 0, 0, 10]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex in [3, 4]:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(8, array, "Array")

    # Attribute of adp_context_information_table
    @formatResponse
    def get_adp_context_information_table(self, dataType=False, response=None):
        """
        获取 adp_context_information_table 的值

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
                if index in [1, 3, 4]:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_adp_context_information_table(self, ck_data):
        """
        检查 adp_context_information_table 的值

        :param ck_data:    字典
        :return:           KFResult对象

        ck_data 数据格式：
        array context_information_table
        context_information_table ::= structure
        {
            CID: bit-string,
            context_length: unsigned,
            context: octet-string,
            C: boolean,
            valid_lifetime: long-unsigned
        }
        """
        return checkResponsValue(self.get_adp_context_information_table(), ck_data)

    @formatResponse
    def set_adp_context_information_table(self, data):
        """
        检查 adp_context_information_table 的值

        :param data:       字典
        :return:           KFResult对象

        data 数据格式：
        array context_information_table
        context_information_table ::= structure
        {
            CID: bit-string,
            context_length: unsigned,
            context: octet-string,
            C: boolean,
            valid_lifetime: long-unsigned
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "BitString").set("Value", subItem)
                elif subIndex == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
                elif subIndex == 2:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                elif subIndex == 3:
                    etree.SubElement(struct, "Bool,").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(9, array, "Array")

    # Attribute of adp_blacklist_table
    @formatResponse
    def get_adp_blacklist_table(self, dataType=False, response=None):
        """
        获取 adp_blacklist_table 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(10)

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
    def check_adp_blacklist_table(self, ck_data):
        """
        检查 adp_blacklist_table 的值

        :param ck_data:    字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [30, 12]
        }
        """
        checkResponsValue(self.get_adp_blacklist_table(), ck_data)

    @formatResponse
    def set_adp_blacklist_table(self, data):
        """
        设置 adp_blacklist_table 的值

        :param data:       字典
        :return:           KFResult对象

        data 数据格式：
        {
            0 : [30, 12]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(10, array, "Array")

    # Attribute of adp_broadcast_log_table
    @formatResponse
    def get_adp_broadcast_log_table(self, dataType=False, response=None):
        """
        获取 adp_broadcast_log_table 的值

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
                value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_adp_broadcast_log_table(self, ck_data):
        """
        检查 adp_broadcast_log_table 的值

        :param ck_data:    字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [0, 0, 0]
        }
        """
        return checkResponsValue(self.get_adp_broadcast_log_table(), ck_data)

    @formatResponse
    def set_adp_broadcast_log_table(self, data):
        """
        设置 adp_broadcast_log_table 的值

        :param data:       字典
        :return:           KFResult对象

        data 数据格式：
        {
            0 : [0, 0, 0]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex in [0, 2]:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(11, array, "Array")

    # Attribute of adp_group_table
    @formatResponse
    def get_adp_group_table(self, dataType=False, response=None):
        """
        获取 adp_group_table 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(12)

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
    def check_adp_group_table(self, ck_data):
        """
        检查 adp_group_table 的值

        :param ck_data:    字典
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0: 32769
        }
        """
        return checkResponsValue(self.get_adp_group_table(), ck_data)

    @formatResponse
    def set_adp_group_table(self, data):
        """
        设置 adp_group_table 的值

        :param data:       字典
        :return:           KFResult对象

        data 数据格式：
        {
            0: 32769
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            for index, item in enumerate(value):
                etree.SubElement(array, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
        return self.setRequest(12, array, "Array")

    # Attribute of adp_max_join_wait_time
    @formatResponse
    def get_adp_max_join_wait_time(self, dataType=False, response=None):
        """
        获取 adp_max_join_wait_time 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(13, dataType=dataType, response=response)

    @formatResponse
    def check_adp_max_join_wait_time(self, ck_data):
        """
        检查 adp_max_join_wait_time 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 13)

    @formatResponse
    def set_adp_max_join_wait_time(self, data):
        """
        设置 adp_max_join_wait_time 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 13, "LongUnsigned")

    # Attribute of adp_path_discovery_time
    @formatResponse
    def get_adp_path_discovery_time(self, dataType=False, response=None):
        """
        获取 adp_path_discovery_time 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(14, dataType=dataType, response=response)

    @formatResponse
    def check_adp_path_discovery_time(self, ck_data):
        """
        检查 adp_path_discovery_time 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 14)

    @formatResponse
    def set_adp_path_discovery_time(self, data):
        """
        设置 adp_path_discovery_time 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 14, "Unsigned")

    # Attribute of adp_active_key_index
    @formatResponse
    def get_adp_active_key_index(self, dataType=False, response=None):
        """
        获取 adp_active_key_index 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(15, dataType=dataType, response=response)

    @formatResponse
    def check_adp_active_key_index(self, ck_data):
        """
        检查 adp_active_key_index 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 15)

    @formatResponse
    def set_adp_active_key_index(self, data):
        """
        设置 adp_active_key_index 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 15, "Unsigned")

    # Attribute of adp_metric_type
    @formatResponse
    def get_adp_metric_type(self, dataType=False, response=None):
        """
        获取 adp_metric_type 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(16, dataType=dataType, response=response)

    @formatResponse
    def check_adp_metric_type(self, ck_data):
        """
        检查 adp_metric_type 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 16)

    @formatResponse
    def set_adp_metric_type(self, data):
        """
        设置 adp_metric_type 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 16, "Unsigned")

    # Attribute of adp_coord_short_address
    @formatResponse
    def get_adp_coord_short_address(self, dataType=False, response=None):
        """
        获取 adp_coord_short_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(17, dataType=dataType, response=response)

    @formatResponse
    def check_adp_coord_short_address(self, ck_data):
        """
        检查 adp_coord_short_address 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 17)

    @formatResponse
    def set_adp_coord_short_address(self, data):
        """
        设置 adp_coord_short_address 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 17, "LongUnsigned")

    # Attribute of adp_disable_default_routing
    @formatResponse
    def get_adp_disable_default_routing(self, dataType=False, response=None):
        """
        获取 adp_disable_default_routing 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(18, dataType=dataType, response=response)

    @formatResponse
    def check_adp_disable_default_routing(self, ck_data):
        """
        检查 adp_disable_default_routing 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 18)

    @formatResponse
    def set_adp_disable_default_routing(self, data):
        """
        设置 adp_disable_default_routing 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 18, "Bool")

    # Attribute of adp_device_type
    @formatResponse
    def get_adp_device_type(self, dataType=False, response=None):
        """
        获取 adp_device_type 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(19, dataType=dataType, response=response)

    @formatResponse
    def check_adp_device_type(self, ck_data):
        """
        检查 adp_device_type 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 19)

    @formatResponse
    def set_adp_device_type(self, data):
        """
        设置 adp_device_type 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 19, "Enum")

    # Attribute of adp_default_coord_route _enabled
    @formatResponse
    def get_adp_default_coord_route_enabled(self, dataType=False, response=None):
        """
        获取 adp_default_coord_route_enabled 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(20, dataType=dataType, response=response)

    @formatResponse
    def check_adp_device_type(self, ck_data):
        """
        检查 adp_device_type 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 20)

    @formatResponse
    def set_adp_device_type(self, data):
        """
        设置 adp_device_type 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 20, "Bool")

    # Attribute of adp_destination_address_set
    @formatResponse
    def get_adp_destination_address_set(self, dataType=False, response=None):
        """
        获取 adp_destination_address_set 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            数组
        """
        if response is None:
            response = self.getRequest(21)

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
    def check_adp_destination_address_set(self, ck_data):
        """
        检查 adp_destination_address_set 的值

        :param ck_data:    数组
        :return:           KFResult对象
        """
        return checkResponsValue(self.get_adp_group_table(), ck_data)

    @formatResponse
    def set_adp_destination_address_set(self, data):
        """
        设置 adp_destination_address_set 的值

        :param data:       数组
        :return:           KFResult对象
        """

        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            for index, item in enumerate(value):
                etree.SubElement(array, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
        return self.setRequest(21, array, "Array")
