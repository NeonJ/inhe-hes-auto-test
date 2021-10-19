# -*- coding: UTF-8 -*-

import threading

class Singleton(object):
    """
    单例模式，确保只有一个实例对象存在
    """

    # 保存ClassDlms对象
    ClassDlms = None
    # 保存从AARE报文中获取的Conformance (ApduParser.py - AAREApduParser)
    Conformance = None

    # 保存Meter项目名称: "-p"
    Project = ""
    # 保证用例名: "-t"
    TestCase = ""
    # 保存Meter通信模式: "-m"
    Communication = ""
    # 保存串口通信ID: "--comPort"
    ComPort = ""
    # 保存连接电表客户端的ID: "--client"
    Client = ""
    # 保存DCU/GPRS的IP地址
    ServerIpAddress = ""
    # 保存DCU上Meter的shortAddr (Sap Id)
    MeterSapId = ""

    # 保存eKey
    EKey = ""
    # 保存aKey
    AKey = ""
    # 保存bKey
    BKey = ""
    # 保存kek
    MasterKey = ""
    # 保存llsKey
    LlsKey = ""
    # 保存hlsKey
    HlsKey = ""
    # 保存Client端的SystemTitle
    SystemTitleClient = ""
    # 保存AARE中返回的 respondingApTitle
    SystemTitleServer = ""
    # 保存服务端公钥
    ServerPublicKeySigning = ""
    # 保存客户端公钥
    ClientPublicKeySigning = ""


    # 保存接收的HDLC分包的数据
    FragmentRecvPackages = list()
    # 标记接收的DLMS分包是否为最后一个
    LastRecvDlmsBlock = 0
    # 保存接收的DLMS分包的数据
    FragmentRecvDlmsData = ""

    # 保存发送的HDLC分包的数据
    FragmentSendPackages = list()
    # 标记发送的DLMS分包是否为最后一个
    LastSendvDlmsBlock = 0
    # 保存发送的DLMS分包的数据
    FragmentSendDlmsData = ""

    # 保存接收的GBT分片数据
    GbtRecvPackages = dict()
    # 保存接收的GBT block Number
    GbtRecvBNList = list()

    # 保存发送的GBT分片数据
    GbtSendPackages = dict()
    # 保存发送的GBT block Number
    GbtSendBNList = list()

    # 用于线程间通信
    Pause = threading.Event()

    # 保存继电器IP地址
    PowerControlHost = ""
    # 保存继电器开关回路
    PowerControlCircuitIndexList = ""

    # 保存firmware在Jenkins服务器上的存储路径
    FwUrl = ""

    # 保存firmware在Jenkins服务器上的存储路径
    UnTag = ""

    # 保存表类型
    MeterType = ""

    # 保存升级位置
    UpgradePosition = ""

    # 保存升级文件信息
    ImgMap = dict()

    # 设置QtInputDialog停留时长 (单位:秒)
    QT_TIMEOUT = 30

    isCheckAction = ""

    SupportedObjects = ""

    # threading lock
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance



if __name__ == '__main__':
    Singleton().SystemTitleServer = 10
    print(Singleton().SystemTitleServer)