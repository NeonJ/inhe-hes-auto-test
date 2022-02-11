# -*- coding: UTF-8 -*-

from libs.Singleton import Singleton
from projects.camel.comm import setMPCValue

from dlms.DlmsClass import *


class C1Data(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "value"
    }

    data_access_result = ["ReadWriteDenied", "ObjectUndefined", "OtherReason", "DataBlockNumberInvalid",
                          "TypeUnmatched", "NoLongSetInProgress", "LongSetAborted", "NoLongGetInProgress",
                          "LongGetAborted", "DataBlockUnavailable", "ScopeOfAccessViolated", "ObjectUnavailable",
                          "ObjectClassInconsistent", "TemporaryFailure", "HardwareFault"]

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=1)

    # Attribute of logical_name (No .1)
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

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toOBIS(response[0]), response[1]
        return hex_toOBIS(response[0])

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
        return self.setRequest(1, obis_toHex(data), "OctetString")

    # Attribute of value (No.2)
    @formatResponse
    def get_value(self, obis=None, dataType=False, response=None):
        """
        获取 value 的值

        :param obis:        获取指定obis的值
        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回各种数据格式的value值
        """
        obis = obis if obis is not None else self.obisList[0]
        self.obis = obis

        if response is None:
            # self.showMethodInfo(method='Get', classId=self.__class__.__name__, obis=self.obis, attrId="2 - value")
            response = self.getRequestWithObis(2, obis)

        attributeType = getClassAttributeType(self.classId, obis, Singleton().Project)
        if not attributeType:
            ret = getSingleDataFromGetResp(response)
            if dataType:
                return ret
            return ret[0]

        # 有多种格式struct
        if attributeType.find("st_") != -1 or attributeType.find("a_") != -1:  # Structure / Array
            ret = getStrucDataFromGetResp(response)
            for value in ret[0].values():
                for index, item in enumerate(value):
                    if len(str(item)) < 12:
                        value[index] = hex_toDec(item)
            if dataType:
                return ret
            return ret[0]
        if attributeType.find("as_") != -1:
            response = getStrucDataFromGetResp(response)
            if response[0] in data_access_result:
                if dataType:
                    return response
            for value in response[0].values():
                for index, item in enumerate(value):
                    if index == 1 and len(item) > 0:
                        value[index] = hex_toOBIS(item)
                    else:
                        if item == "":
                            value[index] = ""
                        else:
                            value[index] = hex_toDec(item)
            if dataType:
                return response
            return response[0]
        else:
            ret = getSingleDataFromGetResp(response)
            if ret[0] in data_access_result:
                if dataType:
                    return ret
                return ret[0]

        if len(ret[0]) == 0:
            if dataType:
                return ret
            return ret[0]

        if attributeType == "h":  # Time
            if dataType:
                return hex_toTimeString(ret[0]), ret[1]
            return hex_toTimeString(ret[0])
        elif attributeType == "y":  # Date
            if dataType:
                return hex_toDateString(ret[0]), ret[1]
            return hex_toDateString(ret[0])
        elif attributeType == "t":  # DateTime
            if dataType:
                return hex_toDateTimeString(ret[0]), ret[1]
            return hex_toDateTimeString(ret[0])
        elif attributeType == "s":  # ASCII
            if dataType:
                return hex_toAscii(ret[0]), ret[1]
            return hex_toAscii(ret[0])
        # Decimal, Enum, Bool,Unsigned, LongUnsigned, DoubleLongUnsigned
        elif attributeType in ["d", "e", "b", "u", "lu", "dlu"]:
            if dataType:
                return hex_toDec(ret[0]), ret[1]
            return hex_toDec(ret[0])

        else:
            if dataType:
                return ret
            return ret[0]

    @formatResponse
    def check_value(self, ck_data):
        """
        检查 value 的值

        :param ck_data:     期望值 (Time/Date/DateTime/ASCII/Decimal)
        :return:            KFResult 对象
        """
        ret = self.get_value()
        attributeType = getClassAttributeType(self.classId, self.obis, Singleton().Project)
        if not attributeType:
            if str(ret).lower() == str(ck_data).lower():
                return KFResult(True, "")
            return KFResult(False, f"{ret} not equal to {ck_data}")
        elif attributeType.find("st_") != -1 or attributeType.find("a_") != -1:  # Structure/ Array
            return checkResponsValue(ret, ck_data)
        else:
            if str(ret).lower() == str(ck_data).lower():
                return KFResult(True, "")
            return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_value(self, data, isDownloadMode=True):
        """
        设置 logical_name 的值

        :param data:                    期望值 (Time/Date/DateTime/ASCII/Decimal)
        :param isDownloadMode:
        :return:                        返回一个KFResult对象
        """

        if isDownloadMode:
            if self.obis == '0-96:15.128.0.255':
                value = {"meterReadingParameter": data}
                return setMPCValue(self.conn, mpcMap=value)
            if self.obis == '0-0:21.0.1.255':
                value = {"normalDisplay": data}
                return setMPCValue(self.conn, mpcMap=value)
            if self.obis == '0-0:21.0.2.255':
                value = {"testDisplay": data}
                return setMPCValue(self.conn, mpcMap=value)
            if self.obis == '0-96:94.96.8.255':
                value = {"controlSignals": data}
                return setMPCValue(self.conn, mpcMap=value)
            if self.obis == '0-96:94.96.10.255':
                value = {"autoRecoveryTimes": data}
                return setMPCValue(self.conn, mpcMap=value)

        attributeType = getClassAttributeType(self.classId, self.obis, Singleton().Project)
        if not attributeType:
            return self.setRequest(2, data, "OctetString")
        if attributeType.find("st_") != -1:  # Structure
            lst = attributeType.split("_")[1:]
            if len(data) > 1:
                struct = etree.Element("Structure")
                struct.set("Qty", dec_toHexStr(len(data), 4))
                for value in data.values():
                    subStruct = etree.SubElement(struct, "Structure")
                    subStruct.set("Qty", dec_toHexStr(len(value), 4))
                    for index, item in enumerate(value):
                        typeMode = int(lst.pop(0))
                        if typeMode == 3:
                            etree.SubElement(subStruct, "Bool").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 4:
                            etree.SubElement(subStruct, "BitString").set("Value", item)
                        elif typeMode == 17:
                            etree.SubElement(subStruct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 18:
                            etree.SubElement(subStruct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                        elif typeMode == 22:
                            etree.SubElement(subStruct, "Enum").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 15:
                            etree.SubElement(subStruct, "Integer").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 9:
                            etree.SubElement(subStruct, "OctetString").set("Value", item)
                        elif typeMode == 4:
                            etree.SubElement(subStruct, "BitString").set("Value", item)
                        elif typeMode == 6:
                            etree.SubElement(subStruct, "DoubleLongUnsigned").set("Value", dec_toHexStr(item, 8))
            else:
                struct = etree.Element("Structure")
                struct.set("Qty", dec_toHexStr(len(lst), 4))
                for value in data.values():
                    for index, item in enumerate(value):
                        typeMode = int(lst.pop(0))
                        if typeMode == 3:
                            etree.SubElement(struct, "Bool").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 4:
                            etree.SubElement(struct, "BitString").set("Value", item)
                        elif typeMode == 17:
                            etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 18:
                            etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                        elif typeMode == 22:
                            etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 15:
                            etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(item, 2))
                        elif typeMode == 9:
                            etree.SubElement(struct, "OctetString").set("Value", item)
                        elif typeMode == 6:
                            etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(item, 8))
            return self.setRequest(2, struct, "Struct")

        elif attributeType.find("a_") != -1:  # Array
            array = etree.Element("Array")
            array.set("Qty", dec_toHexStr(len(data), 4))

            lst = attributeType.split("_")[1:]
            for index, item in enumerate(list(data.values())):
                typeMode = int(lst.pop(0))
                if typeMode == 3:
                    etree.SubElement(array, "Bool").set("Value", dec_toHexStr(item, 2))
                elif typeMode == 4:
                    etree.SubElement(array, "BitString").set("Value", item)
                elif typeMode == 6:
                    etree.SubElement(array, "DoubleLongUnsigned").set("Value", dec_toHexStr(item, 8))
                elif typeMode == 17:
                    etree.SubElement(array, "Unsigned").set("Value", dec_toHexStr(item, 2))
                elif typeMode == 18:
                    etree.SubElement(array, "LongUnsigned").set("Value", dec_toHexStr(item, 4))
                elif typeMode == 22:
                    etree.SubElement(array, "Enum").set("Value", dec_toHexStr(item, 2))
                elif typeMode == 15:
                    etree.SubElement(array, "Integer").set("Value", dec_toHexStr(item, 2))
                elif typeMode == 9:
                    etree.SubElement(array, "OctetString").set("Value", item)

            return self.setRequest(2, array, "Array")

        elif attributeType.find("as_") != -1:  # Array Structure
            if data is None or len(data) == 0:
                array = etree.Element("Array")
                array.set("Qty", "0000")
                return self.setRequest(2, array, "Array")

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
                    if subIndex == 2:
                        etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
                    if subIndex == 3:
                        if subItem == "":
                            etree.SubElement(struct, "OctetString").set("Value", "")
                        else:
                            etree.SubElement(struct, "OctetString").set("Value", dec_toHexStr(subItem))
            return self.setRequest(2, array, "Array")

        elif attributeType == "h":  # Time
            ret = time_toHex(data)
        elif attributeType == "y":  # Date
            ret = date_toHex(data)
        elif attributeType == "t":  # DateTime
            ret = dateTime_toHex(data[:19])
            print(ret)
        elif attributeType == "s":  # ASCII
            ret = ascii_toHex(data)
        elif attributeType == "vs":  # ASCII
            return self.setRequest(2, str(data), "VisibleString")
        elif attributeType == "b":  # Bool
            return self.setRequest(2, dec_toHexStr(data, 2), "Bool")
        elif attributeType == "e":  # Enum
            return self.setRequest(2, dec_toHexStr(data, 2), "Enum")
        elif attributeType == "dlu":  # DoubleLongUnsigned
            return self.setRequest(2, dec_toHexStr(data, 8), "DoubleLongUnsigned")
        elif attributeType == "lu":  # LongUnsigned
            return self.setRequest(2, dec_toHexStr(data, 4), "LongUnsigned")
        elif attributeType == "u":  # Unsigned
            return self.setRequest(2, dec_toHexStr(data, 2), "Unsigned")
        elif attributeType.find("stl_") != -1:  # Structure
            lst = attributeType.split("_")[1:]
            struct = etree.Element("Structure")
            struct.set("Qty", dec_toHexStr(len(data), 4))
            for value in data.values():
                for index, item in enumerate(value):
                    typeMode = int(lst.pop(0))
                    if typeMode == 22:
                        etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(item, 2))
                    elif typeMode == 4:
                        etree.SubElement(struct, "BitString").set("Value", item)
            return self.setRequest(2, struct, "Struct")
        else:
            ret = str(data)
        return self.setRequest(2, ret, "OctetString")

    # ==================================================================================================#

    @formatResponse
    def get_value_with_list(self):
        """
        批量获取 class 1 的value值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            response[index] = self.get_value(obis)
        return response

    @formatResponse
    def check_value_with_list(self, ck_data, increment=None):
        """
        批量检查 class 1 的value值

        :param ck_data:       期望值(列表)
        :param increment:     增量（ck_data中每个值对应的增量）
        :return:              返回一个KFResult对象
        """
        response = list()
        result = self.get_value_with_list()
        if increment is None:
            increment = [0 for _ in range(len(result))]

        try:
            for key, value in ck_data.items():
                if int(value) + increment[key] != int(result[key]):
                    response.append(
                        f"'response[{key}]={result[key]}'not equal to 'ck_data[{key}]={value}' + {increment[key]} ")
            if len(response) == 0:
                return KFResult(True, '')
            else:
                return KFResult(False, "; ".join(response))
        except Exception as ex:
            error(ex)
