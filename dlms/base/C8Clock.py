# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *


class C8Clock(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "time",
        3: "time_zone",
        4: "status",
        5: "daylight_savings_begin",
        6: "daylight_savings_end",
        7: "daylight_savings_deviation",
        8: "daylight_savings_enabled",
        9: "clock_base"
    }

    action_index_dict = {
        1: "adjust_to_quarter",
        2: "adjust_to_measuring_period",
        3: "adjust_to_minute",
        4: "adjust_to_preset_time",
        5: "preset_adjusting_time",
        6: "shift_time"
    }

    def __init__(self, conn, obis=None):
        self.obis = obis
        super().__init__(conn, obis, classId=8)

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
        return self.setRequest(1, obis_toHex(data), "OctetString", data)

    # Attribute of time (No.2)
    @formatResponse
    def get_time(self, dataType=False, response=None):
        """
        获取 time 的值

        :param dataType:      是否返回数据类型， 默认False不返回
        :param response:      如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:              时间字符串
        """
        if response is None:
            response = self.getRequest(2)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            print("----", response[0])
            return hex_toDateTimeString(response[0]), response[1]
        return hex_toDateTimeString(response[0])

    @formatResponse
    def check_time(self, ckTime, interval=0):
        """
        检查 time 的值

        :param ckTime:             时间字符串
        :param interval:           允许的误差范围(单位: 秒)
        :return:                   KFResult对象
        """
        return timeDiff(self.get_time()[:19], ckTime, interval)

    @formatResponse
    def set_time(self, data):
        """
        设置 time 的值

        :param data:                时间字符串, 支持三种格式
                                    1: 2019-05-01 14:24:45 0,32768,0; (十进制 hos, dev, status)   2019-05-01 14:30:30 00,8000,00 (十六进制 hos, dev, status )
                                    2: 2019-05-01 14:24:45
                                    3: 05740511FF000000008000FF (该数据类型用于异常测试)
        :return:                    KFResult对象
        """
        return self.setRequest(2, dateTime_toHex(data), "OctetString", data)

    # Attribute of time_zone
    @formatResponse
    def get_time_zone(self, dataType=False, response=None):
        """
        获取 time_zone 的值

        :param dataType:      是否返回数据类型， 默认False不返回
        :param response:
        :return:              十进制数
        """
        if response is None:
            response = self.getRequest(3)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toTimeZone(response[0]), response[1]
        return hex_toTimeZone(response[0])

    @formatResponse
    def check_time_zone(self, ck_data):
        """
        检查 time_zone 的值

        :param ck_data:      十进制数
        :return:             KFResult对象
        """
        ret = self.get_time_zone()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_time_zone(self, data):
        """
        设置 time_zone 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(3, timezone_toHex(data), "Long", data)

    # Attribute of status (No.4)
    @formatResponse
    def get_status(self, dataType=False, response=None):
        """
        获取 status 的值

        :param dataType:      是否返回数据类型， 默认False不返回
        :param response:      如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:             status字符串
        """
        if response is None:
            response = self.getRequest(4)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toDec(response[0]), response[1]
        return hex_toDec(response[0])

    @formatResponse
    def check_status(self, ck_data):
        """
        检查 status 的值

        :param ck_data:       字符串
        :return:              KFResult对象
        """
        ret = self.get_status()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_status(self, data):
        """
        设置 status 的值

        :param data:          字符串
        :return:              KFResult对象
        """
        return self.setRequest(4, dec_toHexStr(data, 2), "Unsigned", data)

    # Attribute of daylight_savings_begin (No.5)
    @formatResponse
    def get_daylight_savings_begin(self, dataType=False, response=None):
        """
        获取 daylights_savings_begin 的值

        :param dataType:         是否返回数据类型， 默认False不返回
        :param response:         如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                 夏令时格式时间（FFFF-03-FE-07-02-00-00-00-8000-FF）
        """
        if response is None:
            response = self.getRequest(5)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toWildcardTimeString(response[0]), response[1]
        return hex_toWildcardTimeString(response[0])

    @formatResponse
    def check_daylight_savings_begin(self, ck_data):
        """
        检查 daylights_savings_begin 的值

        :param ck_data:          夏令时格式时间（FFFF-03-FE-07-02-00-00-00-8000-FF）
        :return:                 KFResult对象
        """
        ret = self.get_daylight_savings_begin()
        if ret in ck_data:
            return KFResult(True, "")
        return KFResult(False, f"{ret} not cotains {ck_data}")

    @formatResponse
    def set_daylight_savings_begin(self, data):
        """
        设置 daylights_savings_begin 的值

        :param data:               字符串（FFFF03FE07020000FF800000）
        :return:                   KFResult对象
        """
        return self.setRequest(5, str(data).replace("-", ""), "OctetString", data)

    # Attribute of daylight_savings_end (No.6)
    @formatResponse
    def get_daylight_savings_end(self, dataType=False, response=None):
        """
        获取 daylights_savings_end 的值

        :param dataType:         是否返回数据类型， 默认False不返回
        :param response:         如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                 夏令时格式时间（FFFF-03-FE-07-02-00-00-00-8000-FF）
        """
        if response is None:
            response = self.getRequest(6)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toWildcardTimeString(response[0]), response[1]
        return hex_toWildcardTimeString(response[0])

    @formatResponse
    def check_daylight_savings_end(self, ck_data):
        """
        检查 daylights_savings_end 的值

        :param ck_data:          夏令时格式时间（FFFF-03-FE-07-02-00-00-00-8000-FF）
        :return:                 KFResult对象
        """
        ret = self.get_daylight_savings_end()
        if ret in ck_data:
            return KFResult(True, "")
        return KFResult(False, f"{ret} not cotains {ck_data}")

    @formatResponse
    def set_daylight_savings_end(self, data):
        """
        设置 daylights_savings_end 的值

        :param data:           16进制夏令时格式字符串（FFFF0AFE07030000FF800080）
        :return:               KFResult对象
        """

        return self.setRequest(6, str(data).replace("-", ""), "OctetString", data)

    # Attribute of daylight_savings_deviation (No.7)
    @formatResponse
    def get_daylight_savings_deviation(self, dataType=False, response=None):
        """
        获取 daylights_savings_deviation 的值

        :param dataType:        是否返回数据类型， 默认False不返回
        :param response:        如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                十进制数
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
    def check_daylight_savings_deviation(self, ck_data):
        """
        检查 daylights_savings_deviation 的值

        :param ck_data:         十进制数
        :return:                KFResult对象
        """
        ret = self.get_daylight_savings_deviation()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_daylight_savings_deviation(self, data):
        """
        设置 daylights_savings_deviation 的值

        :param data:             十进制数 (-120 ~ 120)
        :return:                 KFResult对象
        """
        data = int(data)
        if data < 0:
            data = 256 + data
        return self.setRequest(7, dec_toHexStr(data, 2), "Integer", data)

    # Attribute of daylight_savings_enabled (No.8)
    @formatResponse
    def get_daylight_savings_enabled(self, dataType=False, response=None):
        """
        获取 daylights_savings_enabled 的值

        :param dataType:           是否返回数据类型， 默认False不返回
        :param response:           如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                   十进制数
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
    def check_daylight_savings_enabled(self, ck_data):
        """
        检查 daylights_savings_enabled 的值

        :param ck_data:             十进制数
        :return:                    KFResult对象
        """
        ret = self.get_daylight_savings_enabled()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_daylight_savings_enabled(self, data):
        """
        设置 daylights_savings_enabled 的值

        :param data:                 十进制数
        :return:                     KFResult对象
        """
        return self.setRequest(8, dec_toHexStr(data, 2), "Bool", data)

    # Attribute of clock_base (No.9)
    @formatResponse
    def get_clock_base(self, dataType=False, response=None):
        """
        获取 clock_base 的值

        :param dataType:      是否返回数据类型， 默认False不返回
        :param response:      如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:              十进制数
        """
        if response is None:
            response = self.getRequest(9)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_clock_base(self, ck_data):
        """
        检查 clock_base 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        ret = self.get_clock_base()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_clock_base(self, data):
        """
        设置 clock_base的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(9, dec_toHexStr(data, 2), "Enum", data)

    # ==================================================================================================#

    @formatResponse
    def get_time_by_period(self, period, offset=0):
        """
        根据给定的周期和偏移量获得等待offset秒后到达下一条曲线的捕获时间

        :param period:  周期时间（分钟）
        :param offset   偏移量（秒）
        :return:        时间字符串(2018-10-01 23:15:00)
        """
        current_datetime = datetime.datetime.strptime(self.get_time()[:19], '%Y-%m-%d %H:%M:%S')
        seconds = current_datetime.hour * 3600 + current_datetime.minute * 60 + current_datetime.second
        # 周期小于等于一天
        if period <= 1440:
            sums = 0
            tmp_list = []
            while sums <= 1440:
                tmp_list.append(sums)
                sums += period
            tmp_list.append(sums)
            set_seconds = list(filter(lambda x: x * 60 > seconds, tmp_list))[0] * 60
            datetime_str = str(current_datetime.year) + "-" + str(current_datetime.month) + \
                           "-" + str(current_datetime.day) + " 00:00:00"
            get_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S') + \
                           datetime.timedelta(seconds=set_seconds - offset)
            return get_datetime.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ""
