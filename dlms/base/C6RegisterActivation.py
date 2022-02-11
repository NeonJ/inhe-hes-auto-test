# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C6RegisterActivation(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "register_assignment",
        3: "mask_list",
        4: "active_mask"
    }

    action_index_dict = {
        1: "add_register",
        2: "add_mask",
        3: "delete_mask"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=6)

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
            return hex_toOBIS(ret[0]), ret
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

    # Attribute of register_assignment (No.2)
    @formatResponse
    def get_register_assignment(self, dataType=False, response=None):
        """
        获取 register_assignment 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
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
                if index == 1 and len(item) > 0:
                    value[index] = hex_toOBIS(item)
                else:
                    value[index] = hex_toDec(item)

        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_register_assignment(self, ck_data):
        """
        检查 register assignment 的值

        :param ck_data:               期望值 (一个字典)
        :return                       返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [3, '1-0:1.8.1.255'],
            1 : [3, '1-0:1.8.2.255'],
            2 : [3, '1-0:2.8.1.255'],
            3 : [3, '1-0:2.8.2.255']
        }
        """
        # 处理OBIS对象的格式
        for value in ck_data.values():
            value[1].replace("-", ".").replace(":", ".")
        return checkResponsValue(self.get_register_assignment(), ck_data)

    @formatResponse
    def set_register_assignment(self, data):
        """
        设置 register assignment 的值

        :param data:                  期望值 (一个字典)
        :return                       返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [3, '1-0:1.8.1.255'],
            1 : [3, '1-0:1.8.2.255'],
            2 : [3, '1-0:2.8.1.255'],
            3 : [3, '1-0:2.8.2.255']
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
                if subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
        return self.setRequest(2, array, "Array", data)

    # Attribute of mask_list (No.3)
    @formatResponse
    def get_mask_list(self, dataType=None, response=None):
        """
        获取 mask_list 的值
        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个字典
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
                if index == 0:
                    value[index] = hex_toAscii(item)
                if index == 1 and len(item) > 0:
                    for i in range(len(item)):
                        item[i] = hex_toDec(item[i])

        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_mask_list(self, ck_data):
        """
        检查 mask_list 的值

        :param ck_data:               期望值 (一个字典)
        :return                       返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['5431', [1, 3, 5, 7]],
            1: ['5432', [2, 4, 6, 8]]
        }
        """
        return checkResponsValue(self.get_mask_list(), ck_data)

    @formatResponse
    def set_mask_list(self, data):
        """
        设置 mask_list 的值

        :param data:               期望值 (一个字典)
        :return                    返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['5431', [1, 3, 5, 7]],
            1: ['5432', [2, 4, 6, 8]]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                if subIndex == 1:
                    sub_array = etree.SubElement(struct, "Array")
                    sub_array.set("Qty", dec_toHexStr(len(subItem), 4))
                    for ele in subItem:
                        etree.SubElement(sub_array, "Unsigned").set("Value", dec_toHexStr(ele, 2))
        return self.setRequest(3, array, "Array", data)

    # Attribute of active_mask (No.4)
    @formatResponse
    def get_active_mask(self, dataType=None, response=None):
        """
        获取 active_mask 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个octet-string
        """
        if response is None:
            response = self.getRequest(4)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_active_mask(self, ck_data):
        """
        检查 active_mask 的值

        :param ck_data:          期望值（octet_string）
        :return:                 KFResult对象
        """
        ret = self.get_active_mask()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_active_mask(self, data):
        """
        设置 active_mask 的值

        :param data:              期望值（octet_string）
        :return:                  KFResult对象
        """
        return self.setRequest(4, data, "OctetString", data)

    # Method of add_register
    @formatResponse
    def act_add_register(self, data=None):
        """
        Adds one more registers to the attribute register_assignment. The new register is added
        at the end of the array; i.e. the newly added register has the highest index. The indices
        of the existing registers are not modified.

        :param data:            接收一个字典参数
        :return                 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [3, '1-0:1.8.1.255'],
            1: [3, '1-0:1.8.2.255'],
            2: [3, '1-0:2.8.1.255'],
            3: [3, '1-0:2.8.2.255']
        }
        """
        if data is None:
            data = {}

        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                if subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
        return self.actionRequest(1, array, "Array", data)

    # Method of add_mask
    @formatResponse
    def act_add_mask(self, data=None):
        """
        Adds another mask to the attribute mask_list. If there exists already a mask with the same name,
        the existing mask will be overwritten by the new mask.

        :param data:          接收一个字典参数
        :return               KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['5431', [1, 3, 5, 7]],
            1: ['5432', [2, 4, 6, 8]]
        }
        """
        if data is None:
            data = {}

        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                if subIndex == 1:
                    sub_array = etree.SubElement(struct, "Array")
                    sub_array.set("Qty", "0004")
                    for ele in subItem:
                        etree.SubElement(sub_array, "Unsigned").set("Value", dec_toHexStr(ele, 2))
        return self.actionRequest(2, array, "Array", data)

    # Method of delete_mask
    @formatResponse
    def act_delete_mask(self, data=""):
        """
        Deletes a mask from the attribute mask_list. The mask is defined by its mask name.

        :param data:       参数格式为: "5341"
        :return:               KFResult 对象
        """
        return self.actionRequest(3, data, "OctetString", data)
