# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C9Script(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "scripts"
    }

    action_index_dict = {
        1: "execute"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=9)

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

    # Attribute of scripts (No.2)
    @formatResponse
    def get_scripts(self, dataType=False, response=None):
        """
        获取 scripts 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
        """
        if response is None:
            response = self.getRequest(2)

        response = getStrucDataFromGetResp(response)
        if isinstance(response[0], dict):
            for value in response[0].values():
                value[0] = hex_toDec(value[0])  # script_identifier
                for item in value[1]:
                    for subIndex, subItem in enumerate(item):
                        if subIndex == 0 and len(subItem) > 0:
                            item[subIndex] = hex_toDec(subItem)  # service_id
                        if subIndex == 1 and len(subItem) > 0:
                            item[subIndex] = hex_toDec(subItem)  # class_id
                        if subIndex == 2 and len(subItem) > 0:
                            item[subIndex] = hex_toOBIS(subItem)  # logical_name
                        if subIndex == 3 and len(subItem) > 0:
                            item[subIndex] = hex_toDec(subItem)  # index
                        if subIndex == 4 and len(subItem) > 0:
                            if subItem != 'NullData':
                                item[subIndex] = hex_toDec(subItem)  # parameter
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_scripts(self, ck_data):
        """
        检查 scripts 的值

        :param ck_data:     期望值 (字典)
        :return:            KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [1, [[2, 40, '0-1:25.9.0.255', 1, 0]]]
        }
        """
        return checkResponsValue(self.get_scripts(), ck_data)

    @formatResponse
    def set_scripts(self, data):
        """
         设置 scripts 的值

        :param data:       接收一个字典参数
        :return:           KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [1, [[2, 40, '0-1:25.9.0.255', 1, 0]]]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0 and isinstance(item, int):
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                if index == 1 and isinstance(item, list):
                    subArray = etree.SubElement(struct, "Array")
                    subArray.set("Qty", dec_toHexStr(len(item), 4))
                    for subIndex, subitem in enumerate(item):
                        subStruct = etree.SubElement(subArray, "Structure")
                        subStruct.set("Qty", dec_toHexStr(len(subitem), 4))
                        for sub2Index, sub2Item in enumerate(subitem):
                            if sub2Index == 0:
                                etree.SubElement(subStruct, "Enum").set("Value", dec_toHexStr(sub2Item, 2))
                            if sub2Index == 1:
                                etree.SubElement(subStruct, "LongUnsigned").set("Value", dec_toHexStr(sub2Item, 4))
                            if sub2Index == 2:
                                etree.SubElement(subStruct, "OctetString").set("Value", obis_toHex(sub2Item))
                            if sub2Index == 3:
                                etree.SubElement(subStruct, "Integer").set("Value", dec_toHexStr(sub2Item, 2))
                            if sub2Index == 4:
                                if sub2Item != 'NullData':
                                    etree.SubElement(subStruct, "OctetString").set("Value", dec_toHexStr(sub2Item, 2))
                                else:
                                    etree.SubElement(subStruct, "NullData")
        return self.setRequest(2, array, "Array", data)

    # Method of execute (No.1)
    @formatResponse
    def act_execute(self, index=1):
        """
        Executes the script specified in parameter data.

        :param index:                十进制数
        :return:                     返回一个KFResult对象
        """
        return self.actionRequest(1, dec_toHexStr(index, 4), "LongUnsigned", index)
