# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C23IECHDLCSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "comm_speed",
        3: "window_size_transmit",
        4: "window_size_receive",
        5: "max_info_field_length_transmit",
        6: "max_info_field_length_receive",
        7: "inter_octet_time_out",
        8: "inactivity_time_out",
        9: "device_address"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=23)

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

    # Attribute of comm_speed
    @formatResponse
    def get_comm_speed(self, dataType=False, response=None):
        """
        获取 comm_speed 的值

        :param dataType:    是否返回数据类型， 默认False不返回
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
    def check_comm_speed(self, ck_data):
        """
        检查 comm_speed 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_comm_speed()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_comm_speed(self, data):
        """
        设置 comm_speed 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(2, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of window_size_transmit
    @formatResponse
    def get_window_size_transmit(self, dataType=False, response=None):
        """
        获取 window_size_transmit 的值

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
    def check_window_size_transmit(self, ck_data):
        """
        检查 window_size_transmit 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_window_size_transmit()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_window_size_transmit(self, data):
        """
        设置 window_size_transmit 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of window_size_receive
    @formatResponse
    def get_window_size_receive(self, dataType=False, response=None):
        """
        获取 window_size_receive 的值

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
    def check_window_size_receive(self, ck_data):
        """
        检查 window_size_receive 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_window_size_receive()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_window_size_receive(self, data):
        """
        设置 window_size_receive 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(4, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of max_info_field_length_transmit
    @formatResponse
    def get_max_info_field_length_transmit(self, dataType=False, response=None):
        """
        获取 max_info_field_length_transmit 的值

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
    def check_max_info_field_length_transmit(self, ck_data):
        """
        检查 max_info_field_length_transmit 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_max_info_field_length_transmit()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_max_info_field_length_transmit(self, data):
        """
        设置 max_info_field_length_transmit 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(5, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of max_info_field_length_receive
    @formatResponse
    def get_max_info_field_length_receive(self, dataType=False, response=None):
        """
        获取 max_info_field_length_receive 的值

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
    def check_max_info_field_length_receive(self, ck_data):
        """
        检查 max_info_field_length_receive 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_max_info_field_length_receive()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_max_info_field_length_receive(self, data):
        """
        设置 max_info_field_length_receive 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(6, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of inter_octet_time_out
    @formatResponse
    def get_inter_octet_time_out(self, dataType=False, response=None):
        """
        获取 inter_octet_time_out 的值

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
    def check_inter_octet_time_out(self, ck_data):
        """
        检查 inter_octet_time_out 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_inter_octet_time_out()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_inter_octet_time_out(self, data):
        """
        设置 max_info_field_length_receive 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(7, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of inactivity_time_out
    @formatResponse
    def get_inactivity_time_out(self, dataType=False, response=None):
        """
        获取 inactivity_time_out 的值

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
    def check_inactivity_time_out(self, ck_data):
        """
        检查 inactivity_time_out 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_inactivity_time_out()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_inactivity_time_out(self, data):
        """
        设置 inactivity_time_out 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(8, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of device_address
    @formatResponse
    def get_device_address(self, dataType=False, response=None):
        """
        获取 device_address 的值

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
    def check_device_address(self, ck_data):
        """
        检查 device_address 的值

        :param ck_data:     十进制数
        :return:            KFResult 对象
        """
        ret = self.get_device_address()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_device_address(self, data):
        """
        设置 device_address 的值

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.setRequest(9, dec_toHexStr(data, 4), "LongUnsigned", data)
