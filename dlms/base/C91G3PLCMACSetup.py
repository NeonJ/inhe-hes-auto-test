# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C91G3PLCMACSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "mac_short_address",
        3: "mac_rc_coord",
        4: "mac_pan_id",
        5: "mac_key_table",
        6: "mac_frame_counter",
        7: "mac_tone_mask",
        8: "mac_tmr_ttl",
        9: "mac_max_frame_retries",
        10: "mac_neighbour_table_entry_ttl",
        11: "mac_neighbour_table",
        12: "mac_high_priority_window_size",
        13: "mac_csma_fairness_limit",
        14: "mac_beacon_randomization_window_length",
        15: "mac_a",
        16: "mac_k",
        17: "mac_min_cw_attempts",
        18: "mac_cenelec_legacy_mode",
        19: "mac_fcc_legacy_mode",
        20: "mac_max_be",
        21: "mac_max_csma_backoffs",
        22: "mac_min_be",
        23: "mac_broadcast_max_CW_enabled",
        24: "mac_transmit_atten",
        25: "mac_POS_table"
    }

    action_index_dict = {
        1: "mac_get_neighbour_table_entry"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=91)

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

    # Attribute of mac_short_address
    @formatResponse
    def get_mac_short_address(self, dataType=False, response=None):
        """
        获取 mac_short_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(2, dataType=dataType, response=response)

    @formatResponse
    def check_mac_short_address(self, ck_data):
        """
        检查 mac_short_address 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 2)

    @formatResponse
    def set_mac_short_address(self, data):
        """
        设置 mac_short_address 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 2, "LongUnsigned")

    # Attribute of mac_RC_coord
    @formatResponse
    def get_mac_rc_coord(self, dataType=False, response=None):
        """
        获取 mac_RC_coord 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(3, dataType=dataType, response=response)

    @formatResponse
    def check_mac_rc_coord(self, ck_data):
        """
        检查 mac_RC_coord 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 3)

    @formatResponse
    def set_mac_rc_coord(self, data):
        """
        设置 mac_RC_coord 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 3, "LongUnsigned")

    # Attribute of mac_PAN_id
    @formatResponse
    def get_mac_pan_id(self, dataType=False, response=None):
        """
        获取 mac_PAN_id 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(4, dataType=dataType, response=response)

    @formatResponse
    def check_mac_pan_id(self, ck_data):
        """
        检查 mac_PAN_id 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 4)

    @formatResponse
    def set_mac_pan_id(self, data):
        """
        设置 mac_PAN_id 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 4, "LongUnsigned")

    # Attribute of mac_key_table
    @formatResponse
    def get_mac_key_table(self, dataType=False, response=None):
        """
        获取 mac_key_table 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(5)

        response = getStrucDataFromGetResp(response)
        if isinstance(response[0], dict):
            for value in response[0].values():
                for index, item in enumerate(value):
                    if index == 0:
                        value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_mac_key_table(self, ck_data):
        """
        检查 mac_key_table 的值

        :param ck_data:      字典
        :return:             KFResult对象

        ck_data数据格式：
        {
            0 : [0, "00000000000000001111111111111"],
        }
        """
        return checkResponsValue(self.get_mac_key_table(), ck_data)

    @formatResponse
    def set_mac_key_table(self, data):
        """
        设置 mac_key_table 的值

        :param data:         字典
        :return:             KFResult对象

        data数据格式：
        {
            0 : [0, "00000000000000001111111111111"],
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(5, array, "Array")

    # Attribute of mac_frame_counter
    @formatResponse
    def get_mac_frame_counter(self, dataType=False, response=None):
        """
        获取 mac_frame_counter 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(6, dataType=dataType, response=response)

    @formatResponse
    def check_mac_frame_counter(self, ck_data):
        """
        检查 mac_frame_counter 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 6)

    @formatResponse
    def set_mac_frame_counter(self, data):
        """
        设置 mac_frame_counter 的值

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.__set_attr(data, 6, "DoubleLongUnsigned")

    # Attribute of mac_tone_mask
    @formatResponse
    def get_mac_tone_mask(self, dataType=False, response=None):
        """
        获取 mac_tone_mask 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            16进制字符串
        """
        if response is None:
            response = self.getRequest(7)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return bit_toHexStr(ret[0]), ret[1]
        return bit_toHexStr(ret[0])

    @formatResponse
    def check_mac_tone_mask(self, ck_data):
        """
        检查 mac_tone_mask 的值

        :param ck_data:    16进制字符串
        :return:           KFResult对象
        """
        ret = self.get_mac_tone_mask()
        if str(ck_data).startswith("0x"):
            ck_data = ck_data[2:]
        else:
            ck_data = hex(ck_data)[2:]
        if ret == ck_data:
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_mac_tone_mask(self, data):
        """
        设置 mac_tone_mask 的值

        :param data:     16进制字符串
        :return:         KFResult对象
        """
        if str(data).startswith("0x"):
            data = data[2:]
        elif str(data).find("F") != -1:
            data = data
        else:
            data = hex(data)[2:]
        return self.setRequest(7, hex_toBitStr(data), "BitString")

    # Attribute of mac_TMR_TTL
    @formatResponse
    def get_mac_tmr_ttl(self, dataType=False, response=None):
        """
        获取 mac_TMR_TTL 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(8, dataType=dataType, response=response)

    @formatResponse
    def check_mac_tmr_ttl(self, ck_data):
        """
        检查 mac_TMR_TTL 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        return self.__check_attr(ck_data, 8)

    @formatResponse
    def set_mac_tmr_ttl(self, data):
        """
        设置 mac_TMR_TTL 的值

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.__set_attr(data, 8, "Unsigned")

    # Attribute of mac_max_frame_retries
    @formatResponse
    def get_mac_max_frame_retries(self, dataType=False, response=None):
        """
        获取 mac_max_frame_retries 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(9, dataType=dataType, response=response)

    @formatResponse
    def check_mac_max_frame_retries(self, ck_data):
        """
        检查 mac_max_frame_retries 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 9)

    @formatResponse
    def set_mac_max_frame_retries(self, data):
        """
        设置 mac_max_frame_retries 的值

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.__set_attr(data, 9, "Unsigned")

    # Attribute of mac_neighbour_table_entry_TTL
    @formatResponse
    def get_mac_neighbour_table_entry_ttl(self, dataType=False, response=None):
        """
        获取 mac_neighbour_table_entry_TTL 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(10, dataType=dataType, response=response)

    @formatResponse
    def check_mac_neighbour_table_entry_ttl(self, ck_data):
        """
        检查 mac_neighbour_table_entry_TTL 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 10)

    @formatResponse
    def set_mac_neighbour_table_entry_ttl(self, data):
        """
        设置 mac_neighbour_table_entry_TTL 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 10, "Unsigned")

    # Attribute of mac_neighbour_table
    @formatResponse
    def get_mac_neighbour_table(self, dataType=False, response=None):
        """
        获取 mac_neighbour_table 的值

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
                if index in [0, 3, 4, 5, 7, 8, 9, 10]:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_mac_neighbour_table(self, ck_data):
        """
        检查 mac_neighbour_table 的值

        :param ck_data:      字典
        :return:             KFResult对象

        neighbour_table ::= structure
        {
            short_address: long-unsigned,
            payload_modulation_scheme: boolean,
            tone_map: bit-string,
            modulation: enum,
            tx_gain: integer,
            tx_res: enum,
            tx_coeff: bit-string,
            lqi: unsigned,
            phase_differential integer,
            TMR_valid_time: unsigned,
            neighbour_valid_time: unsigned
        }
        """
        return checkResponsValue(self.get_mac_neighbour_table(), ck_data)

    @formatResponse
    def set_mac_neighbour_table(self, data):
        """
        设置 mac_neighbour_table 的值

        :param data:         字典
        :return:             KFResult对象

        neighbour_table ::= structure
        {
            short_address: long-unsigned,
            payload_modulation_scheme: boolean,
            tone_map: bit-string,
            modulation: enum,
            tx_gain: integer,
            tx_res: enum,
            tx_coeff: bit-string,
            lqi: unsigned,
            phase_differential integer,
            TMR_valid_time: unsigned,
            neighbour_valid_time: unsigned
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                elif subIndex == 1:
                    etree.SubElement(struct, "Boolean,").set("Value", subItem)
                elif subIndex in [2, 6]:
                    etree.SubElement(struct, "BitString").set("Value", subItem)
                elif subIndex in [3, 5]:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(subItem, 2))
                elif subIndex in [4, 8]:
                    etree.SubElement(struct, "Integer,").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "Unsigned,").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(11, array, "Array")

    # Attribute of mac_high_priority_window_size
    @formatResponse
    def get_mac_high_priority_window_size(self, dataType=False, response=None):
        """
        获取 mac_high_priority_window_size 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(12, dataType=dataType, response=response)

    @formatResponse
    def check_mac_high_priority_window_size(self, ck_data):
        """
        检查 mac_high_priority_window_size 的值

        :param ck_data:       十进制数
        :return:              KFResult对象
        """
        return self.__check_attr(ck_data, 12)

    @formatResponse
    def set_mac_high_priority_window_size(self, data):
        """
        设置 mac_high_priority_window_size 的值

        :param data:          十进制数
        :return:              KFResult对象
        """
        return self.__set_attr(data, 12, "Unsigned")

    # Attribute of mac_CSMA_fairness_limit
    @formatResponse
    def get_mac_csma_fairness_limit(self, dataType=False, response=None):
        """
        获取 mac_CSMA_fairness_limit 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(13, dataType=dataType, response=response)

    @formatResponse
    def check_mac_csma_fairness_limit(self, ck_data):
        """
        检查 mac_CSMA_fairness_limit 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 13)

    @formatResponse
    def set_mac_csma_fairness_limit(self, data):
        """
        设置 mac_CSMA_fairness_limit 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 13, "Unsigned")

    # Attribute of mac_beacon_randomization_window_length
    @formatResponse
    def get_mac_beacon_randomization_window_length(self, dataType=False, response=None):
        """
        获取 mac_beacon_randomization_window_length 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(14, dataType=dataType, response=response)

    @formatResponse
    def check_mac_beacon_randomization_window_length(self, ck_data):
        """
        检查 mac_beacon_randomization_window_length 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 14)

    @formatResponse
    def set_mac_beacon_randomization_window_length(self, data):
        """
        设置 mac_beacon_randomization_window_length 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 14, "Unsigned")

    # Attribute of mac_A
    @formatResponse
    def get_mac_a(self, dataType=False, response=None):
        """
        获取 mac_A 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(15, dataType=dataType, response=response)

    @formatResponse
    def check_mac_a(self, ck_data):
        """
        检查 mac_A 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 15)

    @formatResponse
    def set_mac_a(self, data):
        """
        设置 mac_A 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 15, "Unsigned")

    # Attribute of mac_K
    @formatResponse
    def get_mac_k(self, dataType=False, response=None):
        """
        获取 mac_K 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(16, dataType=dataType, response=response)

    @formatResponse
    def check_mac_k(self, ck_data):
        """
        检查 mac_K 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 16)

    @formatResponse
    def set_mac_k(self, data):
        """
        设置 mac_K 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 16, "Unsigned")

    # Attribute of mac_min_CW_attempts
    @formatResponse
    def get_mac_min_cw_attempts(self, dataType=False, response=None):
        """
        获取 mac_min_CW_attempts 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(17, dataType=dataType, response=response)

    @formatResponse
    def check_mac_min_cw_attempts(self, ck_data):
        """
        检查 mac_min_CW_attempts 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 17)

    @formatResponse
    def set_mac_min_cw_attempts(self, data):
        """
        设置 mac_min_CW_attempts 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 17, "Unsigned")

    # Attribute of mac_cenelec_legacy_mode
    @formatResponse
    def get_mac_cenelec_legacy_mode(self, dataType=False, response=None):
        """
        获取 mac_cenelec_legacy_mode 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(18, dataType=dataType, response=response)

    @formatResponse
    def check_mac_cenelec_legacy_mode(self, ck_data):
        """
        检查 mac_cenelec_legacy_mode 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 18)

    @formatResponse
    def set_mac_cenelec_legacy_mode(self, data):
        """
        设置 mac_cenelec_legacy_mode 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 18, "Unsigned")

    # Attribute of mac_FCC_legacy_mode
    @formatResponse
    def get_mac_fcc_legacy_mode(self, dataType=False, response=None):
        """
        获取 mac_FCC_legacy_mode 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(19, dataType=dataType, response=response)

    @formatResponse
    def check_mac_fcc_legacy_mode(self, ck_data):
        """
        检查 mac_FCC_legacy_mode 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 19)

    @formatResponse
    def set_mac_fcc_legacy_mode(self, data):
        """
        设置 mac_FCC_legacy_mode 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 19, "Unsigned")

    # Attribute of mac_max_BE
    @formatResponse
    def get_mac_max_be(self, dataType=False, response=None):
        """
        获取 mac_max_BE 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(20, dataType=dataType, response=response)

    @formatResponse
    def check_mac_max_be(self, ck_data):
        """
        检查 mac_max_BE 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 20)

    @formatResponse
    def set_mac_max_be(self, data):
        """
        设置 mac_max_BE 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 20, "Unsigned")

    # Attribute of mac_max_CSMA_backoffs
    @formatResponse
    def get_mac_max_csma_backoffs(self, dataType=False, response=None):
        """
        获取 mac_max_CSMA_backoffs 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(21, dataType=dataType, response=response)

    @formatResponse
    def check_mac_max_csma_backoffs(self, ck_data):
        """
        检查 mac_max_CSMA_backoffs 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 21)

    @formatResponse
    def set_mac_max_csma_backoffs(self, data):
        """
        设置 mac_max_CSMA_backoffs 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 21, "Unsigned")

    # Attribute of mac_min_BE
    @formatResponse
    def get_mac_min_be(self, dataType=False, response=None):
        """
        获取 mac_min_BE 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(22, dataType=dataType, response=response)

    @formatResponse
    def check_mac_min_be(self, ck_data):
        """
        检查 mac_min_BE 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 22)

    @formatResponse
    def set_mac_min_be(self, data):
        """
        设置 mac_min_BE 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 22, "Unsigned")

    # Attribute of mac_broadcast_max_CW_enabled
    @formatResponse
    def get_mac_broadcast_max_CW_enabled(self, dataType=False, response=None):
        """
        获取 mac_broadcast_max_CW_enabled 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(23, dataType=dataType, response=response)

    @formatResponse
    def check_mac_broadcast_max_CW_enabled(self, ck_data):
        """
        检查 mac_broadcast_max_CW_enabled 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 23)

    @formatResponse
    def set_mac_broadcast_max_CW_enabled(self, data):
        """
        设置 mac_broadcast_max_CW_enabled 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 23, "Bool")

    # Attribute of mac_mac_transmit_atten
    @formatResponse
    def get_mac_transmit_atten(self, dataType=False, response=None):
        """
        获取 mac_transmit_atten 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(24, dataType=dataType, response=response)

    @formatResponse
    def check_mac_transmit_atten(self, ck_data):
        """
        检查 mac_transmit_atten 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 24)

    @formatResponse
    def set_mac_transmit_atten(self, data):
        """
        设置 mac_transmit_atten 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 24, "Unsigned")

    # Attribute of mac_POS_table
    @formatResponse
    def get_mac_POS_table(self, dataType=False, response=None):
        """
        获取 mac_POS_table 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            数组
        """
        if response is None:
            response = self.getRequest(25)

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
    def check_mac_POS_table(self, ck_data):
        """
        检查 mac_POS_table 的值

        :param ck_data:    数组
        :return:           KFResult对象

        ck_data 数据格式：
        {
            0 : [1, 0, 0]
        }
        """
        return checkResponsValue(self.get_mac_POS_table(), ck_data)

    @formatResponse
    def set_mac_POS_table(self, data):
        """
        设置 mac_POS_table 的值

        :param data:    数组
        :return:        KFResult对象

        ck_data 数据格式：
        {
            0 : [1, 0, 0]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(25, array, "Array")

    # Method of mac_get_neighbour_table_entry
    @formatResponse
    def act_mac_get_neighbour_table_entry(self, data=0):
        """
        This method is used to retrieve the mac neighbour table for one MAC short address.
        It may be used to perform topology monitoring by the client.

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 4), "LongUnsigned", data)
