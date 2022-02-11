# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C40PushSetup(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "push_object_list",
        3: "send_destination_and_method",
        4: "communication_window",
        5: "randomisation_start_interval",
        6: "number_of_retries",
        7: "repetition_delay"
    }

    action_index_dict = {
        1: "push"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=40)

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

    # Attribute of push_object_list
    @formatResponse
    def get_push_object_list(self, dataType=False, response=None):
        """
        获取 push_object_list 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(2)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                if index == 0:
                    value[index] = hex_toDec(item)  # class_id
                if index == 1:
                    value[index] = hex_toOBIS(item)  # logical_name
                if index == 2:
                    value[index] = hex_toDec(item)  # attribute_index
                if index == 3:
                    value[index] = hex_toDec(item)  # data_index
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_push_object_list(self, ck_data):
        """
        检查 push_object_list 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            class_id: long-unsigned,
            logical_name: octet-string,
            attribute_index: integer,
            data_index: long-unsigned
        }
        """
        return checkResponsValue(self.get_push_object_list(), ck_data)

    @formatResponse
    def set_push_object_list(self, data):
        """
        设置 push_object_list 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            class_id: long-unsigned,
            logical_name: octet-string,
            attribute_index: integer,
            data_index: long-unsigned
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                if index == 1:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(item))
                if index == 2:
                    etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(item, 2))
                if index == 3:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
        return self.setRequest(2, array, "Array", data)

    # Attribute of send_destination_and_method
    @formatResponse
    def get_send_destination_and_method(self, dataType=False, response=None):
        """
        获取 send_destination_and_method 的值

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
                if index in [0, 2]:
                    value[index] = hex_toDec(item)
                if index == 1:
                    # cetus02 和 cetus05 返回结果不一致， 需要分开处理
                    # value[index] = hex_toAscii(item)
                    value[index] = item
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_send_destination_and_method(self, ck_data):
        """
        检查 send_destination_and_method 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            transport_service: transport_service_type,
            destination: octet-string,
            message: message_type
        }
        transport_service_type ::= enum:
            (0) TCP,
            (1) UDP,
            (2) reserved for FTP,
            (3) reserved for SMTP,
            (4) SMS,
            (5) HDLC
            (6) reserved for M-Bus
            (7) reserved for ZigBee®
            (200...255) manufacturer specific
        message_type ::= enum:
            (0) A-XDR encoded xDLMS APDU,
            (1) XML encoded xDLMS APDU,
            (128...255) manufacturer specific
        """
        return checkResponsValue(self.get_send_destination_and_method(), ck_data)

    @formatResponse
    def set_send_destination_and_method(self, data):
        """
        设置 send_destination_and_method 的值

        :param data:        字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            transport_service: transport_service_type,
            destination: octet-string,
            message: message_type
        }
        transport_service_type ::= enum:
            (0) TCP,
            (1) UDP,
            (2) reserved for FTP,
            (3) reserved for SMTP,
            (4) SMS,
            (5) HDLC
            (6) reserved for M-Bus
            (7) reserved for ZigBee®
            (200...255) manufacturer specific
        message_type ::= enum:
            (0) A-XDR encoded xDLMS APDU,
            (1) XML encoded xDLMS APDU,
            (128...255) manufacturer specific
        """
        struct = etree.Element("Structure")
        if len(data) > 0:
            for value in data.values():
                struct.set("Qty", dec_toHexStr(len(value), 4))
                for index, item in enumerate(value):
                    if index in [0, 2]:
                        etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(item, 2))
                    if index == 1:
                        # etree.SubElement(struct, "OctetString").set("Value", ascii_toHex(item))
                        etree.SubElement(struct, "OctetString").set("Value", item)
        else:
            struct.set("Qty", dec_toHexStr(0, 4))
        return self.setRequest(3, struct, "Struct", data)

    # Attribute of communication_window
    @formatResponse
    def get_communication_window(self, dataType=False, response=None):
        """
        获取 communication_window 的值

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
                value[index] = hex_toWildcardTimeString(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_communication_window(self, ck_data):
        """
        检查 communication_window 的值

        :param ck_data:     字典
        :return:            KFResult 对象

        ck_data数据格式为：
        {
            start_time: octet-string,
            end_time: octet-string
        }
        """
        return checkResponsValue(self.get_communication_window(), ck_data)

    @formatResponse
    def set_communication_window(self, data):
        """
        设置 communication_window 的值

        :param data:        字典
        :return:            KFResult 对象

        data数据格式为：
        {
            0: [start_time, end_time],
            1: [start_time, end_time],
            ...
        }
        """
        array = etree.Element("Array")
        if len(data) > 0:
            array.set("Qty", dec_toHexStr(len(data), length=4))
            for value in data.values():
                struct = etree.SubElement(array, "Structure")
                struct.set("Qty", dec_toHexStr(len(value), 4))
                for index, item in enumerate(value):
                    etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(item))
        else:
            array.set("Qty", dec_toHexStr(0, length=4))

        return self.setRequest(4, array, "Array", data)

    # Attribute of randomisation_start_interval (No.5)
    @formatResponse
    def get_randomisation_start_interval(self, dataType=False, response=None):
        """
        获取 capture_period 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    LongUnsigned
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
    def check_randomisation_start_interval(self, ck_data):
        """
        检查 capture_period 的值

        :param ck_data:             LongUnsigned
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_randomisation_start_interval()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_randomisation_start_interval(self, data):
        """
        设置 capture_period 的值
        :param data:                LongUnsigned
        :return:                    返回一个 KFResult 对象
        """
        return self.setRequest(5, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Attribute of number_of_retries (No.6)
    @formatResponse
    def get_number_of_retries(self, dataType=False, response=None):
        """
        获取 number_of_retries 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    十进制数
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
    def check_number_of_retries(self, ck_data):
        """
        检查 number_of_retries 的值

        :param ck_data:             十进制数
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_number_of_retries()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_number_of_retries(self, data):
        """
        设置 number_of_retries 的值

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        return self.setRequest(6, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of repetition_delay (No.7)
    @formatResponse
    def get_repetition_delay(self, dataType=False, response=None):
        """
        获取 repetition_delay 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    十进制数
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
    def check_repetition_delay(self, ck_data):
        """
        检查 repetition_delay 的值

        :param ck_data:             十进制数
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_repetition_delay()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_repetition_delay(self, data):
        """
        设置 repetition_delay 的值

        :param data:                十进制数
        :return:                    返回一个 KFResult 对象
        """
        return self.setRequest(7, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Method of push
    @formatResponse
    def act_push(self, index=0):
        """
        Activates the push process leading to the elaboration and the sending of the push data taking into
        account the values of the attributes defined in the given instance of this IC.

        :param index:              十进制数
        :return:                   返回一个 KFResult 对象
        """
        return self.actionRequest(1, dec_toHexStr(index, 2), "Integer", index)
