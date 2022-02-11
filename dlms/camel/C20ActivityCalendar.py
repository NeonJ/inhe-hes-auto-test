# -*- coding: UTF-8 -*-


from projects.camel.comm import setMPCValue

from dlms.DlmsClass import *


class C20ActivityCalendar(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "calendar_name_active",
        3: "season_profile_active",
        4: "week_profile_table_active",
        5: "day_profile_table_active",
        6: "calendar_name_passive",
        7: "season_profile_passive",
        8: "week_profile_table_passive",
        9: "day_profile_table_passive",
        10: "activate_passive_calendar_time"
    }

    action_index_dict = {
        1: "activate_passive_calendar"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=20)

    def __get_calendar_name(self, dataType, response, attrId):
        if response is None:
            response = self.getRequest(attrId)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:  # 需求改变，以前是返回ASCII码，现在直接返回字符串
            return ret
        return ret[0]

    def __get_season_profile(self, dataType, response, attrId):
        if response is None:
            response = self.getRequest(attrId)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                if index == 0 and len(item) > 0:
                    value[index] = item
                if index == 1 and len(item) > 0:
                    # value[index] = hex_toWildcardTimeString(item)[0]
                    value[index] = hex_toWildcardTimeString(item)
                if index == 2 and len(item) > 0:
                    value[index] = item
        if dataType:
            return response
        return response[0]

    def __set_season_profile(self, data, attrId):
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
                if subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", subItem.replace("-", ""))
                if subIndex == 2:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(attrId, array, 'Array', data)

    def __get_week_profile_table(self, dataType, response, attrId):
        if response is None:
            response = self.getRequest(attrId)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():
            for index, item in enumerate(value):
                if index != 0:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    def __set_week_profile_table(self, data, attrId):
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "OctetString").set("Value", str(subItem))
                else:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(subItem, 2))
        return self.setRequest(attrId, array, 'Array', data)

    def __get_day_profile_table(self, dataType, response, attrId):
        if response is None:
            response = self.getRequest(attrId)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():  # list: level2
            for index, item in enumerate(value):
                if isinstance(item, str):
                    value[index] = hex_toDec(item)
                if isinstance(item, list):
                    for subIndex, subItem in enumerate(item):  # list: level2
                        if isinstance(subItem, list):
                            for sub2Index, sub2Item in enumerate(subItem):  # list: level3
                                if sub2Index == 0 and len(sub2Item) > 0:
                                    subItem[sub2Index] = hex_toTimeString(sub2Item)  # start_time
                                if sub2Index == 1 and len(sub2Item) > 0:
                                    subItem[sub2Index] = hex_toOBIS(sub2Item)  # script_logical_name
                                if sub2Index == 2 and len(sub2Item) > 0:
                                    subItem[sub2Index] = hex_toDec(sub2Item)  # script_selector
        if dataType:
            return response
        return response[0]

    def __set_day_profile_table(self, data, attrId):
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Unsigned").set("Value", dec_toHexStr(value[index], 2))
                if index == 1:
                    subArray = etree.SubElement(struct, 'Array')
                    subArray.set("Qty", dec_toHexStr(len(value[index]), 4))
                    for subItem in value[index]:
                        subStruct = etree.SubElement(subArray, "Structure")
                        subStruct.set("Qty", dec_toHexStr(len(subItem), 4))
                        for sub2Index, sub2Item in enumerate(subItem):
                            if sub2Index == 0:
                                etree.SubElement(subStruct, "OctetString").set("Value",
                                                                               dayDateTime_toHex(sub2Item).ljust(8,
                                                                                                                 '0'))
                            if sub2Index == 1:
                                etree.SubElement(subStruct, "OctetString").set("Value", obis_toHex(sub2Item))
                            if sub2Index == 2:
                                etree.SubElement(subStruct, "LongUnsigned").set("Value", dec_toHexStr(sub2Item, 4))
        return self.setRequest(attrId, array, 'Array', data)

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

    # Attribute of calendar_name_active (No.2)
    @formatResponse
    def get_calendar_name_active(self, dataType=False, response=None):
        """
        获取属性 calendar_name_active 的值

        :param dataType:      是否返回数据类型， 默认False不返回
        :param response:      如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :param attr:          属性ID
        :return:              字符串
        """
        return self.__get_calendar_name(dataType, response, 2)

    @formatResponse
    def check_calendar_name_active(self, ck_data):
        """
        检查属性 calendar_name_active 的值

        :param ck_data:           字符串
        :param attr:              属性ID
        :return:                  KFResult对象
        """
        ret = self.get_calendar_name_active()
        if str(ret) == str(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_calendar_name_active(self, data):
        """
        设置属性 calendar_name_active 的值

        :param data:             字符串
        :return:                 KFResult对象
        """
        return self.setRequest(2, data, "OctetString", data)

    # Attribute of season_profile_active (No.3)
    @formatResponse
    def get_season_profile_active(self, dataType=False, response=None):
        """
        获取属性 season_profile_active 的值

        :param dataType:           是否返回数据类型， 默认False不返回
        :param response:           如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                   字典
        """
        return self.__get_season_profile(dataType, response, 3)

    @formatResponse
    def check_season_profile_active(self, ck_data):
        """
        检查属性 season_profile_active 的值

        :param ck_data:   字典

        ck_data 的数据格式为:
        {
            0: ['1', 'FFFF-01-01-FF-00-00-00-00-8000-00', '1'],
            1: ['S01', 'FFFF-01-01-FF-00-00-00-00-8000-00', 'W01']
        }
        """
        return checkResponsValue(self.get_season_profile_active(), ck_data)

    @formatResponse
    def set_season_profile_active(self, data):
        """
        设置属性 season_profile_active 的值

        :param data:           字典

        data 的数据格式为:
        {
            0: ['1', 'FFFF-01-01-FF-00-00-00-00-8000-00', '1'],
            1: ['S01', 'FFFF-01-01-FF-00-00-00-00-8000-00', 'W01']
        }
        """
        return self.__set_season_profile(data, 3)

    # Attribute of week_profile_table_active (No.4)
    @formatResponse
    def get_week_profile_table_active(self, dataType=False, response=None):
        """
        获取属性 week_profile_table_active 的值

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                  字典
        """
        return self.__get_week_profile_table(dataType, response, 4)

    @formatResponse
    def check_week_profile_table_active(self, ck_data):
        """
        检查属性 week_profile_table_active 的值

        :param ck_data:           字典
        :return:                  KFResult 对象

        ck_data 的数据格式为:
        {
            0: ['1', 0, 0, 0, 0, 0, 0, 0],
            1: ['W02', 0, 0, 0, 0, 0, 0, 0]
        }
        """
        return checkResponsValue(self.get_week_profile_table_active(), ck_data)

    @formatResponse
    def set_week_profile_table_active(self, data):
        """
        设置属性 week_profile_table_active 的值

        :param data:           字典
        :return:               KFResult 对象

        ck_data 的数据格式为:
        {
            0: ['1', 0, 0, 0, 0, 0, 0, 0],
            1: ['W02', 0, 0, 0, 0, 0, 0, 0]
        }
        """
        return self.__set_week_profile_table(data, 4)

    # Attribute of day_profile_table_active (No.5)
    @formatResponse
    def get_day_profile_table_active(self, dataType=False, response=None):
        """
        获取属性 day_profile_table_active 的值

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :param attr:
        :return:                  字典
        """
        return self.__get_day_profile_table(dataType, response, 5)

    @formatResponse
    def check_day_profile_table_active(self, ck_data):
        """
        检查属性 day_profile_table_active 的值

        :param ck_data:         字典
        :param attr:

        ck_data 的数据格式为: 注意内嵌的双层list
        {
             0 : [0, [['0:0', '0.0.10.0.100.255', '1'], ['0:30', '0.0.10.0.100.255', '2']]],
             1 : [0, [['0:30', '0.0.10.0.100.255', '1'], ['1:30', '0.0.10.0.100.255', '2'], ['2:30', '0.0.10.0.100.255', '3']]],
             2 : [0, [['0:30', '0.0.10.0.100.255', '1']]]
        }
        :return:   KFResult对象
        """
        return checkResponsValue(self.get_day_profile_table_active(), ck_data)

    @formatResponse
    def set_day_profile_table_active(self, data):
        """
        为属性 day_profile_table_active 赋值

        :param data:  预期值
        :return:      KFResult对象

        data 的数据格式为: 注意内嵌的双层list
        {
             0 : [0, [['0:0', '0.0.10.0.100.255', '1'], ['0:30', '0.0.10.0.100.255', '2']]],
             1 : [0, [['0:30', '0.0.10.0.100.255', '1'], ['1:30', '0.0.10.0.100.255', '2'], ['2:30', '0.0.10.0.100.255', '3']]],
             2 : [0, [['0:30', '0.0.10.0.100.255', '1']]]
        }
        """
        return self.__set_day_profile_table(data, 5)

    # Attribute of calendar_name_passive (No.6)
    @formatResponse
    def get_calendar_name_passive(self, dataType=False, response=None):
        """
        获取 calendar_name_passive

        :param dataType:     是否返回数据类型， 默认False不返回
        :param response:     如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:             字符串
        """
        return self.__get_calendar_name(dataType, response, 6)

    @formatResponse
    def check_calendar_name_passive(self, ck_data):
        """
        检查 calendar_name_passive

        :param ck_data:     字符串
        :return:            KFResult 对象
        """
        ret = self.get_calendar_name_passive()
        if str(ret) == str(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_calendar_name_passive(self, data, isDownloadMode=True):
        """
        设置 calendar_name_passive

        :param data:                字符串
        :param isDownloadMode:      字符串
        :return:                    KFResult 对象
        """
        error(f'C20:set_calendar_name_passive {data}')

        if isDownloadMode:
            value = {"passiveCalendarName": data}
            return setMPCValue(self.conn, mpcMap=value)
        else:
            return self.setRequest(6, data, "OctetString", data)

    # Attribute of season_profile_passive (No.7)
    @formatResponse
    def get_season_profile_passive(self, dataType=False, response=None):
        """
        获取 season_profile_passive

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                  字典
        """
        return self.__get_season_profile(dataType, response, 7)

    @formatResponse
    def check_season_profile_passive(self, ck_data):
        """
        检查 season_profile_passive

        :param ck_data:     字典
        :return:            KFResult对象

        ck_data 的数据格式为:
        {
            0: ['1', 'FFFF-01-01-FF-00-00-00-00-8000-00', '1'],
            1: ['S01', 'FFFF-01-01-FF-00-00-00-00-8000-00', 'W01']
        }
        """
        return checkResponsValue(self.get_season_profile_passive(), ck_data)

    @formatResponse
    def set_season_profile_passive(self, data, isDownloadMode=True):
        """
        设置 season_profile_passive

        :param data:                字典
        :param isDownloadMode:      字典
        :return:                    KFResult对象

        data 的数据格式为:
        {
            0: ['1', 'FFFF-01-01-FF-00-00-00-00-8000-00', '1'],
            1: ['S01', 'FFFF-01-01-FF-00-00-00-00-8000-00', 'W01']
        }
        """
        if isDownloadMode:
            data = {"passiveSeasonProfile": data}
            return setMPCValue(self.conn, mpcMap=data)
        else:
            return self.__set_season_profile(data, 7)

    # Attribute of week_profile_table_passive (No.8)
    @formatResponse
    def get_week_profile_table_passive(self, dataType=False, response=None):
        """
        获取属性 week_profile_table_passive 的值

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                  字典
        """
        return self.__get_week_profile_table(dataType, response, 8)

    @formatResponse
    def check_week_profile_table_passive(self, ck_data):
        """
        检查属性 week_profile_table_passive 的值

        :param ck_data:           字典
        :return:                  KFResult 对象

        ck_data 的数据格式为:
        {
            0: ['1', 0, 0, 0, 0, 0, 0, 0],
            1: ['W02', 0, 0, 0, 0, 0, 0, 0]
        }
        """
        return checkResponsValue(self.get_week_profile_table_passive(), ck_data)

    @formatResponse
    def set_week_profile_table_passive(self, data, isDownloadMode=True):
        """
        设置属性 week_profile_table_passive 的值

        :param data:                        字典
        :param isDownloadMode:              字典
        :return:                            KFResult 对象

        ck_data 的数据格式为:
        {
            0: ['1', 0, 0, 0, 0, 0, 0, 0],
            1: ['W02', 0, 0, 0, 0, 0, 0, 0]
        }
        """
        if isDownloadMode:
            data = {"passiveWeekProfile": data}
            return setMPCValue(self.conn, mpcMap=data)
        else:
            return self.__set_week_profile_table(data, 8)

    # Attribute of day_profile_table_passive (No.9)
    @formatResponse
    def get_day_profile_table_passive(self, dataType=False, response=None):
        """
        获取属性 day_profile_table_passive 的值

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                  字典
        """
        return self.__get_day_profile_table(dataType, response, 9)

    @formatResponse
    def check_day_profile_table_passive(self, ck_data):
        """
        检查属性 day_profile_table_passive 的值

        :param ck_data:         字典
        ck_data 的数据格式为: 注意内嵌的双层list
        {
             0 : [0, [['0:0', '0.0.10.0.100.255', '1'], ['0:30', '0.0.10.0.100.255', '2']]],
             1 : [0, [['0:30', '0.0.10.0.100.255', '1'], ['1:30', '0.0.10.0.100.255', '2'], ['2:30', '0.0.10.0.100.255', '3']]],
             2 : [0, [['0:30', '0.0.10.0.100.255', '1']]]
        }
        :return:   KFResult对象
        """
        return checkResponsValue(self.get_day_profile_table_passive(), ck_data)

    @formatResponse
    def set_day_profile_table_passive(self, data, isDownloadMode=True):
        """
        为属性 day_profile_table_passive 赋值

        :param data:                    预期值
        :param isDownloadMode:          预期值
        :return:                        KFResult对象

        data 的数据格式为: 注意内嵌的双层list
        {
             0 : [0, [['0:0', '0.0.10.0.100.255', '1'], ['0:30', '0.0.10.0.100.255', '2']]],
             1 : [0, [['0:30', '0.0.10.0.100.255', '1'], ['1:30', '0.0.10.0.100.255', '2'], ['2:30', '0.0.10.0.100.255', '3']]],
             2 : [0, [['0:30', '0.0.10.0.100.255', '1']]]
        }
        """
        if isDownloadMode:
            data = {"passiveDayProfile": data}
            return setMPCValue(self.conn, mpcMap=data)
        else:
            return self.__set_day_profile_table(data, 9)

    # Attribute of activate_passive_calendar_time (No.10)
    @formatResponse
    def get_activate_passive_calendar_time(self, dataType=False, response=None):
        """
        获取属性 activate_passive_calendar_time 的值

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                  字符串
        """
        if response is None:
            response = self.getRequest(10)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDateTimeString(ret[0]), ret[1]
        return hex_toDateTimeString(ret[0])

    @formatResponse
    def check_activate_passive_calendar_time(self, ck_data):
        """
        检查 activate_passive_calendar_time 的值

        :param ck_data:       字符串（FFFF0AFE07030000FF800080）
        :return:              KFResult对象
        """
        ret = self.get_activate_passive_calendar_time()
        if ck_data in ret:
            return KFResult(True, "")
        return KFResult(False, f"{ret} not contains {ck_data}")

    @formatResponse
    def set_activate_passive_calendar_time(self, data):
        """
        :param data:     字符串（FFFF0AFE07030000FF800080）
        :return:         KFResult对象
        """
        return self.setRequest(10, dateTime_toHex(data), "OctetString", data)

    # Method of active_passive_calendar (No.1)
    @formatResponse
    def act_activate_passive_calendar(self, data=0):
        """
        This method copies all attributes called …_passive to the corresponding attributes called …_active

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)
