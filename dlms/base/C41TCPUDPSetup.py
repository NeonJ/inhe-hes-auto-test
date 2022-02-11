# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C41TCPUDPSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "tcp_udp_port",
        3: "ip_reference",
        4: "mss",
        5: "nb_of_sim_conn",
        6: "inactivity_time_out"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=41)

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

    # Attribute of TCP-UDP_port
    @formatResponse
    def get_tcp_udp_port(self, dataType=False, response=None):
        """
        获取 TCP-UDP port 的值

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
    def check_tcp_udp_port(self, ck_data):
        """
        检查 TCP-UDP port 的值

        :param ck_data:    十进制数
        :return:           KFResult 对象
        """
        ret = self.get_tcp_udp_port()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_tcp_udp_port(self, data):
        """
        设置 TCP-UDP port 的值

        :param data:       十进制数
        :return:           KFResult 对象
        """
        return self.setRequest(2, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of IP_reference
    @formatResponse
    def get_ip_reference(self, dataType=False, response=None):
        """
        获取 IP_reference 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            点分十进制形式的OBIS值
        """
        if response is None:
            response = self.getRequest(3)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toOBIS(ret[0]), ret[1]
        return hex_toOBIS(ret[0])

    @formatResponse
    def check_ip_reference(self, ck_data):
        """
        检查 IP_reference 的值

        :param ck_data:     点分十进制形式的OBIS值
        :return:            KFResult 对象
        """
        ret = self.get_ip_reference()
        if ret.lower() == ck_data.lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_ip_reference(self, data):
        """
        设置 IP_reference 的值

        :param data:        点分十进制形式的OBIS值
        :return:            KFResult 对象
        """
        return self.setRequest(3, obis_toHex(data), "OctetString", data)

    # Attribute of MSS
    @formatResponse
    def get_mss(self, dataType=False, response=None):
        """
        获取 MSS 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            LongUnsigned
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
    def check_mss(self, ck_data):
        """
        检查 MSS 的值

        :param ck_data:           十进制数
        :return:                  KFResult 对象
        """
        ret = self.get_mss()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_mss(self, data):
        """
        设置 MSS 的值

        :param data:      十进制数
        :return:          KFResult 对象
        """
        return self.setRequest(4, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of nb_of_sim_conn
    @formatResponse
    def get_nb_of_sim_conn(self, dataType=False, response=None):
        """
        获取 nb_of_sim_conn 的值

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
    def check_nb_of_sim_conn(self, ck_data):
        """
        检查 nb_of_sim_conn 的值

        :param ck_data:          十进制数
        :return:                 KFResult对象
        """
        ret = self.get_nb_of_sim_conn()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_nb_of_sim_conn(self, data):
        """
        设置 nb_of_sim_conn 的值

        :param data:              十进制数
        :return:                  KFResult对象
        """
        return self.setRequest(5, dec_toHexStr(data, 2), "Unsigned", data)

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
    def check_inactivity_time_out(self, ck_data):
        """
        检查 inactivity_time_out 的值

        :param ck_data:           十进制数
        :return:                  KFResult对象
        """
        ret = self.get_inactivity_time_out()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_inactivity_time_out(self, data):
        """
        设置 inactivity_time_out 的值

        :param data:            十进制数
        :return:                KFResult对象
        """
        return self.setRequest(6, dec_toHexStr(data, 4), "LongUnsigned", data)
