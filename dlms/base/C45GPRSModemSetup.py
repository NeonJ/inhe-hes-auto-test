# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C45GPRSModemSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "apn",
        3: "pin_code",
        4: "quality_of_service"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=45)

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

    # Attribute of APN
    @formatResponse
    def get_apn(self, dataType=False, response=None):
        """
        获取 APN 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return ret
        return hex_toOBIS(ret[0])

    @formatResponse
    def check_apn(self, ck_data):
        """
        检查 APN 的值

        :param ck_data:            字符串
        :return:                   KFResult对象
        """
        ret = self.get_apn()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_apn(self, data):
        """
        设置 APN 的值

        :param data:        字符串
        :return:            KFResult对象
        """
        return self.setRequest(2, obis_toHex(data), "OctetString", data)

    # Attribute of PIN_code
    @formatResponse
    def get_pin_code(self, dataType=False, response=None):
        """
        获取 PIN_code 的值

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
    def check_pin_code(self, ck_data):
        """
        检查 PIN_code 的值

        :param ck_data:           十进制数
        :return:                  KFResult对象
        """
        ret = self.get_pin_code()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_pin_code(self, data):
        """
        设置 PIN_code 的值

        :param data:              十进制数
        :return:                  KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of quality_of_service
    @formatResponse
    def get_quality_of_service(self, dataType=False, response=None):
        """
        获取 quality_of_service 的值

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
    def check_quality_of_service(self, ck_data):
        """
        检查 quality_of_service 的值

        :param ck_data:         字典
        :return:                KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [0, 0, 0, 0, 0],
            1: [0, 0, 0, 0, 0]
        }
        """
        return checkResponsValue(self.get_quality_of_service(), ck_data)

    @formatResponse
    def set_quality_of_service(self, data):
        """
        设置 quality_of_service 的值

        :param data:            字典
        :return:                KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [0, 0, 0, 0, 0],
            1: [0, 0, 0, 0, 0]
        }
        """
        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            sub_struct = etree.SubElement(struct, "Structure")
            sub_struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(sub_struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(4, struct, "Struct", data)
