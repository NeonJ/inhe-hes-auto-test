# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C90G3PLCMACLayerCounters(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "mac_tx_data_packet_count",
        3: "mac_rx_data_packet_count",
        4: "mac_tx_cmd_packet_count",
        5: "mac_rx_cmd_packet_count",
        6: "mac_csma_fail_count",
        7: "mac_csma_no_ack_count",
        8: "mac_bad_crc_count",
        9: "mac_tx_data_broadcast_count",
        10: "mac_rx_data_broadcast_count"
    }

    action_index_dict = {
        1: "reset"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=90)

    # Common get/set/check method for double-long-unsigned type
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

    def __set_attr(self, data, attr_id):
        return self.setRequest(attr_id, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of logical_name (No.1)
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

    # Attribute of mac_Tx_data_packet_count (No.2)
    @formatResponse
    def get_mac_tx_data_packet_count(self, dataType=False, response=None):
        """
        获取 mac_Tx_data_packet_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(2, dataType=dataType, response=response)

    @formatResponse
    def check_mac_tx_data_packet_count(self, ck_data):
        """
        检查 mac_Tx_data_packet_count 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        return self.__check_attr(ck_data, 2)

    @formatResponse
    def set_mac_tx_data_packet_count(self, data):
        """
        设置 mac_Tx_data_packet_count 的值

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.__set_attr(data, 2)

    # Attribute of mac_Rx_data_packet_count (No.3)
    @formatResponse
    def get_mac_rx_data_packet_count(self, dataType=False, response=None):
        """
        获取 mac_Rx_data_packet_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(3, dataType=dataType, response=response)

    @formatResponse
    def check_mac_rx_data_packet_count(self, ck_data):
        """
        检查 mac_Rx_data_packet_count 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 3)

    @formatResponse
    def set_mac_rx_data_packet_count(self, data):
        """
        设置 mac_Rx_data_packet_count 的值

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.__set_attr(data, 3)

    # Attribute of mac_Tx_cmd_packet_count (No.4)
    @formatResponse
    def get_mac_tx_cmd_packet_count(self, dataType=False, response=None):
        """
        获取 mac_Tx_cmd_packet_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(4, dataType=dataType, response=response)

    @formatResponse
    def check_mac_tx_cmd_packet_count(self, ck_data):
        """
        检查 mac_Tx_cmd_packet_count 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 4)

    @formatResponse
    def set_mac_tx_cmd_packet_count(self, data):
        """
        获取 mac_Tx_cmd_packet_count 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 4)

    # Attribute of mac_Rx_cmd_packet_count(No.5)
    @formatResponse
    def get_mac_rx_cmd_packet_count(self, dataType=False, response=None):
        """
        获取 mac_Rx_cmd_packet_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(5, dataType=dataType, response=response)

    @formatResponse
    def check_mac_rx_cmd_packet_count(self, ck_data):
        """
        检查 mac_Rx_cmd_packet_count 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 5)

    @formatResponse
    def set_mac_rx_cmd_packet_count(self, data):
        """
        设置 mac_Rx_cmd_packet_count 的值

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.__set_attr(data, 5)

    # Attribute of mac_CSMA_fail_count(No.6)
    @formatResponse
    def get_mac_csma_fail_count(self, dataType=False, response=None):
        """
        获取 mac_CSMA_fail_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(6, dataType=dataType, response=response)

    @formatResponse
    def check_mac_csma_fail_count(self, ck_data):
        """
        检查 mac_CSMA_fail_count 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        return self.__check_attr(ck_data, 6)

    @formatResponse
    def set_mac_csma_fail_count(self, data):
        """
        设置 mac_CSMA_fail_count 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 6)

    # Attribute of mac_CSMA_no_ACK_count (No.7)
    @formatResponse
    def get_mac_csma_no_ack_count(self, dataType=False, response=None):
        """
        获取 mac_CSMA_no_ACK_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(7, dataType=dataType, response=response)

    @formatResponse
    def check_mac_csma_no_ack_count(self, ck_data):
        """
        检查 mac_CSMA_no_ACK_count 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 7)

    @formatResponse
    def set_mac_csma_no_ack_count(self, data):
        """
        设置 mac_CSMA_no_ACK_count 的值

        :param data:  十进制数
        :return:      KFResult对象
        """
        return self.__set_attr(data, 7)

    # Attribute of mac_bad_CRC_count(No.8)
    @formatResponse
    def get_mac_bad_crc_count(self, dataType=False, response=None):
        """
        获取 mac_bad_CRC_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(8, dataType=dataType, response=response)

    @formatResponse
    def check_mac_bad_crc_count(self, ck_data):
        """
        检查 mac_bad_CRC_count 的值

        :param ck_data:  十进制数
        :return:         KFResult对象
        """
        return self.__check_attr(ck_data, 8)

    @formatResponse
    def set_mac_bad_crc_count(self, data):
        """
        设置 mac_bad_CRC_count 的值

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.__set_attr(data, 8)

    # Attribute of mac_Tx_data_broadcast_count (No.9)
    @formatResponse
    def get_mac_tx_data_broadcast_count(self, dataType=False, response=None):
        """
        获取 mac_Tx_data_broadcast_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(9, dataType=dataType, response=response)

    @formatResponse
    def check_mac_tx_data_broadcast_count(self, ck_data):
        """
        检查 mac_Tx_data_broadcast_count 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 9)

    @formatResponse
    def set_mac_tx_data_broadcast_count(self, data):
        """
        设置 mac_Tx_data_broadcast_count 的值

        :param data:  十进制数
        :return:      KFResult对象
        """
        return self.__set_attr(data, 9)

    # Attribute of mac_Rx_data_broadcast_count (No.10)
    @formatResponse
    def get_mac_rx_data_broadcast_count(self, dataType=False, response=None):
        """
        获取 mac_Rx_data_broadcast_count 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(10, dataType=dataType, response=response)

    @formatResponse
    def check_mac_rx_data_broadcast_count(self, ck_data):
        """
        检查 mac_Rx_data_broadcast_count 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        return self.__check_attr(ck_data, 10)

    @formatResponse
    def set_mac_rx_data_broadcast_count(self, data):
        """
        设置 mac_Rx_data_broadcast_count 的值

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.__set_attr(data, 10)

    @formatResponse
    def act_reset(self, data=0):
        """
        This method forces a reset of the object. By invoking this method,
        the value of all counters is set to 0.

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)
