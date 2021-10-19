# -*- coding: UTF-8 -*-

import re
import time
import serial
from comms.KFLog import *


class Serial(object):

    def __init__(self, **argv):
        self.comPort = argv['comPort']
        self.baudrate = int(argv.get("baudrate", 9600))
        self.bytesize = int(argv.get("bytesize", 8))
        self.parity = argv.get("parity", 'N')
        self.stopbits = int(argv.get("stopbits", 1))
        self.timeout = int(argv.get("timeout", 2))
        self.prompt = argv.get("prompt", '7E')
        self.conn = None


    def connect(self):
        """
        串口连接
        """
        try:
            self.conn = serial.Serial('COM' + str(self.comPort), baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout)
        except Exception as ex:
            error(f"Serial connect failed! -- {ex}")


    def disconnect(self):
        """
        断开串口连接
        """
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as ex:
                error(ex)


    @staticmethod
    def bytesToHex(bH):
        """
        将16进制字符串按每两位用空格分开

        :param bH:      16进制字符串
        :return:        分割后的字符串
        """
        lst = re.findall(r'([0-9a-fA-F]{2})', bH.upper())
        return " ".join(lst)


    # def readConsole(self):
    #     responses = [self.conn.read().hex()]
    #     # 轮询读取512次
    #     for loop in range(3):
    #         resps = self.conn.readline().hex()
    #         responses.append(resps)
    #
    #         # 遇到提示符时退出
    #         if resps.find(self.prompt) > -1:
    #             break
    #     return self.bytesToHex("".join(responses))


    def readConsole(self):
        """
        读取Console内容
        """
        # 轮询5次
        for i in range(5):
            # 每次读取之前等待 1s
            time.sleep(1)
            # 判断缓存区中是否有数据
            if self.conn.in_waiting > 0:
                resps = self.conn.read(self.conn.in_waiting).hex()
                if resps.lower().find(self.prompt.lower()) > -1:
                    return self.bytesToHex(resps)


    def sendCmd(self, cmdline, dataType="hex"):
        """
        向串口下发指令, 需要预先连接

        :param cmdline:    待下发的指令, 默认为16进制字符串
        :param dataType:   指令的数据类型, 支持`hex` 和`str`, 默认为`hex`
        :return:           None
        """
        if self.conn is None:
            self.connect()

        info(f"** Send  to  console: {cmdline}")
        if dataType.lower() == "hex":
            self.conn.write(bytes.fromhex(cmdline.replace(" ", "")))
        else:
            self.conn.write(bytes(cmdline.strip(), encoding="utf8"))
        self.conn.flush()
        info(f"** Recv from console: {self.readConsole()}")


    def sendCmdOnce(self, cmdline, dataType="hex"):
        """
        向串口下发单次命令 (该方法包含了串口的连接和断开)

        :param cmdline:    待下发的指令, 默认为16进制字符串
        :param dataType:   指令的数据类型, 支持`hex` 和`str`, 默认为`hex`
        :return:           None
        """
        self.connect()
        self.sendCmd(cmdline, dataType)
        self.disconnect()
