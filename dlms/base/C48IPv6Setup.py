# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C48IPv6Setup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "dl_reference",
        3: "address_config_mode",
        4: "unicast_ipv6_addresses",
        5: "multicast_ipv6_addresses",
        6: "gateway_ipv6_addresses",
        7: "primary_dns_address",
        8: "secondary_dns_address",
        9: "traffic_class",
        10: "neighbor_discovery_setup"
    }

    action_index_dict = {
        1: "add_ipv6_address",
        2: "remove_ipv6_address"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=48)

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

    # Attribute of DL_reference
    @formatResponse
    def get_dl_reference(self, dataType=False, response=None):
        """
        获取 DL_reference 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            点分十进制形式的OBIS值
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toOBIS(ret[0]), ret[1]
        return hex_toOBIS(ret[0])

    @formatResponse
    def check_dl_reference(self, ck_data):
        """
        检查 DL_reference 的值

        :param ck_data:         点分十进制形式的OBIS值
        :return:                KFResult对象
        """
        ret = self.get_dl_reference()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_dl_reference(self, data):
        """
        设置 DL_reference 的值

        :param data:         点分十进制形式的OBIS值
        :return:             KFResult对象
        """
        return self.setRequest(2, obis_toHex(data), "OctetString", data)

    # Attribute of address_config_mode
    @formatResponse
    def get_address_config_mode(self, dataType=False, response=None):
        """
        获取 address_config_mode 的值

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
    def check_address_config_mode(self, ck_data):
        """
        检查 address_config_mode 的值

        :param ck_data:         十进制数
        :return:                KFResult对象
        """
        ret = self.get_address_config_mode()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_address_config_mode(self, data):
        """
        设置 address_config_mode 的值

        :param data:         十进制数
        :return:             KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of unicast_IPv6_addresses
    @formatResponse
    def get_unicast_ipv6_addresses(self, dataType=False, response=None):
        """
        获取 unicast_IPv6_addresses 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(4)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_unicast_ipv6_addresses(self, ck_data):
        """
        检查 unicast_IPv6_addresses 的值

        :param ck_data:     字典
        :return:            KFResult对象

        unicast_IPv6_addresses ::= array octet-string
        """
        return checkResponsValue(self.get_unicast_ipv6_addresses(), ck_data)

    @formatResponse
    def set_unicast_ipv6_addresses(self, data):
        """
        设置 unicast_ipv6_addresses 的值

        :param data:        字典
        :return：           KFResult对象

        unicast_IPv6_addresses ::= array octet-string
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            for item in value:
                etree.SubElement(array, "OctetString").set("Value", item)
        return self.setRequest(4, array, "Array", data)

    # Attribute of multicast_IPv6_addresses
    @formatResponse
    def get_multicast_ipv6_addresses(self, dataType=False, response=None):
        """
        获取 multicast_IPv6_addresses 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(5)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_multicast_ipv6_addresses(self, ck_data):
        """
        检查 multicast_IPv6_addresses 的值

        :param ck_data:     字典
        :return:            KFResult对象

        multicast_IPv6_addresses ::= array octet-string
        """
        return checkResponsValue(self.get_multicast_ipv6_addresses(), ck_data)

    @formatResponse
    def set_multicast_ipv6_addresses(self, data):
        """
        设置 multicast_IPv6_addresses 的值

        :param data:        字典
        :return:            KFResult对象

        multicast_IPv6_addresses ::= array octet-string
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            for item in value:
                etree.SubElement(array, "OctetString").set("Value", item)
        return self.setRequest(5, array, "Array", data)

    # Attribute of gateway_IPv6_addresses
    @formatResponse
    def get_gateway_ipv6_addresses(self, dataType=False, response=None):
        """
        获取 gateway_IPv6_addresses 的值

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
    def check_gateway_ipv6_addresses(self, ck_data):
        """
        检查 gateway_IPv6_addresses 的值

        :param ck_data:     字典
        :return:            KFResult对象

        gateway_IPv6_addresses ::= array octet-string
        """
        return checkResponsValue(self.get_gateway_ipv6_addresses(), ck_data)

    @formatResponse
    def set_gateway_ipv6_addresses(self, data):
        """
        设置 gateway_IPv6_addresses 的值

        :param data:        字典
        :return:            KFResult对象

        gateway_IPv6_addresses ::= array octet-string
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            etree.SubElement(array, "OctetString").set("Value", value)
        return self.setRequest(6, array, "Array", data)

    # Attribute of primary_DNS_address
    @formatResponse
    def get_primary_dns_address(self, dataType=False, response=None):
        """
        获取 primary_DNS_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(7)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_primary_dns_address(self, ck_data):
        """
        检查 primary_DNS_address 的值

        :param ck_data:    字符串
        :return:           KFResult对象
        """
        ret = self.get_primary_dns_address()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_primary_dns_address(self, data):
        """
        设置 primary_DNS_address 的值

        :param data:       字符串
        :return:           KFResult对象
        """
        return self.setRequest(7, data, "OctetString", data)

    # Attribute of secondary_DNS_address
    @formatResponse
    def get_secondary_dns_address(self, dataType=False, response=None):
        """
        获取 secondary_DNS_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(8)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_secondary_dns_address(self, ck_data):
        """
        检查 secondary_DNS_address 的值

        :param ck_data:    字符串
        :return:           KFResult对象
        """
        ret = self.get_secondary_dns_address()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_secondary_dns_address(self, data):
        """
        设置 secondary_DNS_address 的值

        :param data:       字符串
        :return:           KFResult对象
        """
        return self.setRequest(8, data, "OctetString", data)

    # Attribute of traffic_class
    @formatResponse
    def get_traffic_class(self, dataType=False, response=None):
        """
        获取 traffic_class 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(9)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_traffic_class(self, ck_data):
        """
        检查 traffic_class 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_traffic_class()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_traffic_class(self, data):
        """
        设置 traffic_class 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(9, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of neighbor_discovery_setup
    @formatResponse
    def get_neighbor_discovery_setup(self, dataType=False, response=None):
        """
        获取 neighbor_discovery_setup 的值

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
    def check_neighbor_discovery_setup(self, ck_data):
        """
        检查 neighbor_discovery_setup 的值

        :param ck_data:         字典
        :return:                KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [3, 10000, 5]
        }
        """
        return checkResponsValue(self.get_neighbor_discovery_setup(), ck_data)

    @formatResponse
    def set_neighbor_discovery_setup(self, data):
        """
        设置 neighbor_discovery_setup 的值

        :param data:            字典
        :return:                KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [3, 10000, 5]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                elif index == 1:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                else:
                    etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(item, 8))
        return self.setRequest(10, array, "Array", data)

    # Method of add_IPv6_address
    @formatResponse
    def act_add_ipv6_address(self, data=None):
        """
        Adds one IPv6 address for the physical interface to the IPv6 address array.

        :param data:            字典

        data ::= structure
        {
            IPv6_address_type: enum,
            IPv6_address: octet_string
        }
        """
        if data is None:
            data = {}
        struct = etree.Element("Structure")
        if len(data) == 0:
            struct.set("Qty", dec_toHexStr(0, 4))

        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(item, 2))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", )
        return self.actionRequest(1, struct, "Structure", data)

    @formatResponse
    def act_remove_ipv6_address(self, data):
        """
        Removes one IPv6 address for the physical interface to the IPv6 address

        :param data:    字典

        data ::= structure
        {
            IPv6_address_type: enum,
            IPv6_address: octet-string
        }
        """
        struct = etree.Element("Structure")
        if len(data) == 0:
            struct.set("Qty", dec_toHexStr(0, 4))

        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(item, 2))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", item)
        return self.actionRequest(2, struct, "Structure", data)
