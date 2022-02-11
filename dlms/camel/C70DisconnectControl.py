# -*- coding: UTF-8 -*-

from projects.camel.comm import setMPCValue

from dlms.DlmsClass import *


class C70DisconnectControl(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "output_state",
        3: "control_state",
        4: "control_mode"
    }

    action_index_dict = {
        1: "remote_disconnect",
        2: "remote_reconnect"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=70)

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

    # Attribute of output_state
    @formatResponse
    def get_output_state(self, dataType=False, response=None):
        """
        获取 output_state 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_output_state(self, ck_data):
        """
        检查 output_state 的值

        :param ck_data:            十进制数
        :return:                   KFResult对象
        """
        ret = self.get_output_state()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_output_state(self, data):
        """
        设置 output_state 的值

        :param data:       十进制数
        :return:           KFResult对象
        """
        return self.setRequest(2, dec_toHexStr(data, 2), "Bool", data)

    # Attribute of control_state
    @formatResponse
    def get_control_state(self, dataType=False, response=None):
        """
        获取 control_state 的值

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
    def check_control_state(self, ck_data):
        """
        检查 control_state 的值

        :param ck_data:       十进制数
        :return:              KFResult对象
        """
        ret = self.get_control_state()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_control_state(self, data):
        """
        设置 control_state 的值

        :param data:            十进制数
        :return:                KFResult对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of control_mode
    @formatResponse
    def get_control_mode(self, dataType=False, response=None):
        """
        获取 control_mode 的值

        :param dataType:          是否返回数据类型， 默认False不返回
        :param response:          如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:                  十进制数
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
    def check_control_mode(self, ck_data):
        """
        检查 control_mode 的值

        :param ck_data:           十进制数
        :return:                  KFResult对象
        """
        ret = self.get_control_mode()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_control_mode(self, data, isDownloadMode=True):
        """
        设置 control_mode 的值

        :param data:                十进制数
        :param isDownloadMode:
        :return:                    KFResult对象
        """
        if isDownloadMode:
            data = {"controlMode": data}
            return setMPCValue(self.conn, mpcMap=data)
        else:
            return self.setRequest(4, dec_toHexStr(data, 2), "Enum", data)

    # Method of remote_disconnect
    @formatResponse
    def act_remote_disconnect(self, data=0):
        """
        Forces the “Disconnect control” object into 'disconnected' state if remote
        disconnection is enabled (control mode > 0).

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Integer", data)

    # Method of remote_disconnect
    @formatResponse
    def act_remote_reconnect(self, data=0):
        """
        Forces the “Disconnect control” object into the 'ready_for_reconnection'
        state if a direct remote reconnection is disabled (control_mode = 1, 3, 5, 6).
        Forces the “Disconnect control” object into the 'connected' state
        if a direct remote reconnection is enabled (control_mode = 2, 4).

        :param data:     十进制数
        :return:         KFResult对象
        """
        return self.actionRequest(2, dec_toHexStr(data, 2), "Integer", data)
