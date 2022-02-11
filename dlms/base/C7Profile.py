# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C7Profile(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "buffer",
        3: "capture_objects",
        4: "capture_period",
        5: "sort_method",
        6: "sort_object",
        7: "entries_in_use",
        8: "profile_entries"
    }

    action_index_dict = {
        1: "reset",
        2: "capture"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=7)

    @staticmethod
    def __bufferResponse(data, dataType):
        """
        对返回的buffer进行数据类型转换

        :param data:         存储的buffer数据
        :param dataType      data数据对应的数据类型
        :return:             转换数据类型后的buffer数据
        """
        if isinstance(data, dict):
            for key, value in data.items():
                for index, item in enumerate(value):
                    if item == 'NullData':
                        value[index] = 'NullData'
                    elif isinstance(item, list):
                        for subIndex, subItem in enumerate(item):
                            if isinstance(subItem, list):
                                for sub2Index, sub2Item in enumerate(subItem):
                                    if isinstance(sub2Item, list):
                                        for sub3Index, sub3Item in enumerate(sub2Item):  # for 0-0:94.43.132.255
                                            if isinstance(sub3Item, list):
                                                for sub4Index, sub4Item in enumerate(sub3Item):
                                                    if checkDataTypeIsNum(
                                                            dataType[key][index][subIndex][sub2Index][sub3Index][
                                                                sub4Index]).status:
                                                        sub3Item[sub4Index] = hex_toDec(sub4Item)
                                            else:
                                                if checkDataTypeIsNum(
                                                        dataType[key][index][subIndex][sub2Index][sub3Index]).status:
                                                    sub2Item[sub3Index] = hex_toDec(sub3Item)
                                                elif len(sub3Item.strip()) >= 24 and \
                                                        dataType[key][index][subIndex][sub2Index][sub3Index] in [
                                                    "OctetString", "DateTime"]:
                                                    sub2Item[sub3Index] = hex_toDateTimeString(sub3Item)
                                                elif len(sub3Item.strip()) == 12 and \
                                                        dataType[key][index][subIndex][sub2Index][sub3Index] in [
                                                    "OctetString"]:
                                                    sub2Item[sub3Index] = hex_toOBIS(sub3Item)
                                    elif len(sub2Item.strip()) >= 24 and dataType[key][index][subIndex][sub2Index] in [
                                        "OctetString", "DateTime"]:
                                        subItem[sub2Index] = hex_toDateTimeString(sub2Item)
                                    elif checkDataTypeIsNum(dataType[key][index][subIndex][sub2Index]).status:
                                        subItem[sub2Index] = hex_toDec(sub2Item)
                                    elif len(sub2Item.strip()) == 12 and dataType[key][index][subIndex][sub2Index] in [
                                        "OctetString"]:
                                        subItem[sub2Index] = hex_toOBIS(sub2Item)
                            elif len(subItem.strip()) >= 24 and dataType[key][index][subIndex] in ["OctetString",
                                                                                                   "DateTime"]:
                                item[subIndex] = hex_toDateTimeString(subItem)
                            elif len(subItem.strip()) == 12 and dataType[key][index][subIndex] in ["OctetString"]:
                                item[subIndex] = hex_toOBIS(subItem)
                            elif checkDataTypeIsNum(dataType[key][index][subIndex]).status:
                                item[subIndex] = hex_toDec(subItem)
                    elif len(item.strip()) >= 24 and dataType[key][index] in ["OctetString", "DateTime"]:
                        value[index] = hex_toDateTimeString(item)
                    elif dataType[key][index] == "VisibleString":
                        value[index] = hex_toAscii(item)
                    else:
                        if checkDataTypeIsNum(dataType[key][index]).status:
                            value[index] = hex_toDec(item)
        return data

    @staticmethod
    def __checkPeriod(response, capture_period):
        """
        检查返回的曲线是否连续

        :param response:         存储的buffer数据
        :param capture_period:   曲线周期
        :return:                 KFResult 对象
        """
        if not response or len(response) < 2:
            return KFResult(False, "the response data is not correct")
        time_list = [string_toTimestamp(item[0][:19]) for item in response.values()]
        for i in range(len(time_list) - 1):
            if (time_list[i + 1] - time_list[i]) != capture_period:
                return KFResult(False, f"{time_list[i + 1]} and {time_list[i]} is not successive")
        info("Check capture period success")
        return KFResult(True, "Check capture period success")

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

    # Attribute of buffer (No.2)
    @formatResponse
    def get_buffer(self, dataType=False, response=None):
        """
        获取 buffer 的值 (全部)

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个字典
        """
        if response is None:
            response = self.getRequest(2)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return self.__bufferResponse(response[0], response[1]), response[1]
        return self.__bufferResponse(response[0], response[1])

    @formatResponse
    def check_buffer(self, ck_data, isCheckPeriod=False):
        """
        检查 buffer 的值

        :param ck_data:           期望值 (一个字典)
        :param isCheckPeriod:     检查获取的曲线是否连续(默认值为False不检查)
        :return:                  返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-05-12 06:00:00 00,FDE4,80', 21554],
            1: ['2019-05-15 06:00:00 00,FDE4,80', 21554]
        }
        """
        data = self.get_buffer()
        if isCheckPeriod:
            ret = self.__checkPeriod(data, self.get_capture_period())
            if not ret.status:
                return ret
        return checkResponsValue(data, ck_data)

    @formatResponse
    def set_buffer(self, data):
        """
        设置 buffer 的值

        :param data:              期望值 (一个字典)
        :return:                  返回一个KFResult对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-05-12 06:00:00 00,FDE4,80', 21554],
            1: ['2019-05-15 06:00:00 00,FDE4,80', 21554]
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index in [0, 3]:
                    etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(item))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", dec_toHexStr(item))
        return self.setRequest(2, array, "Array", data)

    @formatResponse
    def get_buffer_by_range(self, startTime, endTime, captureObjects=None, dataType=False):
        """
        基于时间范围选择性返回部分曲线

        :param startTime:           起始时间, 参数格式为: 2019-05-01 00:00:00
        :param endTime:             结束时间, 参数格式为: 2019-05-01 23:59:59
        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param dataType:            是否返回数据类型， 默认False不返回
        :return:                    返回一个字典

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        response = getStrucDataFromGetResp(self.getRequestByTime(2, startTime, endTime, captureObjects))
        if dataType:
            return self.__bufferResponse(response[0], response[1]), response[1]
        return self.__bufferResponse(response[0], response[1])

    @formatResponse
    def check_buffer_by_range(self, startTime, endTime, ck_data, captureObjects=None, isCheckPeriod=False):
        """
        基于时间范围检查返回的部分曲线

        :param startTime:           起始时间, 参数格式为: 2019-05-01 00:00:00
        :param endTime:             结束时间, 参数格式为: 2019-05-01 23:59:59
        :param ck_data:             预期结果
        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param isCheckPeriod:       检查获取的曲线是否连续(默认值为False不检查)
        :return:                    返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-07-13 10:00:00 00,FF88,80', 136, 0, 0],
            1: ['2019-07-13 10:15:00 00,FF88,80', 8, 0, 0],
            2: ['2019-07-13 10:30:00 00,FF88,80', 8, 0, 0]
        }

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        data = self.get_buffer_by_range(startTime, endTime, captureObjects)
        if isCheckPeriod:
            ret = self.__checkPeriod(data, self.get_capture_period())
            if not ret.status:
                return ret
        return checkResponsValue(data, ck_data)

    @formatResponse
    def get_buffer_by_range_today(self, captureObjects=None, dataType=False):
        """
        基于时间返回当天的全部曲线

        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param dataType:            是否返回数据类型， 默认False不返回
        :return:                    返回一个字典

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        startTime, endTime = time_range_of_today()
        if dataType:
            return self.get_buffer_by_range(startTime, endTime, captureObjects, dataType=True)
        return self.get_buffer_by_range(startTime, endTime, captureObjects)

    @formatResponse
    def check_buffer_by_range_today(self, ck_data, captureObjects=None, isCheckPeriod=False):
        """
        基于时间检查当天的全部曲线

        :param ck_data:             预期结果
        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param isCheckPeriod:       检查获取的曲线是否连续(默认值为False不检查)
        :return:                    返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-07-13 10:00:00 00,FF88,80', 136, 0, 0],
            1: ['2019-07-13 10:15:00 00,FF88,80', 8, 0, 0],
            2: ['2019-07-13 10:30:00 00,FF88,80', 8, 0, 0]
        }

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        data = self.get_buffer_by_range_today(captureObjects)
        if isCheckPeriod:
            ret = self.__checkPeriod(data, self.get_capture_period())
            if not ret.status:
                return ret
        return checkResponsValue(data, ck_data)

    @formatResponse
    def get_buffer_by_range_yesterday(self, captureObjects=None, dataType=False):
        """
        基于时间返回昨天的全部曲线

        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param dataType:
        :return                     返回一个字典

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        startTime, endTime = time_range_of_yesterday()
        if dataType:
            return self.get_buffer_by_range(startTime, endTime, captureObjects, dataType=True)
        return self.get_buffer_by_range(startTime, endTime, captureObjects)

    @formatResponse
    def check_buffer_by_range_yesterday(self, ck_data, captureObjects=None, isCheckPeriod=False):
        """
        基于时间检查昨天的全部曲线

        :param ck_data:             预期结果
        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param isCheckPeriod:       检查获取的曲线是否连续(默认值为False不检查)
        :return:                    返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-07-13 10:00:00 00,FF88,80', 136, 0, 0],
            1: ['2019-07-13 10:15:00 00,FF88,80', 8, 0, 0],
            2: ['2019-07-13 10:30:00 00,FF88,80', 8, 0, 0]
        }

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        data = self.get_buffer_by_range_yesterday(captureObjects)
        if isCheckPeriod:
            ret = self.__checkPeriod(data, self.get_capture_period())
            if not ret.status:
                return ret
        return checkResponsValue(data, ck_data)

    @formatResponse
    def get_buffer_by_range_lastWeek(self, captureObjects=None, dataType=False):
        """
        基于时间返回上周的曲线

        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param dataType:            是否返回数据类型， 默认False不返回
        :return                     返回一个字典

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : 8,0.0.1.0.0.255,0,
            1 : 3,1.0.1.8.0.255,2,
            2 : 3,1.0.4.8.0.255,2,
        }
        """
        startTime, endTime = time_range_of_lastWeek()
        if dataType:
            return self.get_buffer_by_range(startTime, endTime, captureObjects, True)
        return self.get_buffer_by_range(startTime, endTime, captureObjects)

    @formatResponse
    def check_buffer_by_range_lastWeek(self, ck_data, captureObjects=None, isCheckPeriod=False):
        """
        基于时间检查上周的全部曲线

        :param ck_data:             预期结果
        :param captureObjects:      捕获对象列表, 默认为空, 返回全部捕获对象
        :param isCheckPeriod:       检查获取的曲线是否连续(默认值为False不检查)
        :return:                    返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-07-13 10:00:00 00,FF88,80', 136, 0, 0],
            1: ['2019-07-13 10:15:00 00,FF88,80', 8, 0, 0],
            2: ['2019-07-13 10:30:00 00,FF88,80', 8, 0, 0]
        }

        ### 使用字典的方式传值, 可自由指定OBIS, 用于测试非法捕获对象
        captureObjects 是一个字典, 字典的键是OBIS, 对应的值是ClassID
        {
            0 : '8,0.0.1.0.0.255,0',
            1 : '3,1.0.1.8.0.255,2',
            2 : '3,1.0.4.8.0.255,2',
        }
        """
        data = self.get_buffer_by_range_lastWeek(captureObjects)
        if isCheckPeriod:
            ret = self.__checkPeriod(data, self.get_capture_period())
            if not ret.status:
                return ret
        return checkResponsValue(data, ck_data)

    @formatResponse
    def get_buffer_by_entry(self, startEntry, endEntry, startCaptureIndex=1, endCaptureIndex=0, dataType=False,
                            obis=None):
        """
        基于条目索引选择性返回部分曲线, 索引起始值为1, 支持负数索引(-1 代表最后一个索引)

        :param startEntry:              起始索引
        :param endEntry:                结束索引 (结束索引对应的元素内容也会返回)
        :param startCaptureIndex:       起始capture_object索引
        :param endCaptureIndex:         结束capture_object索引
        :param dataType:                是否返回数据类型， 默认False不返回
        :param obis:
        :return:                        返回一个字典
        """
        obis = obis if obis is not None else self.obisList[0]
        if int(startEntry) < 0 or int(endEntry) < 0:
            totalEntries = self.get_entries_in_use(obis=obis)
            startEntry = totalEntries + 1 + int(startEntry) if int(startEntry) < 0 else startEntry
            endEntry = totalEntries + 1 + int(endEntry) if int(endEntry) < 0 else endEntry
        response = getStrucDataFromGetResp(
            self.getRequestByEntryWithObis(2, obis, startEntry, endEntry, startCaptureIndex, endCaptureIndex))
        if dataType:
            return self.__bufferResponse(response[0], response[1]), response[1]
        return self.__bufferResponse(response[0], response[1])

    @formatResponse
    def check_buffer_by_entry(self, startEntry, endEntry, ck_data, startCaptureIndex=1, endCaptureIndex=0,
                              isCheckPeriod=False):
        """
        基于条目索引检查返回的部分曲线

        :param startEntry:              起始索引
        :param endEntry:                结束索引 (结束索引对应的元素内容也会返回)
        :param ck_data:                 期望值
        :param startCaptureIndex:       起始capture_object索引
        :param endCaptureIndex:         结束capture_object索引
        :param isCheckPeriod:           检查获取的曲线是否连续(默认值为False不检查)
        :return:                        返回一个KFResult对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: ['2019-07-13 10:00:00 00,FF88,80', 136, 0, 0],
            1: ['2019-07-13 10:15:00 00,FF88,80', 8, 0, 0],
            2: ['2019-07-13 10:30:00 00,FF88,80', 8, 0, 0]
        }
        """
        data = self.get_buffer_by_entry(startEntry, endEntry, startCaptureIndex, endCaptureIndex)
        if isCheckPeriod:
            ret = self.__checkPeriod(data, self.get_capture_period())
            if not ret.status:
                return ret
        return checkResponsValue(data, ck_data)

    # Attribute of capture_objects (No.3)
    @formatResponse
    def get_capture_objects(self, dataType=False, response=None):
        """
        获取 capture_objects 的值

        :param dataType:        是否返回数据类型， 默认False不返回
        :param response:        如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                返回一个字典
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
                if index == 1 and len(item) > 0:
                    value[index] = hex_toOBIS(item)
                else:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_capture_objects(self, ck_data):
        """
        检查 capture_objects 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0 : [8, "0-0:1.0.0.255", 2, 0],
            1 : [1, "0.0.96.10.2.255", 2, 0],
            2 : [3, "1.0.1.8.0.255", 2, 0],
            3 : [3, "1-0.2.8.0.255", 2, 0],
        }
        """
        # 处理OBIS对象的格式
        for value in ck_data.values():
            value[1].replace("-", ".").replace(":", ".")
        return checkResponsValue(self.get_capture_objects(), ck_data)

    @formatResponse
    def set_capture_objects(self, data):
        """
        设置 capture_objects 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了期望的结果数据
        {
            0 : [8, "0-0:1.0.0.255", 2, 0],
            1 : [1, "0.0.96.10.2.255", 2, 0],
            2 : [3, "1.0.1.8.0.255", 2, 0],
            3 : [3, "1-0.2.8.0.255", 2, 0],
        }
        """
        if data is None or len(data) == 0:
            array = etree.Element("Array")
            array.set("Qty", "0000")
            return self.setRequest(3, array, "Array", data)

        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        if isinstance(data, dict):
            for value in data.values():
                struct = etree.SubElement(array, "Structure")
                struct.set("Qty", dec_toHexStr(len(value), 4))
                for subIndex, subItem in enumerate(value):
                    if subIndex == 0:
                        etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                    if subIndex == 1:
                        etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
                    if subIndex == 2:
                        etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                    if subIndex == 3:
                        etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
            return self.setRequest(3, array, "Array", data)

    # Attribute of capture_period (No.4)
    @formatResponse
    def get_capture_period(self, dataType=False, response=None):
        """
        获取 capture_period 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个数值
        """
        if response is None:
            response = self.getRequest(4)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            return ret[0]
        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_capture_period(self, ck_data):
        """
        检查 capture_period 的值

        :param ck_data:             预期值
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_capture_period()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_capture_period(self, data):
        """
        检查 capture_period 的值

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        return self.setRequest(4, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of sort_method (No.5)
    @formatResponse
    def get_sort_method(self, dataType=False, response=None):
        """
        获取 sort_method 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个数值
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
    def check_sort_method(self, ck_data):
        """
        检查 sort_method 的值

        :param ck_data:             预期值
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_sort_method()
        if isinstance(ck_data, dict):
            for value in ck_data.values():
                if int(value) == int(ret):
                    return KFResult(True, "")
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_sort_method(self, data):
        """
        设置 sort_method 的值

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        if isinstance(data, dict):
            data = data.get(0)
        return self.setRequest(5, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of sort_object (No.6)
    @formatResponse
    def get_sort_object(self, dataType=False, response=None):
        """
        获取 sort_object 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字典
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
                if index == 1:
                    value[index] = hex_toOBIS(item)
                else:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_sort_object(self, ck_data):
        """
        检查 capture_objects 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0 : [0, '0-0:0.0.0.0', 0, 0]
        }
        """
        return checkResponsValue(self.get_sort_object(), ck_data)

    @formatResponse
    def set_sort_object(self, data):
        """
        设置 capture_objects 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0 : [0, '0-0:0.0.0.0', 0, 0]
        }
        """
        struct = etree.Element("Structure")
        for value in data.values():
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
                if subIndex == 1:
                    etree.SubElement(struct, "OctetString").set("Value", obis_toHex(subItem))
                if subIndex == 2:
                    etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(subItem, 2))
                if subIndex == 3:
                    etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(subItem, 4))
        return self.setRequest(6, struct, "Struct", data)

    # Attribute of entries_in_use (No.7)
    @formatResponse
    def get_entries_in_use(self, dataType=False, response=None, obis=None):
        """
        获取 entries_in_use 的值
        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :param obis:
        :return:                    返回一个数值
        """
        obis = obis if obis is not None else self.obisList[0]
        self.obis = obis

        if response is None:
            response = self.getRequestWithObis(7, obis)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toDec(response[0]), response[1]
        return hex_toDec(response[0])

    @formatResponse
    def check_entries_in_use(self, ck_data):
        """
        检查 entries_in_use 的值

        :param ck_data:             预期值
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_entries_in_use()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_entries_in_use(self, data):
        """
        设置 entries_in_use 的值

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        return self.setRequest(7, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of profile_entries (No.8)
    @formatResponse
    def get_profile_entries(self, dataType=False, response=None):
        """
        获取 profile_entries 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个数值
        """
        if response is None:
            response = self.getRequest(8)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toDec(response[0]), response[1]
        return hex_toDec(response[0])

    @formatResponse
    def check_profile_entries(self, ck_data):
        """
        检查 profile_entries 的值

        :param ck_data:             预期值
        :return:                    返回一个 KFResult 对象
        """
        ret = self.get_profile_entries()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_profile_entries(self, data):
        """
        设置 profile_entries 的值

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        return self.setRequest(8, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Method of reset
    @formatResponse
    def act_reset(self, data=0):
        """
        Clears the buffer. It has no valid entries afterwards; entries_in_use is zero after this call.
        This call does not trigger any additional operations on the capture objects. Specifically,
        it does not reset any attributes captured

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)

    # Method of capture
    @formatResponse
    def act_capture(self, data=0):
        """
        Copies the values of the objects to capture into the buffer by reading each capture object.
        Depending on the sort_method and the actual state of the buffer this produces a new entry
        or a replacement for the less significant entry. As long as not all entries are already used,
        the entries_in_use attribute will be incremented

        :param data:                期望值
        :return:                    返回一个 KFResult 对象
        """
        return self.actionRequest(2, dec_toHexStr(data, 2), "Integer", data)

    # ==================================================================================================#

    @formatResponse
    def get_buffer_by_entry_with_list(self):
        """
        批量获取 class 7 的buffer值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            if self.get_entries_in_use(obis=obis) == 0:
                response[index] = {}
            else:
                response[index] = self.get_buffer_by_entry(startEntry=1, endEntry=-1, obis=obis)
        return response

    @formatResponse
    def check_buffer_by_entry_with_list(self, ck_data, obis_dict=None, clock_error_range=0, error_range=None):
        """
        批量检查 class 7 的buffer值

        :param ck_data:                  期望值
        :param obis_dict                 指定每个Obis 比较数据, 未指定则只比较最新一条数据
        :param clock_error_range         时间误差
        :param error_range               曲线里面每个对象的误差
        :return:                         KFResult对象
        """
        response = list()
        # result = self.get_buffer_by_entry_with_list()

        try:
            for index, obis in enumerate(self.obisList):

                # 需要比较多条数据
                if obis_dict and obis_dict.get(obis, None):
                    current_obis_data = obis_dict.get(obis, None)
                    if self.get_entries_in_use(obis=obis) == 0:
                        response.append(f"The {index} obis not have profiles data")
                        continue
                    else:
                        result = self.get_buffer_by_entry(startEntry=-len(current_obis_data), endEntry=-1, obis=obis)

                    # 第一条数据和初始数据完全相同，后面的数据除了时间有误差其它数据也相同
                    for key, value in enumerate(current_obis_data):
                        if key == 0:
                            if value != result[key]:
                                response.append(
                                    f"'response[{index}][{key}]: {result[key]}' not equal to 'ck_data[{key}]={value}'")
                                break
                        else:
                            if error_range is not None:
                                # 根据不同的误差范围进行检查
                                for subIndex, subValue in enumerate(value):
                                    if re.search(r"\d{4}-\d{2}-\d{2}", str(subValue)):
                                        time_diff_result = timeDiff(subValue[:19], result[key][subIndex][:19],
                                                                    clock_error_range)
                                        if not time_diff_result.status:
                                            response.append(f"response[{index}][{key}]: {time_diff_result.result}")
                                            break
                                    else:
                                        error_value = error_range.get(subIndex, None)
                                        if error_value is not None:
                                            if abs(subValue - result[key][subIndex]) > error_value:
                                                response.append(
                                                    f"response[{index}][{key}] {subIndex + 1} Item: {result[key][subIndex]} not equal to ck_data{subValue}")

                                        else:
                                            if subValue != result[key][subIndex]:
                                                response.append(
                                                    f"response[{index}][{key}] {subIndex + 1} Item: {result[key][subIndex]} not equal to ck_data{subValue}, error_range={error_value}")

                            else:
                                for subIndex, subValue in enumerate(value):
                                    if re.search(r"\d{4}-\d{2}-\d{2}", str(subValue)):
                                        time_diff_result = timeDiff(subValue[:19], result[key][subIndex][:19],
                                                                    clock_error_range)
                                        if not time_diff_result.status:
                                            response.append(f"response[{index}][{key}]: {time_diff_result.result}")
                                            break
                                    else:
                                        if subValue != result[key][subIndex]:
                                            response.append(
                                                f"response[{index}][{key}] {subIndex + 1} Item: {result[key][subIndex]} not equal to ck_data{subValue}")

                                # 检查status的bit位是否正确
                                if len(value[0]) > 19:
                                    if not checkBit(hex_toDec(result[key][0][-2:]), value[0][23:]).status:
                                        response.append(
                                            f"'response[{index}]: check status {hex_toDec(result[key][0][-2:])} {value[0][23:]}failed'")

                else:
                    # 未指定obis则只比较第一条数据是否相同
                    if self.get_entries_in_use(obis=obis) == 0:
                        result = {}
                    else:
                        result = self.get_buffer_by_entry(startEntry=-1, endEntry=-1, obis=obis)

                    if result != ck_data[index]:
                        response.append(
                            f"'response[{index}]={result}' not equal to 'ck_data[{index}]={ck_data[index]}'")

            if len(response) == 0:
                return KFResult(True, '')
            else:
                return KFResult(False, "; ".join(response))

        except Exception as ex:
            error(ex)

    @formatResponse
    def get_entries_in_use_with_list(self):
        """
        批量获取 class 7 entries_in_use的值

        :return:  返回一个列表
        """
        response = list()
        for index, obis in enumerate(self.obisList):
            response.append(self.get_entries_in_use(obis=obis))
        return response

    @formatResponse
    def check_entries_in_use_with_list(self, ck_data):
        """
        批量检查 class 7 entries_in_use的值

        :param ck_data:                  期望值
        :return:                         KFResult对象
        """
        response = list()
        for index, obis in enumerate(self.obisList):
            result = self.get_entries_in_use(obis=obis)
            if result != ck_data[index]:
                response.append(f"'response[{index}]={result}' not equal to 'ck_data[{index}]={ck_data[index]}'")

        if len(response) == 0:
            return KFResult(True, '')
        else:
            return KFResult(False, "; ".join(response))
