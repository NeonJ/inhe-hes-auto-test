# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C44PPPSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "phy_reference",
        3: "lcp_options",
        4: "ipcp_options",
        5: "ppp_authentication"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=44)

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

    # Attribute of PHY_reference
    @formatResponse
    def get_phy_reference(self, dataType=False, response=None):
        """
        获取 PHY_reference 的值

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
    def check_phy_reference(self, ck_data):
        """
        检查 PHY_reference 的值

        :param ck_data:         点分十进制形式的OBIS值
        :return:                KFResult对象
        """
        ret = self.get_phy_reference()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_phy_reference(self, data):
        """
        设置 PHY_reference 的值

        :param data:         点分十进制形式的OBIS值
        :return:             KFResult对象
        """
        return self.setRequest(2, obis_toHex(data), "OctetString", data)

    # Attribute of LCP_options
    @formatResponse
    def get_lcp_options(self, dataType=False, response=None):
        """
        获取 LCP_options 的值

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
        for value in response[0].values():
            for index, item in enumerate(value):
                value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_lcp_options(self, ck_data):
        """
        检查 LCP_options 的值

        :param ck_data:         期望值（一个字典）
        :return:                返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [3, 4, 49187]
        }
        """
        return checkResponsValue(self.get_lcp_options(), ck_data)

    @formatResponse
    def set_lcp_options(self, data):
        """
        设置  LCP_options 的值

        :param data:         期望值（一个字典）
        :return:             返回一个KFResult对象

         data 是一个字典, 描述了预期的结果数据
        {
            0: [3, 4, 49187]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0 or subIndex == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(3, array, "Array", data)

    # Attribute of IPCP_options
    @formatResponse
    def get_ipcp_options(self, dataType=False, response=None):
        """
        获取 IPCP_options 的值

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
                value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_ipcp_options(self, ck_data):
        """
        检查 IPCP_options 的值

        :param ck_data:         期望值（一个字典）
        :return:                返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [2, 4, 0]
        }
        """
        return checkResponsValue(self.get_ipcp_options(), ck_data)

    @formatResponse
    def set_ipcp_options(self, data):
        """
        检查 IPCP_options 的值

        :param data:             期望值（一个字典）
        :return:                 返回一个KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [2, 4, 0]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0 or subIndex == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(4, array, "Array", data)

    # Attribute of PPP_authentication
    @formatResponse
    def get_ppp_authentication(self, dataType=False, response=None):
        """
        获取 PPP_authentication 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(5)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                value[index] = hex_toOBIS(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_ppp_authentication(self, ck_data):
        """
        检查 PPP_authentication 的值

        :param ck_data:             期望值（一个字典）
        :return:                    返回一个KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['', '']
        }
        """
        return checkResponsValue(self.get_ppp_authentication(), ck_data)

    @formatResponse
    def set_ppp_authentication(self, data):
        """
        设置 PPP_authentication 的值

        :param data:             期望值（一个字典）
        :return:                 返回一个KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['', '']
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
        return self.setRequest(5, struct, "Struct", data)
