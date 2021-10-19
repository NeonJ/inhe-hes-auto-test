# -*- coding: UTF-8 -*-

import os
PTSProtocol = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dll\PTS.Protocol.dll")
PTSModel = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dll\PTS.Model.dll")

import clr
clr.AddReference(PTSProtocol)
clr.AddReference(PTSModel)

from PTS.Protocol.Manufacture import KaifaManufactureCommon, KaifaManuTCP
from PTS.Model.Model import *


import yaml
from libs.Singleton import Singleton
from comms.DataFormatAPI import KFResult
from comms.KFLog import *


class KaifaCmcs(object):
    """
    包含CMCS的相关操作
    """
    def __init__(self, **argv):
        self.argv = argv
        self.yml = None
        self.classCmcs = None
        self.retryNum = 3

        self.connect()


    def configTcp(self):
        """
        配置TCP连接参数
        """
        self.classCmcs = KaifaManuTCP()

        ip = ''
        port = ''
        sapId = ''

        if Singleton().Communication.upper() == 'DCU':
            ip = self.argv.get('DCU_ServerIpAddress', Singleton().ServerIpAddress) or self.yml['DCU']['ServerIpAddress']
            port = self.argv.get('DCU_ServerIpPort', self.yml['DCU']['ServerIpPort'])
            sapId = self.argv.get('DCU_MeterSapId', Singleton().MeterSapId) or self.yml['DCU']['MeterSapId']

        if Singleton().Communication.upper() == 'GPRS':
            ip = self.argv.get('GPRS_ServerIpAddress', Singleton().ServerIpAddress) or self.yml['GPRS']['ServerIpAddress']
            port = self.argv.get('GPRS_ServerIpPort', self.yml['GPRS']['ServerIpPort'])
            sapId = 1

        self.classCmcs.SetParams('IP', ip)
        self.classCmcs.SetParams('Port', port)
        self.classCmcs.SetParams('SAP', sapId)


    def configHDLC(self):
        """
        配置HDLC连接参数
        """
        self.classCmcs = KaifaManufactureCommon()
        self.classCmcs.SetParams("PortName", "COM" + str(self.argv.get('HDLC_comPort', Singleton().ComPort) or self.yml['HDLC']['comPort']))
        self.classCmcs.SetParams("BaudRate", self.argv.get('HDLC_baudrate', self.yml['HDLC']['baudrate']))
        self.classCmcs.SetParams("UseIEC", self.argv.get('HDLC_useIEC', self.yml['HDLC']['useIEC']))
        self.classCmcs.SetParams("ServerAddressSize", self.argv.get('HDLC_serverAddressSize', self.yml["HDLC"]["serverAddressSize"]))
        self.classCmcs.SetParams("ServerLowerMACAddressValue", self.argv.get('HDLC_serverLowerMacAddress', self.yml["HDLC"]["serverLowerMacAddress"]))
        self.classCmcs.SetParams("ServerUpperMACAddressValue", self.argv.get('HDLC_serverUpperMacAddress', self.yml["HDLC"]["serverUpperMacAddress"]))
        self.classCmcs.SetParams("ClientMacAddress", self.argv.get('HDLC_Public_clientMacAddress', self.yml["HDLC"]['Public']["clientMacAddress"]))
        self.classCmcs.SetParams("StopBits", self.argv.get('stopBits', 1))
        self.classCmcs.SetParams("TimeOut", self.argv.get('timeOut', 5000))
        self.classCmcs.SetParams("Parity", self.argv.get('parity', 0))
        self.classCmcs.SetParams("DataBits", self.argv.get('dataBits', 8))
        self.classCmcs.SetParams("ReadTimeout", self.argv.get('readTimeout', 1000))
        self.classCmcs.SetParams("ReTryTime", self.argv.get('reTryTime', 1))


    def connect(self):
        """
        连接CMCS
        """
        # 获取全局配置文件路径
        project = Singleton().Project.lower()

        # 读取项目参数配置文件
        clientId = self.argv.get('client', Singleton().Client)
        if clientId is None:
            clientId = 1
        conf = project + '_client' + str(clientId)
        filename = os.path.join(os.path.dirname(__file__), f"../conf/ConnParam/{project}/{conf}.yaml")
        with open(filename, encoding="utf-8") as f:
            self.yml = yaml.load(f, Loader=yaml.FullLoader)

        # 不同的连接方式选择不同的初始化方法
        if Singleton().Communication.upper()  == 'HDLC':
            self.configHDLC()
        elif Singleton().Communication.upper() in ['DCU', 'GPRS']:
            self.configTcp()
        else:
            raise Exception(f"Not recognized communication mode: {Singleton().Communication}")


        info(f"** SYSTEM INFO ** : CMCS Connecting Meter (by {Singleton().Communication})...")
        # connect meter
        connected = False
        for i in range(int(self.retryNum) + 1):
            try:
                result = self.classCmcs.ConnectToMeter()
                if result:
                    info("** SYSTEM INFO ** : CMCS Connect Meter Succeed")
                    connected = True
                    break
                else:
                    error("** SYSTEM ERROR ** : CMCS Connect Meter Failed")
            except:
                error("** SYSTEM ERROR ** : CMCS Connect Meter Failed")

        if not connected:
            raise Exception("** SYSTEM ERROR ** : CMCS Connect Meter Failed")


    def disconnect(self):
        """
        断开CMCS连接
        """
        try:
            self.classCmcs.DisConnectMeter()
            info("** SYSTEM INFO ** : CMCS DisConnect Meter Succeed")
        except AttributeError as ex:
            error(f"** SYSTEM ERROR ** : CMCS disconnect failed!\n{ex}")


    def readById(self, hexId):
        """
        基于16进制ID获取值

        :param hexId:  16进制字符串形式的ID
        :return:       KFResult对象
        """
        result = self.classCmcs.ReadSingleID(hexId, "")
        info(f"CMCS: readById(hexId={hexId}), result={result}")
        return KFResult(result[0], result[1])


    def readByAddr(self, resType, address, length):
        """
        基于绝对地址获取值

        :param resType:  资源类型
        :param address:  起始地址
        :param length:   地址长度
        :return:         KFResult对象
        """
        result = self.classCmcs.ReadAbsoluteAddress(resType, address, length, "")
        info(f"CMCS: readByAddr(resType={resType}, address={address}, length={length}), result={result}")
        return KFResult(result[0], result[1])


    def writeById(self, hexId, data):
        """
        基于16进制ID设置值

        :param hexId:  16进制字符串形式的ID
        :param data:   待设置的值
        :return:       KFResult对象
        """
        result = self.classCmcs.WriteSingleID(hexId, data)
        info(f"CMCS: writeById(hexId={hexId}, data={data}), result={result}")
        return KFResult(result, "")


    def writeByAddr(self, resType, address, length, data):
        """
        基于绝对地址设置值

        :param resType: 资源类型
        :param address: 起始地址
        :param length:  地址长度
        :param data:    待设置的值
        :return:        KFResult对象
        """
        result = self.classCmcs.WriteAbsoluteAddress(resType, address, length, data)
        info(f"CMCS: writeByAddr(resType={resType}, address={address}, length={length}, data={data}), result={result}")
        return KFResult(result, "")


    def actionById(self, hexId):
        """
        基于16进制ID执行方法

        :param hexId:  16进制字符串形式的ID
        :return:       KFResult对象
        """
        result = self.classCmcs.RunAction(hexId)
        info(f"CMCS: actionById(hexId={hexId}), result={result}")
        return KFResult(result, "")



def disconnectCmcs(conn):
    """
    断开设备连接

    :param conn:  连接对象
    """
    if conn is not None:
        if isinstance(conn, KaifaCmcs):
            conn.disconnect()







if __name__ == '__main__':

    cmcs = KaifaCmcs(GPRS_ServerIpAddress='10.183.100.13')
    result = cmcs.readById("2232")
    print(result.status, result.result)

    result = cmcs.readById("2239")
    print(result.status, result.result)
    cmcs.disconnect()