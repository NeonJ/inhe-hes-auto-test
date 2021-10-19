# -*- coding: UTF-8 -*-

import re
import struct
import threading
import serial
from comms.KFLog import *
import time
from comms import *
from libs.Constants import *


class YCBench(object):

    def __init__(self, **argv):
        self.comPort = argv['comPort']
        self.phase = int(argv['phase'])
        self.nominalVolt = float(argv['nominalVolt'])
        self.nominalCurr = float(argv['nominalCurr'])
        self.maxCurr = float(argv['maxCurr'])
        self.meterConstant = float(argv.get('meterConstant', 1600))
        self.isInitialBench = argv.get('isInitialBench', True)

        self.ser = None
        self.connect(self.isInitialBench)

    @staticmethod
    def splitHexDataWithSpace(hexData):
        """
        将16进制字符串按两位一组，并用空格分开

        :param hexData:       16进制字符串
        :return:              分割后的字符串

        Example: splitHexDataWithSpace("39AB62") -> '39 AB 62'
        """
        ret = re.findall(r'[0-9a-zA-Z]{2}', hexData)
        return " ".join(ret)

    @staticmethod
    def ascii_toHex(s):
        """
        将目标字符串对应的ASCII码转为16进制字符串

        :param s:    ascii 字符串
        :return:     转换后的字符串

        Example: ascii_toHex("A12456") -> '41 31 32 34 35 36'
        """
        list_h = []
        for c in s:
            list_h.append(str(hex(ord(c))[2:]))
        return YCBench.splitHexDataWithSpace(''.join(list_h).upper())

    @staticmethod
    def bytesToString(byte):
        """
        将bytes 转为字符串

        :param byte:   bytes
        :return:       转换后的字符

        Example： bytesToString( b'exmaple') -> 'exmaple'
        """
        return str(byte, encoding='utf-8')


    def connect(self, isInitialBench=True, isCheckConnection=False):
        """
        连接表台
        :param isInitialBench:        是否设置初始化表台参数
        :param isCheckConnection:     是否检查串口连接

        :return:
        """
        try:
            # 尝试断开串口连接
            if self.ser is not None:
                try:
                    self.ser.close()
                except AttributeError:
                    pass

            # 重新连接串口
            comPort = "COM" + str(self.comPort).lower().replace("com", "")
            self.ser = serial.Serial(comPort, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)

            # 检查串口连接是否可用
            if isCheckConnection:
                if not self.ser.is_open:
                    raise Exception("Connecting YC-Bench Failed")

            # suppression overload alarm
            self.overloadResetting()

            # handshake
            self.handShake()

            # initial bench
            if isInitialBench:
                cmdlist = f"I{self.phase} {self.nominalVolt} {self.nominalCurr} {self.maxCurr} {self.meterConstant}"
                self.sendCmd(cmdlist)

        except Exception as ex:
            self.ser.close()
            raise Exception(ex)


    def sendCmd(self, cmdlist, response=False, printCmd=True, length=-1):
        """
        向表台发送命令

        :param cmdlist:     命令字符串
        :param response:    是否等待返回结果，默认False不等待
        :param printCmd:    是否打印command
        :return:            如果response为True则返回命令结果，否则不返回内容
        """
        try:
            if self.ser is not None and self.ser.is_open:
                # drop cached buffer
                self.ser.readline() if response else None

                # send command
                cmd = bytes.fromhex(self.ascii_toHex(cmdlist) + ' 0D')
                info(f"Send Command to YCBench: {cmd}") if printCmd else None
                self.ser.write(cmd)

                # read data
                empytNum = 0
                ret = bytes()
                if response:
                    for i in range(64):
                        byte = self.ser.read()
                        ret += byte

                        # 达到条件退出
                        if byte.hex().upper() == '0D':
                            if length == -1 or len(ret) == length:
                                break

                        # 累计读取数据为空3次就退出
                        if byte is None:
                            empytNum += 1
                            if empytNum > 3:
                                raise Exception("read bench data error")

                    return ret
        except Exception as ex:
            error(ex)


    def disconnect(self, isPowerPause=False):
        """
        断开表台

        :return:    None
        """
        if self.ser is not None:
            try:
                if isPowerPause:
                    self.powerPause()
                else:
                    self.resetBench()
                self.ser.close()
                self.ser = None
            except Exception as ex:
                error(ex)


    def handShake(self):
        """
        握手, 用于判断表台连接状态

        :return:    'H1' 表示握手成功
        """
        cmdlist = f'H0'
        ret = self.sendCmd(cmdlist, response = True)
        if self.bytesToString(ret).strip() != 'H1':
            raise Exception("Connect YCBench via serial failed (not response !!!)")


    def overloadResetting(self):
        """
        过载复位; 实现方式: 启用一个线程, 每隔10s主动向表台下发过载复位指令

        :return:
        """
        def reset():
            while True:
                time.sleep(10)
                self.sendCmd("r", printCmd=False)
        t = threading.Thread(target=reset, daemon=True)
        t.start()


    def setVolt(self, volt):
        """
        设置电压

        :param volt:  数值为相对于标称电压的百分数，100% 对应标称电压(self.nominalVolt)
        :return:      None
        """
        current_volt = self.nominalVolt * volt/100
        info(f"Set Volt: {current_volt}")
        cmdlist = f'V{float(volt)}'
        self.sendCmd(cmdlist)


    def setCurr(self, curr):
        """
        设置电流

        :param curr:  数值为相对于标称电流的百分数，100% 对应标称电流(self.nominalCurr)
        :return:      None
        """
        current_curr = self.nominalCurr * curr/100
        info(f"Set Curr: {current_curr}")
        cmdlist = f'A{float(curr)}'
        self.sendCmd(cmdlist)


    def setCosP(self, cosP):
        """
        设置功率因数

        :param cosP:    可选值有: '0.25L', '0.5L', '0.8L' ... '-0.25C', '-0L' (共计16 组可选值)
        :return:        None
        """
        info(f"Set Phase angle: {YCCosPMap[cosP.upper()]}")
        CosPMap = {
            '0.25L'     : 0,        # 75.52249
            '0.5L'      : 1,        # 60.00000
            '0.8L'      : 2,        # 36.86990
            '1.0'       : 3,        # 0.00000
            '0.8C'      : 4,        # -36.86990
            '0.5C'      : 5,        # -60.00000
            '0.25C'     : 6,        # -75.52249
            '0L'        : 7,        # 90.0000
            '-0.25L'    : 8,        # 75.52249 + 180 = 255.52249
            '-0.5L'     : 9,        # 60.0000 + 180 = 240
            '-0.8L'     : 10,       # 36.86990 + 180 = 216.86990
            '-1.0'      : 11,       # 0 + 180 = 180
            '-0.8C'     : 12,       # -36.86990 + 180 = 143.1301
            '-0.5C'     : 13,       # -60.0000 + 180 = 120
            '-0.25C'    : 14,       # -75.52249 + 180 = 104.47751
            '-0L'       : 15,       # 90 + 180 = 270
        }
        cmdlist = f'P{CosPMap[cosP.upper()]}'
        self.sendCmd(cmdlist)


    def setFreq(self, freq):
        """
        设置频率

        :param freq:    数值为频率值
        :return:        None
        """
        info(f"Set frequency: {float(freq)}")
        cmdlist = f'F{float(freq)}'
        self.sendCmd(cmdlist)


    def setIABC(self, IABC):
        """
        设置合分元

        :param IABC:    可选值有: A, B, C, I (分别代表'A'元, 'B'元, 'C'元, '合'元)
        :return:        None
        """
        info(f"Set up phase position: {IABC}")
        IabcMap = {
            'A' : 0,
            'B' : 1,
            'C' : 2,
            'I' : 3,
        }

        cmdlist = f'C{IabcMap[IABC.upper()]}'
        self.sendCmd(cmdlist)


    def setStablePeriod(self, seconds):
        """
        设置稳定时间

        :param seconds:     数值为稳定时间，单位秒
        :return:            None
        """
        cmdlist = f'T{int(seconds)}'
        self.sendCmd(cmdlist)


    def readBenchData(self):
        """
        读取表台数据

        :return:   表台数据
        """
        isOK = False
        for i in range(3):
            try:
                cmdlist = 'M'
                ret = self.sendCmd(cmdlist, response=True, length=51)
                # error(f'readBenchData: {len(ret)}, {ret.hex().upper()}')
                (_, volt1, volt2, volt3, curr1, curr2, curr3, ang1, ang2, ang3, power, volt, curr, phase, _) = struct.unpack('=1c12f1c1c', ret)
                isOK = True
                return {
                    "volt1": "%.2f" % volt1,
                    "volt2": "%.2f" % volt2,
                    "volt3": "%.2f" % volt3,
                    "curr1": "%.2f" % curr1,
                    "curr2": "%.2f" % curr2,
                    "curr3": "%.2f" % curr3,
                    "ang1": "%.2f" % ang1,
                    "ang2": "%.2f" % ang2,
                    "ang3": "%.2f" % ang3,
                    "power": "%.2f" % power,
                    "volt": "%.2f" % volt,
                    "curr": "%.2f" % curr,
                    "phase": int(phase),
                }
            except struct.error as ex:
                if i == 3 and not isOK:
                    raise Exception(ex)

    def powerOff(self):
        """
        降电压电流
        """
        self.setIABC('I')
        self.setCurr(0)
        self.setVolt(0)


    def resetBench(self):
        """
        重置表台设置, 删除电压、电流、相角、谐波数据参数

        :return:
        """
        self.setIABC('I')
        self.setVolt(0)
        self.setCurr(0)
        self.setCosP('1.0')
        self.setHarmonic(0)

    def powerPause(self):
        """
        重置表台设置, 删除电流、相角、谐波数据参数, 电压保持
        """
        self.setIABC('I')
        self.setVolt(100)
        self.setCurr(0)
        self.setCosP('1.0')
        # self.setHarmonic(0)    # 修改谐波会让电表重新上电

    def setHarmonic(self, num, percent=10, ang=0):
        """
        设置并应用谐波

        :param num:         谐波次数, 取值范围1~31; 0 表示删除谐波数据
        :param percent:     谐波的幅度相对于基波的百分数, 取值范围 0~40
        :param ang:         谐波的相位
        :return:
        """
        info(f"Set harmonic: num={num}, percent={percent}%, ang={ang}")
        # 删除历史谐波数据
        self.sendCmd('hD0')
        # 设置谐波参数
        cmdlist = f'hD{int(num)} {int(percent)} {float(ang)}'
        self.sendCmd(cmdlist)
        # 应用谐波 (3F 表示六个通道全部应用)
        self.sendCmd('hA3F')


    def switchHarmonic(self, channel):
        """
        波表切换

        :param channel:  可选值有: IA, IB, IC, UA, UB, UC
                         指定单个谐波通道时:  IA \ IB \ IC \ UA \ UB \ UC
                         指定多个谐波通道时:  IA+IB+IC, IA+UA, IA+IB+IC+UA+UB+UC
        :return:
        """
        info(f"Switch harmonic: channel={channel}")
        lst = channel.upper().replace(" ", "").split("+")
        binStr = '0'
        for item in ['UC', 'IC', 'UB', 'IB', 'UA', 'IA']:
            if item in lst:
                binStr += '1'
            else:
                binStr += '0'
        hexStr = hex(int(binStr, 2)).replace('0x', '')
        cmdlist = f'hT{hexStr}'
        self.sendCmd(cmdlist)


def disconnectBench(conn, isPowerPause=False):
    """
    断开表台的串口连接, 并重置所有参数

    :param conn:
    :return:
    """
    if isinstance(conn, YCBench):
        conn.disconnect(isPowerPause)


def initYCBench(**kwargs):
    """
        使用指定参数给初始化表台

    :param kwargs:
        comPort: 串口号
        phase： 负载类型
        nominalVolt： 电压
        nominalCurr： 电流
        maxCurr： 最大电流
        freq：频率
    :return:
    """
    comPort = kwargs.get("comPort", "1")
    phase = kwargs.get("phase", 2)
    nominalVolt = kwargs.get("nominalVolt", 230)
    nominalCurr = kwargs.get("nominalCurr", 5)
    maxCurr = kwargs.get("maxCurr", 5)
    freq = kwargs.get("freq", 60)

    ycBench = YCBench(comPort=comPort, phase=phase, nominalVolt=nominalVolt, nominalCurr=nominalCurr, maxCurr=maxCurr)
    ycBench.setVolt(100)
    ycBench.setFreq(freq)
    timedWait(10, "Wait Bench Stable...")  # 等待电表稳定
    return ycBench



if __name__ == '__main__':


    '''CosPMap = {
            '0.25L'     : 0,        # 75.52249
            '0.5L'      : 1,        # 60.00000
            '0.8L'      : 2,        # 36.86990
            '1.0'       : 3,        # 0.00000
            '0.8C'      : 4,        # -36.86990
            '0.5C'      : 5,        # -60.00000
            '0.25C'     : 6,        # -75.52249
            '0L'        : 7,        # 90.0000
            '-0.25L'    : 8,        # 75.52249 + 180
            '-0.5L'     : 9,        # 60.0000 + 180
            '-0.8L'     : 10,       # 36.86990 + 180
            '-1.0'      : 11,       # 0 + 180
            '-0.8C'     : 12,       # -36.86990 + 180
            '-0.5C'     : 13,       # -60.0000 + 180
            '-0.25C'    : 14,       # -75.52249 + 180
            '-0L'       : 15,       # 90 + 180
        }
        '''
    yc = YCBench(comPort='1', phase=2, nominalVolt=230, nominalCurr=5, maxCurr=10)

    yc.setVolt(100)
    yc.setCurr(100)
    time.sleep(5)


    # yc.setHarmonic(3)
    # yc.switchHarmonic('IA+IB+UC')
    #
    # time.sleep(120)
    # disconnectBench(yc)