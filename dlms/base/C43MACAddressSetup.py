# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C43MACAddressSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "mac_address"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=43)

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

    # Attribute of MAC_address
    @formatResponse
    def get_mac_address(self, dataType=False, response=None):
        """
        获取 MAC_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_mac_address(self, ck_data):
        """
        检查 MAC_address 的值

        :param ck_data:       字符串
        :return:              KFResult对象
        """
        return checkResponsValue(self.get_mac_address(), ck_data)

    @formatResponse
    def set_mac_address(self, data):
        """
        设置 MAC_address 的值

        :param data:         字符串
        :return:             KFResult对象
        """
        return self.setRequest(2, data, "OctetString", data)
