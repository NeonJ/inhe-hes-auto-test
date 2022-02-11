# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C72MBusClient(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "mbus_port_reference",
        3: "capture_definition",
        4: "capture_period",
        5: "primary_address",
        6: "identification_number",
        7: "manufacturer_id",
        8: "version",
        9: "device_type",
        10: "access_number",
        11: "status",
        12: "alarm",
        13: "configuration",
        14: "encryption_key_status"
    }

    action_index_dict = {
        1: "slave_install",
        2: "slave_deinstall",
        3: "capture",
        4: "reset_alarm",
        5: "synchronize_clock",
        6: "data_send",
        7: "set_encryption_key",
        8: "transfer_key"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=72)

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
        elif attr_type == "Enum":
            return self.setRequest(attr_id, dec_toHexStr(data, 2), "Enum", data)

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

    # Attribute of mbus_port_reference
    @formatResponse
    def get_mbus_port_reference(self, dataType=False, response=None):
        """
        获取 mbus_port_reference 的值

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
    def check_mbus_port_reference(self, ck_data):
        """
        检查 mbus_port_reference 的值

        :param ck_data:        点分十进制形式的OBIS值
        :return:               KFResult对象
        """
        ret = self.get_mbus_port_reference()
        if isinstance(ck_data, dict):
            for value in ck_data.values():
                if ret.lower() == str(value).lower().strip():
                    return KFResult(True, "")
            return KFResult(False, f"{ret} not equal to {ck_data}")
        else:
            if ret.lower() in str(ck_data).strip().lower():
                return KFResult(True, "")
            return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_mbus_port_reference(self, data):
        """
        设置 mbus_port_reference 的值

        :param data:           点分十进制形式的OBIS值
        :return:               KFResult对象
        """
        if isinstance(data, dict):
            data = data.get(0)
        return self.setRequest(2, obis_toHex(data), "OctetString")

    # Attribute of capture_definition
    @formatResponse
    def get_capture_definition(self, dataType=False, response=None):
        """
        获取 capture_definition 的值

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
                value[index] = hex_toOBIS(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_capture_definition(self, ck_data):
        """
        检查 capture_definition 的值

        :param ck_data:      字典
        :return:             KFResult对象

        ck_data数据格式：
        {
            0: ['0-0:10.0.106.255', '0-0:10.0.106.255'],
            1: ['0-0:10.0.106.255', '0-0:10.0.106.255']
        }
        """
        return checkResponsValue(self.get_capture_definition(), ck_data)

    @formatResponse
    def set_capture_definition(self, data):
        """
        设置 capture_definition 的值

        :param data:         字典
        :return:             KFResult对象

        data数据格式：
        {
            0: ['0-0:10.0.106.255', '0-0:10.0.106.255'],
            1: ['0-0:10.0.106.255', '0-0:10.0.106.255']
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
        return self.setRequest(3, array, "Array")

    # Attribute of capture_period
    @formatResponse
    def get_capture_period(self, dataType=False, response=None):
        """
        获取 capture_period 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(4, dataType=dataType, response=response)

    @formatResponse
    def check_capture_period(self, ck_data):
        """
        检查 capture_period 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 4)

    @formatResponse
    def set_capture_period(self, data):
        """
        设置 capture_period 的值

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.__set_attr(data, 4, "DoubleLongUnsigned")

    # Attribute of primary_address
    @formatResponse
    def get_primary_address(self, dataType=False, response=None):
        """
        获取 primary_address 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(5, dataType=dataType, response=response)

    @formatResponse
    def check_primary_address(self, ck_data):
        """
        检查 primary_address 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 5)

    @formatResponse
    def set_primary_address(self, data):
        """
        设置  primary_address 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.__set_attr(data, 5, "Unsigned")

    # Attribute of identification_number
    @formatResponse
    def get_identification_number(self, dataType=False, response=None):
        """
        获取 identification_number 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(6, dataType=dataType, response=response)

    @formatResponse
    def check_identification_number(self, ck_data):
        """
        检查 identification_number 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 6)

    @formatResponse
    def set_identification_number(self, data):
        """
        设置 identification_number 的值

        :param data:          十进制数
        :return:              KFResult对象
        """
        return self.__set_attr(data, 6, "DoubleLongUnsigned")

    # Attribute of manufacturer_id
    @formatResponse
    def get_manufacturer_id(self, dataType=False, response=None):
        """
        获取 manufacturer_id 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(7, dataType=dataType, response=response)

    @formatResponse
    def check_manufacturer_id(self, ck_data):
        """
        检查 manufacturer_id 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        return self.__check_attr(ck_data, 7)

    @formatResponse
    def set_manufacturer_id(self, data):
        """
        设置 manufacturer_id 的值

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.__set_attr(data, 7, "LongUnsigned")

    # Attribute of version
    @formatResponse
    def get_version(self, dataType=False, response=None):
        """
        获取 version 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(8, dataType=dataType, response=response)

    @formatResponse
    def check_version(self, ck_data):
        """
        检查 version 的值

        :param ck_data:       十进制数
        :return:              KFResult对象
        """
        return self.__check_attr(ck_data, 8)

    @formatResponse
    def set_version(self, data):
        """
        设置 version 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.__set_attr(data, 8, "Unsigned")

    # Attribute of device_type
    @formatResponse
    def get_device_type(self, dataType=False, response=None):
        """
        获取 device_type 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(9, dataType=dataType, response=response)

    @formatResponse
    def check_device_type(self, ck_data):
        """
        检查 device_type 的值

        :param ck_data:    十进制数
        :return:           KFResult对象
        """
        return self.__check_attr(ck_data, 9)

    @formatResponse
    def set_device_type(self, data):
        """
        设置 device_type 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 9, "Unsigned")

    # Attribute of access_number
    @formatResponse
    def get_access_number(self, dataType=False, response=None):
        """
        获取 access_number 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(10, dataType=dataType, response=response)

    @formatResponse
    def check_access_number(self, ck_data):
        """
        检查 access_number 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        return self.__check_attr(ck_data, 10)

    @formatResponse
    def set_access_number(self, data):
        """
        设置 access_number 的值

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.__set_attr(data, 10, "Unsigned")

    # Attribute of status
    @formatResponse
    def get_status(self, dataType=False, response=None):
        """
        获取 status 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(11, dataType=dataType, response=response)

    @formatResponse
    def check_status(self, ck_data):
        """
        检查 status 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        return self.__check_attr(ck_data, 11)

    @formatResponse
    def set_status(self, data):
        """
        设置 status 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.__set_attr(data, 11, "Unsigned")

    # Attribute of alarm
    @formatResponse
    def get_alarm(self, dataType=False, response=None):
        """
        获取 alarm 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(12, dataType=dataType, response=response)

    @formatResponse
    def check_alarm(self, ck_data):
        """
        检查 alarm 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        return self.__check_attr(ck_data, 12)

    @formatResponse
    def set_alarm(self, data):
        """
        设置 alarm 的值

        :param data:      十进制数
        :return:          KFResult对象
        """
        return self.__set_attr(data, 12, "Unsigned")

    # Attribute of configuration
    @formatResponse
    def get_configuration(self, dataType=False, response=None):
        """
        获取 configuration 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(13, dataType=dataType, response=response)

    @formatResponse
    def check_configuration(self, ck_data):
        """
        检查 configuration 的值

        :param ck_data:       十进制数
        :return:              KFResult对象
        """
        return self.__check_attr(ck_data, 13)

    @formatResponse
    def set_configuration(self, data):
        """
        设置 configuration 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 13, "LongUnsigned")

    # Attribute of encryption_key_status
    @formatResponse
    def get_encryption_key_status(self, dataType=False, response=None):
        """
        获取 encryption_key_status 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        return self.__get_attr(14, dataType=dataType, response=response)

    @formatResponse
    def check_encryption_key_status(self, ck_data):
        """
        检查 encryption_key_status 的值

        :param ck_data:   十进制数
        :return:          KFResult对象
        """
        return self.__check_attr(ck_data, 14)

    @formatResponse
    def set_encryption_key_status(self, data):
        """
        设置 encryption_key_status 的值

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.__set_attr(data, 14, "Enum")

    # Method of slave_install
    @formatResponse
    def act_slave_install(self, data=0):
        """
        Installs a slave device, which is yet unconfigured (its primary address is 0).

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Unsigned", data)

    # Method of slave_deinstall
    @formatResponse
    def act_slave_deinstall(self, data=0):
        """
        De-installs the slave device. The main purpose of this service is to de-install the
        M-Bus slave device and to prepare the master for the installation of a new device.

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(2, dec_toHexStr(data, 2), "Integer", data)

    # Method of capture
    @formatResponse
    def act_capture(self, data=0):
        """
        Captures values – as specified by the capture_definition attribute – from the M-Bus slave device.

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(3, dec_toHexStr(data, 2), "Integer", data)

    # Method of reset_alarm
    @formatResponse
    def act_reset_alarm(self, data=0):
        """
        Resets alarm state of the M-Bus slave device.

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(4, dec_toHexStr(data, 2), "Integer", data)

    # Method of synchronize_clock
    @formatResponse
    def act_synchronize_clock(self, data=0):
        """
        Synchronize the clock of the M-Bus slave device with that of the M-Bus client device

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(5, dec_toHexStr(data, 2), "Integer", data)

    # Method of data_send
    @formatResponse
    def act_data_send(self, data=None):
        """
        Sends data to the M-Bus slave device.

        :param data:  接收一个字典参数
        {
            0: ['0-0:10.0.106.255', '0-0:10.0.106.255', "NullData"]
        }
        :return:        KFResult对象
        """

        if data is None:
            data = {}
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex in [0, 1]:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                else:
                    # Choice 元素，需要对每种类型做判断
                    # etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                    etree.SubElement(struct, "NullData")
        return self.actionRequest(6, array, "Array", data)

    # Method of set_encryption_key
    @formatResponse
    def act_set_encryption_key(self, data=""):
        """
        Sets the encryption key in the M-Bus client and enables encrypted
        communication with the M-Bus slave device.

        :param data:    字符串
        :return:        KFResult对象
        """
        return self.actionRequest(7, data, "OctetString", data)

    # Method of transfer_key
    @formatResponse
    def act_transfer_key(self, data=""):
        """
        Transfers an encryption key to the M-Bus slave device.

        :param data:    字符串
        :return:        KFResult对象
        """
        return self.actionRequest(8, data, "OctetString", data)
