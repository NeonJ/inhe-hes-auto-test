# -*- coding: UTF-8 -*-

from dlms.DlmsClass import *
from libs.Constants import *


class C5Demand(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "current_average_value",
        3: "last_average_value",
        4: "scaler_unit",
        5: "status",
        6: "capture_time",
        7: "start_time_current",
        8: "period",
        9: "number_of_periods"
    }

    action_index_dict = {
        1: "reset",
        2: "next_period"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=5)

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

    # Attribute of current_average_value （No.2）
    @formatResponse
    def get_current_average_value(self, dataType=False, response=None, obis=None):
        """
        获取 current_average_value 的值

        :param obis:        obis (ex. 1-0:99.1.0.255)
        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个十进制数
        """
        obis = obis if obis is not None else self.obisList[0]

        if response is None:
            response = self.getRequestWithObis(2, obis)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]
        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_current_average_value(self, ck_data):
        """
        检查 current_average_value 的值

        :param ck_data:     期望值 (十进制数)
        :return:            返回一个KFResult对象
        """
        ret = self.get_current_average_value()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_current_average_value(self, data):
        """
        设置 current_average_value 的值

        :param data:        期望值 (十进制数)
        :return:            返回一个KFResult对象
        """
        return self.setRequest(2, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of last_average_value (No.3)
    @formatResponse
    def get_last_average_value(self, dataType=False, response=None, obis=None):
        """
        获取 last_average_value 的值

        :param obis:        obis (ex. 1-0:99.1.0.255)
        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个十进制数
        """
        obis = obis if obis is not None else self.obisList[0]

        if response is None:
            response = self.getRequestWithObis(3, obis)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_last_average_value(self, ck_data):
        """
        检查 last_average_value 的值

        :param ck_data:     期望值 (十进制数)
        :return:            返回一个KFResult对象
        """
        ret = self.get_last_average_value()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_last_average_value(self, data):
        """
        设置 last_average_value 的值

        :param data:        期望值 (十进制数)
        :return:            返回一个KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of scaler_unit (No.4)
    @formatResponse
    def get_scaler_unit(self, dataType=False, response=None):
        """
        获取 scaler_unit 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            返回一个字典
        """
        if response is None:
            response = self.getRequest(4)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for key, value in response[0].items():
            for index, item in enumerate(value):
                value[index] = hex_toDec(item, response[1][key][index])
                # value[index] = UnitsMap.get(hex_toDec(item), "None")
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_scaler_unit(self, ck_data):
        """
        检查 scaler_unit 的值

        :param ck_data:         接收一个字典参数
        :return                 返回一个 KFResult 对象

        ck_data 是一个字典, 描述了预期的结果数据
        {
            0: [0, 'W']
        }
        """
        # 处理量纲直接给数值的情况
        for value in ck_data.values():
            for index, item in enumerate(value):
                if index == 1:
                    if not re.findall("[a-zA-Z]", str(item)):
                        value[index] = str(UnitsMap.get(int(item), None))
        return checkResponsValue(self.get_scaler_unit(), ck_data)

    @formatResponse
    def set_scaler_unit(self, data):
        """
        设置 scaler_unit 的值

        :param data:            接收一个字典参数
        :return                 返回一个 KFResult 对象

        data 是一个字典, 描述了预期的结果数据
        {
            0: [0, 'W']
        }
        """
        # 处理量纲直接给数值的情况
        for value in data.values():
            for index, item in enumerate(value):
                if index == 1:
                    if not re.findall("[a-zA-Z]", str(item)):
                        value[index] = str(UnitsMap.get(int(item), None))
        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(len(data[0]), 4))
        for index, item in enumerate(data[0]):
            if index == 0:
                etree.SubElement(struct, "Integer").set("Value", dec_toHexStr(item, 2))
            if index == 1:
                etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(
                    str(dict(zip(UnitsMap.values(), UnitsMap.keys()))[item]), 2))
        return self.setRequest(4, struct, "struct", data)

    # Attribute of Status (No.5)
    @formatResponse
    def get_status(self, dataType=False, response=None):
        """
        获取 Status 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    返回一个字符串
        """
        if response is None:
            response = self.getRequest(5)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return response
        if response[1] in ["DoubleLongUnsigned", "Long64Unsigned", "LongUnsigned", "Unsigned"]:
            return hex_toDec(response[0])
        else:
            return response[0]

    @formatResponse
    def check_status(self, ck_data):
        """
        检查 Status 的值

        :param ck_data:            期望结果（字符串）
        :return:                   返回一个 KFResult 对象
        """
        ret = self.get_status()
        if ret == ck_data:
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_status(self, data):
        """
        设置 Status 的值

        :param data:             期望结果（二进制字符串）
        :return:                 返回一个 KFResult 对象
        """
        return self.setRequest(5, data, "BitString", data)

    # Attribute of capture_time （No.6）
    @formatResponse
    def get_capture_time(self, dataType=False, response=None, obis=None):
        """
        获取 capture_time 的值

        :param dataType:        是否返回数据类型， 默认False不返回
        :param response:        如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                返回一个时间字符串
        """
        obis = obis if obis is not None else self.obisList[0]

        if response is None:
            response = self.getRequestWithObis(6, obis)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toDateTimeString(response[0]), response[1]
        return hex_toDateTimeString(response[0])

    @formatResponse
    def check_capture_time(self, ckTime, interval=0):
        """
        检查 capture_time 的值

        :param ckTime:         预期时间字符串
        :param interval:       允许的误差范围(单位: 秒)
        :return:
        """
        return timeDiff(self.get_capture_time(), ckTime, interval)

    @formatResponse
    def set_capture_time(self, data):
        """
        设置 capture_time 的值

        :param data:          预期时间字符串
        :return:              KFResult对象
        """
        if not str(data).startswith("F"):
            data = dateTime_toHex(data)
        return self.setRequest(6, data, "OctetString", data)

    # Attribute of start_time_current (No.7)
    @formatResponse
    def get_start_time_current(self, dataType=False, response=None):
        """
        获取 start_time_current 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    时间字符串
        """
        if response is None:
            response = self.getRequest(7)

        response = getSingleDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        if dataType:
            return hex_toDateTimeString(response[0]), response[1]
        return hex_toDateTimeString(response[0])

    @formatResponse
    def check_start_time_current(self, ckTime, interval=0):
        """
        检查 start_time_current 的值

        :param ckTime:               预期时间字符串
        :param interval:             允许的误差范围（单位：秒）
        :return:                     返回一个 KFResult 对象
        """
        return timeDiff(self.get_start_time_current(), ckTime, interval)

    @formatResponse
    def set_start_time_current(self, data):
        """
        设置 start_time_current 的值

        :param data:                 预期时间字符串
        :return:                     返回一个 KFResult 对象
        """
        if not str(data).startswith("F"):
            data = dateTime_toHex(data)
        return self.setRequest(7, data, "OctetString", data)

    # Attribute of period (No.8)
    @formatResponse
    def get_period(self, dataType=False, response=None):
        """
        获取 period 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :param response:            如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                    十进制数
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
    def check_period(self, ck_data):
        """
        检查 period 的值

        :param ck_data:           期望值（十进制数）
        :return:                  返回一个 KFResult 对象
        """
        ret = self.get_period()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_period(self, data):
        """
        设置 period 的值

        :param data:             期望值（十进制数）
        :return:                 返回一个 KFResult 对象
        """
        return self.setRequest(8, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of number_of_periods (No.9)
    @formatResponse
    def get_number_of_periods(self, dataType=False, response=None, obis=None):
        """
        获取 number_of_periods 的值

        :param dataType:            是否返回数据类型， 默认False不返回
        :return:                    十进制数
        """
        obis = obis if obis is not None else self.obisList[0]

        if response is None:
            response = self.getRequestWithObis(9, obis)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]
        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_number_of_periods(self, ck_data):
        """
        检查 number_of_periods 的值

        :param ck_data:           预期值（十进制数）
        :return:                  返回一个 KFResult 对象
        """
        ret = self.get_number_of_periods()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_number_of_periods(self, data):
        """
        设置 number_of_periods 的值

        :param data:              预期值（十进制数）
        :return:                  返回一个 KFResult 对象
        """
        return self.setRequest(9, dec_toHexStr(data, 4), "LongUnsigned", data)

    # Method of reset
    @formatResponse
    def act_reset(self, data=0):
        """
        This method forces a reset of the object. Activating this method provokes the following actions:
        - the current period is terminated;
        - the current_average_value and the last_average_value are set to their default values;
        - the capture_time and the start_time_current are set to the time of the execution of reset (data).

        :param data:             十进制数
        :return:                 返回一个 KFResult 对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)

    # Method of next_period
    @formatResponse
    def act_next_period(self, data=0):
        """
        This method is used to trigger the regular termination (and restart) of a period. Closes (terminates) the
         current measuring period. Updates capture_time and start_time and copies current_average_value to
         last_average_value, sets current_average_value to its default value. Starts the next measuring period.

        :param data:             十进制数
        :return:                 返回一个KFResult
        """
        return self.actionRequest(2, dec_toHexStr(data, 2), "Integer", data)

    # ==================================================================================================#

    @formatResponse
    def get_current_average_value_with_list(self):
        """
        批量获取 class 5 的 current_average_value 值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            response[index] = self.get_current_average_value(obis=obis)
        return response

    @formatResponse
    def check_current_average_value_with_list(self, ck_data, initial=None):
        """
        批量检查 class 5 的 current_average_value 值 (先减去期望值, 再与预期值对比)

        :param ck_data:       期望值
        :param initial:       初始值
        :return:              KFResult 对象
        """
        response = list()
        result = self.get_current_average_value()

        if initial is None:
            initial = dict()
        try:
            for key, value in ck_data.items():
                # 如果increment字典中特定的Key没有对应的值, 则赋值为0
                if int(key) not in initial:
                    initial[key] = 0

                # ck_data 中包含范围时
                if isinstance(value, list):
                    if not int(value[0]) <= (int(result[key]) - int(initial[key])) <= int(value[-1]):
                        response.append(f"'response[{key}]={result[key]}' not in range of 'ck_data[{key}]={value}'")
                else:
                    if int(value) != int(result[key]) - int(initial[key]):
                        response.append(f"'response[{key}]={result[key]}' not equal to 'ck_data[{key}]={value}'")
            if len(response) == 0:
                return KFResult(True, '')
            else:
                return KFResult(False, "; ".join(response))

        except Exception as ex:
            error(ex)

    @formatResponse
    def get_last_average_value_with_list(self):
        """
        批量获取 class 5 的 last_average_value 值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            response[index] = self.get_last_average_value(obis=obis)
        return response

    @formatResponse
    def check_last_average_value_with_list(self, ck_data, initial=None):
        """
        批量检查 class 5 的 current_average_value 值 (先减去期望值, 再与预期值对比)

        :param ck_data:       期望值
        :param initial:       初始值
        :return:              KFResult对象
        """
        response = list()
        result = self.get_last_average_value_with_list()

        if initial is None:
            initial = dict()
        try:
            for key, value in ck_data.items():
                # 如果increment字典中特定的Key没有对应的值, 则赋值为0
                if int(key) not in initial:
                    initial[key] = 0

                # ck_data 中包含范围时
                if isinstance(value, list):
                    if not int(value[0]) <= (int(result[key]) - int(initial[key])) <= int(value[-1]):
                        response.append(f"'response[{key}]={result[key]}' not in range of 'ck_data[{key}]={value}'")
                else:
                    if int(value) != int(result[key]) - int(initial[key]):
                        response.append(f"'response[{key}]={result[key]}' not equal to 'ck_data[{key}]={value}'")
            if len(response) == 0:
                return KFResult(True, '')
            else:
                return KFResult(False, "; ".join(response))

        except Exception as ex:
            error(ex)

    @formatResponse
    def get_number_of_periods_with_list(self):
        """
        批量获取 class 5 的 number_of_periods 值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            response[index] = self.get_number_of_periods(obis=obis)
        return response

    @formatResponse
    def get_capture_time_with_list(self):
        """
        批量获取 class 5 的 capture_time 值

        :return:  返回一个字典
        """
        response = dict()
        for index, obis in enumerate(self.obisList):
            response[index] = self.get_capture_time(obis=obis)
        return response
