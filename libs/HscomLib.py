# -*- coding: UTF-8 -*-

import os
from ctypes import *


class Hscom(object):
    """
        盛迪表台内部有电压量程, 普通表台分四档(60, 120, 240, 480), 跨档的时候会导致掉电
    """

    def __init__(self, **argv):
        self.port = c_byte(int(argv.get('Dev_Port', 1)))
        self.model = c_char_p(str.encode(argv.get('SModel', 'TC-3000D')))
        self.lib =  self.__loadHscomDll()

    @staticmethod
    def __loadHscomDll():
        """
        供应商反馈:
           重新初始化dll, dll就不清楚当前设备的状态, 为了安全会掉电
           否则影响里面量程切换开关的寿命和精度, 带电切换导致拉弧触电性能下降
        """
        hscomDll = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dll\hscom")
        return windll.LoadLibrary(hscomDll)


    def powerOff(self):
        """
        降电压电流
        """
        return self.lib.Power_Off(self.port)


    def powerPause(self):
        """
        降电流, 电压保持
        """
        return self.lib.Power_Pause(self.port)


    def stdMeterRead(self):
        """
        读取指示仪表数据

        :return:    字符串
        """
        data = c_char_p(b'')
        fn = self.lib.StdMeter_Read
        fn.argtypes = [POINTER(c_char_p), c_char_p, c_byte]
        fn(byref(data), self.model, self.port)
        return bytes.decode(data.value).split(",")


    def adJustUI(self, **argv):
        """
        负载点调整

        :param Phase:           相线 (0 ~ 7)
        :param Rated_Volt:      被校表额定电压
        :param Rated_Curr:      被校表额定电流
        :param Rated_Freq:      被校表额定频率
        :param PhaseSequence:   相序 (0-正相序, 1-逆相序)
        :param Revers:          电流方向 (0-正向, 1-反向)
        :param Volt_Per:        负载点电压百分比 (100 表示100%)
        :param Curr_Per:        负载点电流百分比 (100 表示100%)
        :param IABC:            负载点合分元 (H-合元, A-分A, B-分B, C-分C)
        :param CosP:            负载点功率因数 (取值: 1.0, 0.5L, 0.8C ...)
        :return:
        """
        phase = c_byte(argv.get("Phase", 0))
        rated_Volt = c_double(argv.get("Rated_Volt", 57.0))
        rated_Curr = c_double(argv.get("Rated_Curr", 1.0))
        rated_Freq = c_double(argv.get("Rated_Freq", 50.0))
        phaseSequence = c_int(argv.get("PhaseSequence", 0))
        revers = c_int(argv.get("Revers", 0))
        volt_Per = c_double(argv.get("Volt_Per", 100.0))
        curr_Per = c_double(argv.get("Curr_Per", 100.0))
        iABC = str(argv.get("IABC", "A"))
        cosP = str(argv.get("CosP", "1.0"))
        return self.lib.Adjust_UI(phase, rated_Volt, rated_Curr, rated_Freq, phaseSequence, revers, volt_Per, curr_Per, iABC, cosP, self.model, self.port)


    def adJustUI2(self, **argv):
        """
        负载点调整调整 (三相电压电流可分别设置)

        :param Phase:           相线 (0 ~ 7)
        :param Rated_Volt:      被校表额定电压
        :param Rated_Curr:      被校表额定电流
        :param Rated_Freq:      被校表额定频率 (范围: 45 ~ 65)
        :param PhaseSequence:   相序 (0-正相序, 1-逆相序)
        :param Revers:          电流方向 (0-正向, 1-反向)
        :param Volt_Per1:       负载点电压百分比 (100 表示100%)
        :param Volt_Per2:       负载点电压百分比 (100 表示100%)
        :param Volt_Per3:       负载点电压百分比 (100 表示100%)
        :param Curr_Per1:       负载点电流百分比 (100 表示100%)
        :param Curr_Per2:       负载点电流百分比 (100 表示100%)
        :param Curr_Per3:       负载点电流百分比 (100 表示100%)
        :param IABC:            负载点合分元 (H-合元, A-分A, B-分B, C-分C)
        :param CosP:            负载点功率因数 (取值: 1.0, 0.5L, 0.8C ...)
        :return:
        """

        phase = c_byte(argv.get("Phase", 0))
        rated_Volt = c_double(argv.get("Rated_Volt", 57.0))
        rated_Curr = c_double(argv.get("Rated_Curr", 1.0))
        rated_Freq = c_double(argv.get("Rated_Freq", 50.0))
        phaseSequence = c_int(argv.get("PhaseSequence", 0))
        revers = c_int(argv.get("Revers", 0))
        volt_Per1 = c_double(argv.get("Volt_Per1", 100.0))
        volt_Per2 = c_double(argv.get("Volt_Per2", 100.0))
        volt_Per3 = c_double(argv.get("Volt_Per3", 100.0))
        curr_Per1 = c_double(argv.get("Curr_Per1", 100.0))
        curr_Per2 = c_double(argv.get("Curr_Per2", 100.0))
        curr_Per3 = c_double(argv.get("Curr_Per3", 100.0))
        iABC = str(argv.get("IABC", "A"))
        cosP = str(argv.get("CosP", "1.0"))
        return self.lib.Adjust_UI(phase, rated_Volt, rated_Curr, rated_Freq, phaseSequence, revers, volt_Per1, volt_Per2, volt_Per3, curr_Per1, curr_Per2, curr_Per3, iABC, cosP, self.model, self.port)


    def adJustUI4(self, **argv):
        """
        负载点调整调整 (三相电压电流可分别设置)

        :param Phase:           相线 (0 ~ 7)
        :param Rated_Volt:      被校表额定电压
        :param Rated_Curr:      被校表额定电流
        :param Rated_Freq:      被校表额定频率 (范围: 45 ~ 65)
        :param PhaseSequence:   相序 (0-正相序, 1-逆相序)
        :param Revers:          电流方向 (0-正向, 1-反向)
        :param Volt_Per1:       负载点电压百分比 (100 表示100%)
        :param Volt_Per2:       负载点电压百分比 (100 表示100%)
        :param Volt_Per3:       负载点电压百分比 (100 表示100%)
        :param Curr_Per1:       负载点电流百分比 (100 表示100%)
        :param Curr_Per2:       负载点电流百分比 (100 表示100%)
        :param Curr_Per3:       负载点电流百分比 (100 表示100%)
        :param IABC:            负载点合分元 (H-合元, A-分A, B-分B, C-分C)
        :param COSP:            功因对应的角度，如 0,30,60
        :return:
        """

        phase = c_byte(argv.get("Phase", 1))
        rated_Volt = c_double(argv.get("Rated_Volt", 230.0))
        rated_Curr = c_double(argv.get("Rated_Curr", 1.0))
        rated_Freq = c_double(argv.get("Rated_Freq", 50.0))
        phaseSequence = c_int(argv.get("PhaseSequence", 0))
        revers = c_int(argv.get("Revers", 0))
        volt_Per1 = c_double(argv.get("Volt_Per1", 100.0))
        volt_Per2 = c_double(argv.get("Volt_Per2", 100.0))
        volt_Per3 = c_double(argv.get("Volt_Per3", 100.0))
        curr_Per1 = c_double(argv.get("Curr_Per1", 100.0))
        curr_Per2 = c_double(argv.get("Curr_Per2", 100.0))
        curr_Per3 = c_double(argv.get("Curr_Per3", 100.0))
        iABC = str(argv.get("IABC", "H"))
        cosP = c_double(argv.get("COSP", 0.0))
        return self.lib.Adjust_UI4(phase, rated_Volt, rated_Curr, rated_Freq, phaseSequence, revers, volt_Per1, volt_Per2, volt_Per3, curr_Per1, curr_Per2, curr_Per3, iABC, cosP, self.model, self.port)


    def adJustCUST(self, **argv):
        """
        负载点调整 (可任意设定, 四线状态)

        :param Phase:           相线 (0 ~ 7)
        :param Rated_Freq:      被校表额定频率
        :param Volt1:           A 相电压值(V)
        :param Volt2:           B 相电压值(V)
        :param Volt3:           C 相电压值(V)
        :param Curr1:           A 相电流值(V)
        :param Curr2:           B 相电流值(V)
        :param Curr3:           C 相电流值(V)
        :param Uab:             Ua 和 Ub 的夹角
        :param Uac:             Ua 和 Uc 的夹角
        :param Ang1:            A 相电压电流夹角
        :param Ang2:            B 相电压电流夹角
        :param Ang3:            C 相电压电流夹角
        :return:
        """
        phase = c_byte(argv.get("Phase", 0))
        rated_Freq = c_double(argv.get("Rated_Freq", 50.0))
        volt1 = c_double(argv.get("Volt1", 0))
        volt2 = c_double(argv.get("Volt2", 0))
        volt3 = c_double(argv.get("Volt3", 0))
        curr1 = c_double(argv.get("Curr1", 0))
        curr2 = c_double(argv.get("Curr2", 0))
        curr3 = c_double(argv.get("Curr3", 0))
        uab = c_double(argv.get("Uab", 0))
        uac = c_double(argv.get("Uac", 0))
        ang1 = c_double(argv.get("Ang1", 0))
        ang2 = c_double(argv.get("Ang2", 0))
        ang3 = c_double(argv.get("Ang3", 0))
        return self.lib.Adjust_CUST(phase, rated_Freq, volt1, volt2, volt3, curr1, curr2, curr3, uab, uac, ang1, ang2, ang3, self.model, self.port)


    def setHarmonicData(self, **argv):
        """
        设置输出谐波数据
            原函数'Set_Harmnoic_Data' 接收三组谐波定义, 调用的语言不同, 可能会导致指针混乱
            新函数'Set_Harmnoic_Data1' 接收一组谐波定义 (是一个隐藏函数)

        :param HAng:        谐波相位, 取值范围: (0 ~ 360)
        :param HNum:        谐波次数(3、5、7 次可任意叠加)
        :param HVolt:       电压谐波含量(总含量不能超40%), 取值范围: (0 ~ 40)
        :param HCur:        电流谐波含量(总含量不能超40%), 取值范围: (0 ~ 40)
        :return:
        """
        hAng = c_double(argv.get('HAng', 0))
        hNum = c_int(argv.get('hNum', 3))
        hVolt = c_double(argv.get('HVolt', 10))
        hCur = c_double(argv.get('HCur', 10))
        return self.lib.Set_Harmnoic_Data1(hAng, hNum, hVolt, hCur)



if __name__ == '__main__':

    hscom = Hscom(Dev_Port=1)
    hscom.adJustUI4(Curr_Per1=25, Curr_Per2=25, Curr_Per3=25)

    # print(hscom.adJustUI(Phase=0, IABC='H'))
    # print(hscom.setHarmonicData())
    # print(hscom.stdMeterRead())
    #
    #
    # print(hscom.adJustCUST(Volt1=110))
    # print(hscom.stdMeterRead())
    #
    # print(hscom.powerOff())
    # print(hscom.stdMeterRead())