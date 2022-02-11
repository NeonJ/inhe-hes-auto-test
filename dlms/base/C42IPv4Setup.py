# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C42IPv4Setup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "dl_reference",
        3: "ip_address",
        4: "multicast_ip_address",
        5: "ip_options",
        6: "subnet_mask",
        7: "gateway_ip_address",
        8: "use_dhcp_flag",
        9: "primary_dns_address",
        10: "secondary_dns_address"
    }

    action_index_dict = {
        1: "add_mc_ip_address",
        2: "delete_mc_ip_address",
        3: "get_nbof_mc_ip_addresses"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=42)

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

        :param ck_data:       点分十进制形式的OBIS值
        :return:              KFResult 对象
        """
        ret = self.get_dl_reference()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_dl_reference(self, data):
        """
        设置 DL_reference 的值

        :param data:          点分十进制形式的OBIS值
        :return:              KFResult 对象
        """
        return self.setRequest(2, obis_toHex(data), "OctetString", data)

    # Attribute of IP_address
    @formatResponse
    def get_ip_address(self, dataType=False, response=None, attr=3):
        """
        获取 IP_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            ipv4 地址
        """
        if response is None:
            response = self.getRequest(attr)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toIPv4(ret[0]), ret[1]
        return hex_toIPv4(ret[0])

    @formatResponse
    def check_ip_address(self, ck_data, attr=3):
        """
        检查 IP_address 的值

        :param ck_data:             ipv4 地址
        :param attr:                attr id
        :return:                    KFResult 对象
        """
        ret = self.get_ip_address(attr=attr)
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_ip_address(self, data, attr=3):
        """
        设置 IP_address 的值

        :param data:          ipv4 地址
        :param attr:          attr id
        :return:              KFResult 对象
        """
        return self.setRequest(attr, ipv4_toHex(data), "DoubleLongUnsigned", data)

    # Attribute of multicast_IP_address
    @formatResponse
    def get_multicast_ip_address(self, dataType=False, response=None):
        """
        获取 multicast_ip_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            ipv4地址数组
        """
        if response is None:
            response = self.getRequest(4)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for key, value in response[0].items():
            response[key] = hex_toIPv4(value)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_multicast_ip_address(self, ck_data):
        """
        检查 multicast_ip_address 的值

        :param ck_data:             ipv4地址数组
        :return:                    KFResult对象
        """
        checkResponsValue(self.get_multicast_ip_address(), ck_data)

    @formatResponse
    def set_multicast_ip_address(self, data):
        """
        设置 multicast_ip_address 的值

        :param data:           ipv4地址数组
        :return:               KFResult对象
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            etree.SubElement(array, "DoubleLongUnsigned").set("Value", ipv4_toHex(value))
        return self.setRequest(4, array, "Array", data)

    # Attribute of IP_options
    @formatResponse
    def get_ip_options(self, dataType=False, response=None):
        """
        获取 IP_options 的值
        IP_options ::= array IP_options_element
        IP_options_element ::= structure
        {
            IP_Option_Type: unsigned,
            IP_Option_Length: unsigned,
            IP_Option_Data: octet-string
        }

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
    def check_ip_options(self, ck_data):
        """
        检查 ip_options 的值
        IP_options ::= array IP_options_element
        IP_options_element ::= structure
        {
            IP_Option_Type: unsigned,
            IP_Option_Length: unsigned,
            IP_Option_Data: octet-string
        }

        :param ck_data:   字典
        :return:          KFResult 对象

        """
        return checkResponsValue(self.get_ip_options(), ck_data)

    @formatResponse
    def set_ip_options(self, data):
        """
        设置 ip_options 的值
        IP_options ::= array IP_options_element
        IP_options_element ::= structure
        {
            IP_Option_Type: unsigned,
            IP_Option_Length: unsigned,
            IP_Option_Data: octet-string
        }

        :param data:    字典
        :return:        KFResult 对象
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure").set("Value", ipv4_toHex(value))
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 2:
                    etree.SubElement(struct, "OctetString").set("Value", item)
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
        return self.setRequest(4, array, "Array", data)

    # Attribute of subnet_mask
    @formatResponse
    def get_subnet_mask(self, dataType=False, response=None):
        """
        获取 subnet_mask 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            子网掩码
        """
        return self.get_ip_address(dataType=dataType, response=response, attr=6)

    @formatResponse
    def check_subnet_mask(self, ck_data):
        """
        检查 subnet_mask 的值

        :param ck_data:           子网掩码
        :return:                  KFResult对象
        """
        return self.check_ip_address(ck_data, attr=6)

    @formatResponse
    def set_subnet_mask(self, data):
        """
        设置 subnet_mask 的值

        :param data:          子网掩码
        :return:              KFResult对象
        """
        return self.set_ip_address(data, attr=6)

    # Attribute of gateway_IP_address
    @formatResponse
    def get_gateway_ip_address(self, dataType=False, response=None):
        """
        获取 gateway_IP_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            网关IP地址
        """
        return self.get_ip_address(dataType=dataType, response=response, attr=7)

    @formatResponse
    def check_gateway_ip_address(self, ck_data):
        """
        检查 gateway_IP_address 的值

        :param ck_data:           网关IP地址
        :return:                  KFResult对象
        """
        return self.check_ip_address(ck_data, attr=7)

    @formatResponse
    def set_gateway_ip_address(self, data):
        """
        设置 gateway_IP_address 的值

        :param data:           网关IP地址
        :return:               KFResult对象
        """
        return self.set_ip_address(data, attr=7)

    # Attribute of use_DHCP_flag
    @formatResponse
    def get_use_dhcp_flag(self, dataType=False, response=None):
        """
        获取 use_DHCP_flag 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(8)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_use_dhcp_flag(self, ck_data):
        """
        检查 use_DHCP_flag 的值

        :param ck_data:         十进制数
        :return:                KFResult 对象
        """
        ret = self.get_use_dhcp_flag()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_use_dhcp_flag(self, data):
        """
        设置 use_DHCP_flag 的值

        :param data:            十进制数
        :return:                KFResult 对象
        """
        return self.setRequest(8, dec_toHexStr(data, 2), "Bool", data)

    # Attribute of primary_DNS_address
    @formatResponse
    def get_primary_dns_address(self, dataType=False, response=None):
        """
        获取 primary_DNS_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            primary DNS address
        """

        return self.get_ip_address(dataType=dataType, response=response, attr=9)

    @formatResponse
    def check_primary_dns_address(self, ck_data):
        """
        检查 primary_DNS_address 的值

        :param ck_data:           primary DNS address
        :return:                  KFResult 对象
        """
        return self.check_ip_address(ck_data, attr=9)

    @formatResponse
    def set_primary_dns_address(self, data):
        """
        设置 primary_DNS_address 的值

        :param data:         primary DNS address
        :return:             KFResult 对象
        """
        return self.set_ip_address(data, attr=9)

    # Attribute of secondary_DNS_address
    @formatResponse
    def get_secondary_dns_address(self, dataType=False, response=None):
        """
        获取 secondary_DNS_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            secondary_DNS_address
        """
        return self.get_ip_address(dataType=dataType, response=response, attr=10)

    @formatResponse
    def check_secondary_dns_address(self, ck_data):
        """
         检查 secondary_DNS_address 的值

        :param ck_data:          secondary DNS address
        :return:                 KFResult 对象
        """
        return self.check_ip_address(ck_data, attr=10)

    @formatResponse
    def set_secondary_dns_address(self, data):
        """
        设置 secondary_DNS_address 的值

        :param data:          secondary DNS address
        :return:              KFResult 对象
        """
        return self.set_ip_address(data, attr=10)

    # Method of act_add_mc_ip_address
    @formatResponse
    def act_add_mc_ip_address(self, data=0):
        """
        Adds one multicast IP address to the multicast_IP_address array.

        :param data:            十进制数
        :return:                KFResult 对象
        """

        return self.actionRequest(1, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Method of act_delete_mc_ip_address
    @formatResponse
    def act_delete_mc_ip_address(self, data=0):
        """
        Deletes one IP Address from the multicast_IP_address array. The IP Address to be deleted is
        identified by its value.

        :param data:            十进制数
        :return:                KFResult 对象
        """
        return self.actionRequest(2, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Method of act_get_nbof_mc_ip_addresses
    @formatResponse
    def act_get_nbof_mc_ip_addresses(self, data=0):
        """
        Returns the number of IP Addresses contained in the multicast_IP_address array

        :param data:           十进制数
        :return:               KFResult 对象
        """
        return self.actionRequest(3, dec_toHexStr(data, 2), "Unsigned", data)
