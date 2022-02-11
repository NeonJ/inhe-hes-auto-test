# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C19IECLocalPortSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "default_mode",
        3: "default_baud",
        4: "prop_baud",
        5: "response_time",
        6: "device_addr",
        7: "pass_p1",
        8: "pass_p2",
        9: "pass_w5",
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=19)

    # Attribute of logical_name (No.1)
    @formatResponse
    def get_logical_name(self, dataType=False, response=None):
        """
        获取 logical_name 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    点分十进制形式的OBIS值
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

    # Attribute of default_mode (No.2)
    @formatResponse
    def get_default_mode(self, dataType=False, response=None):
        """
        获取 default_mode 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(2)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_default_mode(self, ck_data):
        """
        检查 default_mode 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_default_mode()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_default_mode(self, data):
        """
         设置 default_mode 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(2, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of default_baud (No.3)
    @formatResponse
    def get_default_baud(self, dataType=False, response=None):
        """
        获取 default_baud 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(3)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_default_baud(self, ck_data):
        """
        检查 default_baud 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_default_baud()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_default_baud(self, data):
        """
         设置 default_baud 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of prop_baud (No.4)
    @formatResponse
    def get_prop_baud(self, dataType=False, response=None):
        """
        获取 prop_baud 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(4)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_prop_baud(self, ck_data):
        """
        检查 prop_baud 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_prop_baud()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_prop_baud(self, data):
        """
         设置 prop_baud 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(4, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of response_time (No.5)
    @formatResponse
    def get_response_time(self, dataType=False, response=None):
        """
        获取 response_time 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(5)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_response_time(self, ck_data):
        """
        检查 response_time 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_response_time()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_response_time(self, data):
        """
         设置 response_time 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(5, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of device_addr (No.6)
    @formatResponse
    def get_device_addr(self, dataType=False, response=None):
        """
        获取 response_time 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(6)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_device_addr(self, ck_data):
        """
        检查 device_addr 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_device_addr()
        if str(ret) == str(ck_data):
            return KFResult(True, "")

        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_device_addr(self, data):
        """
         设置 device_addr 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(6, data, "OctetString", data)

    # Attribute of pass_p1 (No.7)
    @formatResponse
    def get_pass_p1(self, dataType=False, response=None):
        """
        获取 pass_p1 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(7)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_pass_p1(self, ck_data):
        """
        检查 pass_p1 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_pass_p1()
        if str(ret) == str(ck_data):
            return KFResult(True, "")

        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_pass_p1(self, data):
        """
         设置 pass_p1 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(7, data, "OctetString", data)

    # Attribute of pass_p2 (No.8)
    @formatResponse
    def get_pass_p2(self, dataType=False, response=None):
        """
        获取 pass_p2 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(8)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_pass_p2(self, ck_data):
        """
        检查 pass_p2 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_pass_p2()
        if str(ret) == str(ck_data):
            return KFResult(True, "")

        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_pass_p2(self, data):
        """
         设置 pass_p2 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(8, data, "OctetString", data)

    # Attribute of pass_w5 (No.9)
    @formatResponse
    def get_pass_w5(self, dataType=False, response=None):
        """
        获取 pass_w5 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(9)

        response = getSingleDataFromGetResp(response)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_pass_w5(self, ck_data):
        """
        检查 pass_w5 的值

        :param ck_data:     期望值
        :return:            KFResult 对象
        """
        ret = self.get_pass_w5()
        if str(ret) == str(ck_data):
            return KFResult(True, "")

        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_pass_w5(self, data):
        """
         设置 pass_w5 的值

        :param data:       接收一个数值
        :return:           KFResult 对象
        """
        return self.setRequest(9, data, "OctetString", data)
