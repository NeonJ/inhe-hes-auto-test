# -*- coding: UTF-8 -*-

import re
import serial
import socket
from comms.DataFormatAPI import KFResult


class PowerControl(object):

    def __init__(self, hostname, circuitIndex, status):
        """
        控制继电器拉合闸

        :param hostname:        中继器IP地址
        :param circuitIndex:    输出回路，取值1~8表示OUT1~OUT8,0表示全部操作，[] 用于组合控制(如[1,2,3])
        :param status:          'on'代表合闸, 'off'代表拉闸
        """
        self.hostname = hostname
        self.circuitIndex = circuitIndex
        self.status = status


    @staticmethod
    def bytesToString(bS):
        """
        将bytes 转为字符串

        :param bS:     bytes
        :return:       转换后的字符

        Example： bytesToString( b'exmaple') -> 'exmaple'
        """
        return str(bS, encoding="utf8")

    @staticmethod
    def readConsole(conn):
        """
        读取 Console 中的数据

        :param conn:   连接对象
        :return:       有数据则返回True, 否则返回False
        """

        responses = PowerControl.bytesToString(conn.read())
        if len(responses) > 0:
            return True
        else:
            return False

    @staticmethod
    def hexsend(string_data=''):
        """
        Create a bytes object from a string of hexadecimal numbers.

        Spaces between two numbers are accepted.
        Example: bytes.fromhex('B9 01EF') -> b'\\xb9\\x01\\xef'.

        :param string_data:        16进制字符串
        :return:                   bytes
        """
        hex_data = bytes.fromhex(string_data)
        return hex_data

    @staticmethod
    def dec2hex(dec):
        """
        将十进制数转为16进制字符串，并返回后两位。如果不够两位则在前面补零

        :param dec:   十进制数
        :return:      16进制字符串
        """
        ret = str(hex(int(dec)))[2:]
        if len(ret) < 2:
            return "0"*(2-len(ret))+ret
        else:
            return ret[-2:]


    def sendCmd(self, msg):
        """
        如果 hostname 为 IP 地址则调用 sendCmdByIp, 否则调用 sendCmdBySerial

        :param msg:          command
        :return:             KFResult对象
        """
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", self.hostname):
            return self.sendCmdByIp(msg)
        else:
            return self.sendCmdBySerial(msg)


    def sendCmdBySerial(self, msg):
        """
        向继电器发送拉合闸指令 (该操作包含了串口连接和断开相关操作)

        :param msg:         拉合闸指令
        :return:            KFResult对象
        """
        try:
            ser = serial.Serial(f"COM{self.hostname}", 9600, timeout=5)
            if ser.isOpen():
                try:
                    ser.write(self.hexsend(msg))
                    if self.readConsole(ser):
                        return KFResult(True, " ")
                    else:
                        return KFResult(False, 'Not responses from switch')
                except Exception as ex:
                    return KFResult(False, ex)
                finally:
                    ser.close()
            else:
                return KFResult(False, f"COM{self.hostname} connection failed")

        except Exception as ex:
            return KFResult(False, ex)


    def sendCmdByIp(self, msg):
        """
        向继电器发送拉合闸指令 (该操作包含了串口连接和断开相关操作)

        :param msg:         拉合闸指令
        :return:            KFResult对象
        """
        s = None
        try:
            s = socket.socket()
            # 设置连接超时为5s
            s.settimeout(5)
            s.connect((self.hostname, 6000))
            s.send(self.hexsend(msg))
            response = s.recv(256)

            # import binascii
            # print(binascii.hexlify(response).decode('ascii'))

            if len(response) > 0:
                return KFResult(True, " ")
            else:
                return KFResult(False, 'Not responses from switch')

        except Exception as ex:
            return KFResult(False, ex)

        finally:
            if s is not None:
                s.close()


    def controlOneCircuit(self):
        """
        生成单路拉合闸指令 (需要一个int)

        :return:　　16进制字符串
        """
        # 0 表示对全部控制口执行操作
        if not int(self.circuitIndex) == 0:
            if self.status.lower() == 'on':
                control_flg = 1
            else:
                control_flg = 0
            return "55 01 %s 00 00 00 0%s %s"%(str(11+control_flg), str(self.circuitIndex), self.dec2hex(103 + int(self.circuitIndex) + control_flg).upper())
        else:
            if self.status.lower() == 'on':
                return "55 01 13 FF FF FF FF 65"
            else:
                return "55 01 13 00 00 00 00 69"


    def controlMultCircuit(self):
        """
        生成多路拉合闸指令 (需要一个list)

        :return:         16进制字符串
        """
        if self.status.lower() == 'on':
            control_flg = 1
        else:
            control_flg = 0

        sums = 0
        for T in self.circuitIndex:
            sums += 2**(int(T)-1)
        return "55 01 %s 00 00 00 %s %s" % (str(14+control_flg), self.dec2hex(sums).upper(), self.dec2hex(106+sums+control_flg).upper())


    def controlCircuit(self):
        """
        输出拉合闸指令

        :return:             KFResult对象
        """
        if isinstance(self.circuitIndex, (int, str)):
            return self.sendCmd(self.controlOneCircuit())

        if isinstance(self.circuitIndex, list):
            return self.sendCmd(self.controlMultCircuit())




# if __name__ == '__main__':
#
#     import time
#     hostname = '192.168.120.227'
#     hostname = '1'
#
#     print(PowerControl(hostname, 7, 'on').controlCircuit().status)
#     time.sleep(5)
#     PowerControl(hostname, 7, 'off').controlCircuit()
#     time.sleep(5)
#
#     PowerControl(hostname, [1, 3], 'on').controlCircuit()
#     time.sleep(5)
#     PowerControl(hostname, [1, 3], 'off').controlCircuit()
#     time.sleep(5)


