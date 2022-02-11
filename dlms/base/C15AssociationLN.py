# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C15AssociationLN(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "object_list",
        3: "associated_partners_id",
        4: "application_context_name",
        5: "xdlms_context_info",
        6: "authentication_mechanism_name",
        7: "secret",
        8: "association_status",
        9: "security_setup_reference",
        10: "user_list",
        11: "current_user"
    }

    action_index_dict = {
        1: "reply_to_hls_authentication",
        2: "change_hls_secret",
        3: "add_object",
        4: "remove_object",
        5: "add_user",
        6: "remove_user"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=15)

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

    # Attribute of object_list
    @formatResponse
    def get_object_list(self, dataType=False, response=None):
        """
        获取 object_list 的值

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
                if index in [0, 1] and len(item) > 0:
                    value[index] = hex_toDec(item)  # class_id, version
                elif index == 2 and len(item) > 0:
                    value[index] = hex_toOBIS(item)  # logical_name
                elif isinstance(item, list):
                    if len(item[0]) > 0:
                        for subValue in item[0]:
                            for subIndex, subItem in enumerate(subValue):
                                if subIndex == 0 and len(subItem) > 0:
                                    subValue[subIndex] = hex_toDec(subItem)  # attribute_id
                                if subIndex == 1 and len(subItem) > 0:
                                    subValue[subIndex] = hex_toDec(subItem)  # access_mode
                                if subIndex == 2:
                                    if isinstance(subItem, list):
                                        for sub2Index, sub2Item in enumerate(subItem):
                                            subValue[subIndex][sub2Index] = hex_toDec(sub2Item)
                                    if subItem == "NullData":
                                        subValue[subIndex] = "NullData"
                    if len(item[1]) > 0:
                        for subValue in item[1]:
                            for subIndex, subItem in enumerate(subValue):
                                if subIndex == 0 and len(subItem) > 0:
                                    subValue[subIndex] = hex_toDec(subItem)
                                if subIndex == 1 and len(subItem) > 0:
                                    subValue[subIndex] = hex_toDec(subItem)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_object_list(self, ck_data):
        """
        检查 object_list 的值

        :param ck_data:     期望值 (字典)
        :return:            KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [1, 0, '0-0:0.1.0.255', [[[1, 1, 'NullData'], [2, 1, 'NullData']], []]]
        }
        """
        return checkResponsValue(self.get_object_list(), ck_data)

    @formatResponse
    def set_object_list(self, data):
        """
        设置 object_list 的值

        :param data:        期望值 (字典)
        :return:            KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [1, 0, '0-0:0.1.0.255', [[[1, 1, 'NullData'], [2, 1, 'NullData']], []]]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data)))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                elif index == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                elif index == 2:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(item))
                elif index == 3:
                    subStruct = etree.SubElement(struct, "Structure")
                    subStruct.set("Qty", dec_toHexStr(len(item), 4))
                    for subValue in item:
                        subArray = etree.SubElement(subStruct, "Array")
                        subArray.set("Qty", dec_toHexStr(len(subValue), 4))
                        for subIndex, subItem in enumerate(subValue):
                            sub2Struct = etree.SubElement(subArray, "Structure")
                            sub2Struct.set("Qty", dec_toHexStr(len(subItem), 4))
                            for sub2Index, sub2Item in enumerate(subItem):
                                if sub2Index == 0:
                                    etree.SubElement(sub2Struct, "Integer").set("Value", dec_toHexStr(sub2Item, 2))
                                elif sub2Index == 1:
                                    etree.SubElement(sub2Struct, "Enum").set("Value", dec_toHexStr(sub2Item, 2))
                                elif sub2Index == 2:
                                    if isinstance(sub2Item, list):
                                        sub2Array = etree.SubElement(sub2Struct, "Array")
                                        sub2Array.set("Qty", dec_toHexStr(len(subItem), 4))
                                        for sub3Index, sub3Item in enumerate(subItem):
                                            etree.SubElement(sub2Array, "Integer").set("Value",
                                                                                       dec_toHexStr(sub3Item, 2))
                                    elif sub2Item == "NullData":
                                        etree.SubElement(sub2Struct, "NullData")
        return self.setRequest(2, array, "Array", data)

    # Attribute of associated_partners_id
    @formatResponse
    def get_associated_partners_id(self, dataType=False, response=None):
        """
        获取 associated_partners_id 的值

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
    def check_associated_partners_id(self, ck_data):
        """
        检查 associated_partners_id 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
             0: [1, 1]
        }
        """
        return checkResponsValue(self.get_associated_partners_id(), ck_data)

    @formatResponse
    def set_associated_partners_id(self, data):
        """
        检查 associated_partners_id 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
             0: [1, 1]
        }
        """
        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(len(data[0]), 4))
        for index, item in enumerate(data[0]):
            if index == 0:
                etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(item, 2))
            if index == 1:
                etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
        return self.setRequest(3, struct, "struct", data)

    # Attribute of application_context_name
    @formatResponse
    def get_application_context_name(self, dataType=False, response=None):
        """
        获取 application_context_name 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(4)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_application_context_name(self, ck_data):
        """
        检查 application_context_name 的值

        :param ck_data:    字符串（"60857405080103"）
        :return:           KFResult对象
        """
        ret = self.get_application_context_name()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_application_context_name(self, data):
        """
        设置 application_context_name 的值

        :param data:       字符串（"60857405080103"）
        :return:           KFResult对象
        """
        return self.setRequest(4, data, "OctetString", data)

    # Attribute of xDLMS_context_info
    @formatResponse
    def get_xdlms_context_info(self, dataType=None, response=None):
        """
        获取 xDLMS_context_info 的值

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
                if index in [1, 2, 3, 4]:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_xdlms_context_info(self, ck_data):
        """
        检查 xDLMS_context_info 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['010000000001101000011101', 1224, 1224, 6, 0, '']
        }
        """
        return checkResponsValue(self.get_xdlms_context_info(), ck_data)

    @formatResponse
    def set_xdlms_context_info(self, data):
        """
        设置 xDLMS_context_info 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['010000000001101000011101', 1224, 1224, 6, 0, '']
        }
        """
        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(len(data[0]), 4))
        for index, item in enumerate(data[0]):
            if index == 0:
                etree.SubElement(struct, "BitString").set("Value", item)
            if index == 1 or index == 2:
                etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
            if index == 3:
                etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
            if index == 4:
                etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(item, 2))
            if index == 5:
                etree.SubElement(struct, "OctetString").set("Value", item)
        return self.setRequest(5, struct, "struct", data)

    # Attribute of authentication_mechanism_name
    @formatResponse
    def get_authentication_mechanism_name(self, dataType=False, response=None):
        """
        获取 authentication_mechanism_name 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(6)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_authentication_mechanism_name(self, ck_data):
        """
        检查 authentication_mechanism_name 的值

        :param ck_data:    字符串（"60857405080206"）
        :return:           KFResult对象
        """
        ret = self.get_authentication_mechanism_name()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_authentication_mechanism_name(self, data):
        """
        检查 authentication_mechanism_name 的值

        :param data:       字符串（"60857405080206"）
        :return:           KFResult对象
        """
        return self.setRequest(6, data, "OctetString", data)

    # Attribute of secret
    @formatResponse
    def get_secret(self, dataType=False, response=None):
        """
        获取 secret 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(7)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_secret(self, ck_data):
        """
        检查 secret 的值

        :param ck_data:     字符串
        :return:            KFResult对象
        """

        ret = self.get_secret()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_secret(self, data):
        """
        设置 secret 的值

        :param data:        字符串
        :return:            KFResult对象
        """
        return self.setRequest(7, ascii_toHex(data), "OctetString", data)

    # Attribute of association_status
    @formatResponse
    def get_association_status(self, dataType=False, response=None):
        """
        获取 association_status 的值

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
    def check_association_status(self, ck_data):
        """
        检查 association_status 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """

        ret = self.get_association_status()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_association_status(self, data):
        """
        设置 association_status 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(8, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of security_setup_reference
    @formatResponse
    def get_security_setup_reference(self, dataType=False, response=None):
        """
        获取 security_setup_reference 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            点分十进制形式的OBIS值
        """
        if response is None:
            response = self.getRequest(9)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toOBIS(ret[0]), ret[1]
        return hex_toOBIS(ret[0])

    @formatResponse
    def check_security_setup_reference(self, ck_data):
        """
        检查 security_setup_reference 的值

        :param ck_data:     点分十进制形式的OBIS值
        :return:            KFResult对象
        """
        ret = self.get_security_setup_reference()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_security_setup_reference(self, data):
        """
        设置 security_setup_reference 的值

        :param data:        点分十进制形式的OBIS值
        :return:            KFResult对象
        """
        return self.setRequest(9, obis_toHex(data), "OctetString", data)

    # Attribute of user_list
    @formatResponse
    def get_user_list(self, dataType=False, response=None):
        """
        获取 user_list 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(10)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_user_list(self, ck_data):
        """
        检查 user_list 的值

        :param ck_data:            接收一个字典参数
        :return                    返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [2, "144514"]
        }
        """
        checkResponsValue(self.get_user_list(), ck_data)

    @formatResponse
    def set_user_list(self, data):
        """
        设置 user_list 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [2, "144514"]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values())))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value)))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                else:
                    etree.SubElement(struct, "VisibleString").set("Value", item)
        return self.setRequest(10, array, "Array", data)

    # Attribute of current_user
    @formatResponse
    def get_current_user(self, dataType=False, response=None):
        """
        获取 current_user 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(11)

        ret = getStrucDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_current_user(self, ck_data):
        """
        检查 current_user 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [2, "144514"]
        }
        """
        return checkResponsValue(self.get_current_user(), ck_data)

    @formatResponse
    def set_current_user(self, data):
        """
        设置 current_user 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [2, "144514"]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value)))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                else:
                    etree.SubElement(struct, "VisibleString").set("Value", item)
        return self.setRequest(11, struct, "Struct", data)

    # Method of reply_to_HLS_authentication
    @formatResponse
    def act_reply_to_hls_authentication(self, data=""):
        """
        The remote invocation of this method delivers to the server the result of the secret processing
        by the client of the server’s challenge to the client, f(StoC), as the data service parameter
        of the ACTION.request primitive invoked.

        :param data:         字符串
        :return              KFResult 对象
        """
        return self.actionRequest(1, data, "OctetString", data)

    # Method of change_HLS_secret
    @formatResponse
    def act_change_hls_secret(self, data=""):
        """
        Changes the HLS secret (for example encryption key)

        :param data:         字符串
        :return              KFResult 对象
        """
        return self.actionRequest(2, data, "OctetString", data)

    # Method of add_object
    @formatResponse
    def act_add_object(self, data=None):
        """
        Adds the referenced object to the object_list.

        :param data:         字典
        :return              KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['3100', '00', '00002B0107FF', ['01', '01', 'NullData'], ['01', '01']]
        }

        """
        if data is None:
            data = {}
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                elif index == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                elif index == 2:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(item))
                elif index == 3:
                    subStruct = etree.SubElement(struct, "Structure")
                    subStruct.set("Qty", dec_toHexStr(len(item)))
                    for subIndex, subItem in enumerate(item):
                        if subIndex == 0:
                            etree.SubElement(subStruct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                        elif subIndex == 1:
                            etree.SubElement(subStruct, "Enum").set("Value", dec_toHexStr(subItem, 2))
                        elif subIndex == 2:
                            if subItem == "NullData":
                                etree.SubElement(subStruct, "NullData")
        return self.actionRequest(3, array, "Array", data)

    # Method of remove_object
    @formatResponse
    def act_remove_object(self, data=None):
        """
        Removes the referenced object from the object_list.

        :param data:         字典
        :return              KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['3100', '00', '00002B0107FF', ['01', '01', 'NullData'], ['01', '01']]
        }
        """
        if data is None:
            data = {}
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                elif index == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                elif index == 2:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(item))
                elif index == 3:
                    subStruct = etree.SubElement(struct, "Structure")
                    subStruct.set("Qty", dec_toHexStr(len(item)))
                    for subIndex, subItem in enumerate(item):
                        if subIndex == 0:
                            etree.SubElement(subStruct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                        elif subIndex == 1:
                            etree.SubElement(subStruct, "Enum").set("Value", dec_toHexStr(subItem, 2))
                        elif subIndex == 2:
                            if subItem == "NullData":
                                etree.SubElement(subStruct, "NullData")
        return self.actionRequest(4, array, "Array", data)

    # Method of add_user
    @formatResponse
    def act_add_user(self, data):
        """
        Adds a user to the user_list.

        :param data:         字典
        :return              KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [2, "144514"]
        }
        """
        struct = etree.Element("Structure")
        if len(data) == 0:
            struct.set("Qty", dec_toHexStr(0, 4))
        else:
            for value in data.values():
                struct.set("Qty", dec_toHexStr(len(value), 4))
                for index, item in enumerate(value):
                    if index == 0:
                        etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                    else:
                        etree.SubElement(struct, "VisibleString").set("Value", item)
        return self.actionRequest(5, struct, "structure", data)

    # Method of remove_user
    @formatResponse
    def act_remove_user(self, data):
        """
        Removes a user from the user_list.

        :param data:         字典
        :return              KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [2, "144514"]
        }
        """
        struct = etree.Element("Structure")
        if len(data) == 0:
            struct.set("Qty", dec_toHexStr(0, 4))
        else:
            for value in data.values():
                struct.set("Qty", dec_toHexStr(len(value), 4))
                for index, item in enumerate(value):
                    if index == 0:
                        etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                    else:
                        etree.SubElement(struct, "VisibleString").set("Value", item)
        return self.actionRequest(6, struct, "structure", data)
