# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C47GSMDiagnostic(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "operator",
        3: "status",
        4: "cs_attachment",
        5: "ps_status",
        6: "cell_info",
        7: "adjacent_cells",
        8: "capture_time"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=47)

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
        return self.setRequest(1, obis_toHex(data), "OctetString", data)

    # Attribute of operator
    @formatResponse
    def get_operator(self, dataType=False, response=None):
        """
        获取 operator 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_operator(self, ck_data):
        """
        检查 operator 的值

        :param ck_data:          字符串
        :return:                 KFResult对象
        """
        ret = self.get_operator()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_operator(self, data):
        """
        设置 operator 的值

        :param data:       字符串
        :return:           KFResult对象
        """
        return self.setRequest(2, data, "VisibleString", data)

    # Attribute of status
    @formatResponse
    def get_status(self, dataType=False, response=None):
        """
        获取 status 的值

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
    def check_status(self, ck_data):
        """
        检查 status 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        ret = self.get_status()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_status(self, data):
        """
        设置 status 的值

        :param data:         十进制数
        :return:             KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of cs_attachment
    @formatResponse
    def get_cs_attachment(self, dataType=False, response=None):
        """
        获取 cs_attachment 的值

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
    def check_cs_attachment(self, ck_data):
        """
        检查 cs_attachment 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        ret = self.get_cs_attachment()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_cs_attachment(self, data):
        """
        设置 cs_attachment 的值

        :param data:         十进制数
        :return:             KFResult对象
        """
        return self.setRequest(4, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of ps_status
    @formatResponse
    def get_ps_status(self, dataType=False, response=None):
        """
        获取 ps_status 的值

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
    def check_ps_status(self, ck_data):
        """
        检查 ps_status 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        ret = self.get_ps_status()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_ps_status(self, data):
        """
        设置 ps_status 的值

        :param data:         十进制数
        :return:             KFResult对象
        """
        return self.setRequest(5, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of cell_info
    @formatResponse
    def get_cell_info(self, dataType=False, response=None):
        """
        获取 cell_info 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(6)

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
    def check_cell_info(self, ck_data):
        """
        检查 cell_info 的值

        :param ck_data:      字典
        :return:             KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [8056, 33345, 18, 99]
        }
        """
        return checkResponsValue(self.get_cell_info(), ck_data)

    @formatResponse
    def set_cell_info(self, data):
        """
        检查 cell_info 的值

        :param data:         字典
        :return:             KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [8056, 33345, 18, 99]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(subItem, 8))
                elif subIndex == 1:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(6, struct, "Struct", data)

    # Attribute of adjacent_cells
    @formatResponse
    def get_adjacent_cells(self, dataType=False, response=None):
        """
        获取 adjacent_cells 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(7)

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
    def check_adjacent_cells(self, ck_data):
        """
        检查 adjacent_cells 的值

        :param ck_data:      字典
        :return:             KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [23063, 0],
            1: [30753, 99],
            2: [15013, 99],
            3: [31422, 0],
            4: [10413, 99],
            5: [22135, 99]
        }
        """
        return checkResponsValue(self.get_adjacent_cells(), ck_data)

    @formatResponse
    def set_adjacent_cells(self, data):
        """
        设置 adjacent_cells 的值

        :param data:         字典
        :return:             KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [23063, 0],
            1: [30753, 99],
            2: [15013, 99],
            3: [31422, 0],
            4: [10413, 99],
            5: [22135, 99]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data.values()), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(subItem, 8))
                elif subIndex == 1:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(7, array, "Array", data)

    # Attribute of capture_time
    @formatResponse
    def get_capture_time(self, dataType=False, response=None):
        """
        获取 capture_time 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(8)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDateTimeString(ret[0]), ret[1]
        return hex_toDateTimeString(ret[0])

    @formatResponse
    def check_capture_time(self, ck_data):
        """
        检查 capture_time 的值

        :param ck_data:      字符串
        :return:             KFResult对象
        """
        ret = self.get_capture_time()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_capture_time(self, data):
        """
        设置 capture_time 的值

        :param data:         字符串
        :return:             KFResult对象
        """
        return self.setRequest(8, dateTime_toHex(data), "OctetString", data)
