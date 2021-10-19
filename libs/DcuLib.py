#-*- coding:utf-8 -*-

import yaml
from .Delegate import *
from libs.Singleton import Singleton


class Dcu(object):

    def __init__(self, **argv):
        self.argv = argv
        self.apduParser = ApduParser()
        self.classDlms = ClassDLMS()
        self.yml = None
        # 执行连接
        self.connect()


    def configInfrared(self):
        """
        配置HDLC模式连接参数
        """
        info("** SYSTEM INFO ** : Connecting via HDLC...")

        # 配置红外连接模式
        self.classDlms.SetCommunicationType(0)
        self.classDlms.iConnectType = 0

        # 配置串口参数
        self.classDlms.CommunicationParam.CommPortParam.PortNumber = self.argv.get('HDLC_comPort', Singleton().ComPort) or self.yml['HDLC']['comPort']
        self.classDlms.CommunicationParam.CommPortParam.Echoing = self.argv.get('HDLC_echoing', self.yml['HDLC']['echoing'])
        self.classDlms.CommunicationParam.IECParam.MaxBaud = self.argv.get('HDLC_baudrate', self.yml['HDLC']['baudrate'])

        # HDLC params
        self.classDlms.CommunicationParam.HDLCParam.OpeningUsesIEC = self.argv.get('HDLC_useIEC', self.yml['HDLC']['useIEC'])
        self.classDlms.CommunicationParam.HDLCParam.ServerAddressSize = self.argv.get('HDLC_serverAddressSize', self.yml["HDLC"]["serverAddressSize"])
        self.classDlms.CommunicationParam.HDLCParam.ServerUpperMACAddressValue = self.argv.get('HDLC_serverUpperMacAddress', self.yml["HDLC"]["serverUpperMacAddress"])
        self.classDlms.CommunicationParam.HDLCParam.ServerLowerMACAddressValue = self.argv.get('HDLC_serverLowerMacAddress', self.yml["HDLC"]["serverLowerMacAddress"])
        self.classDlms.CommunicationParam.HDLCParam.InactivityTimeout = self.argv.get('HDLC_inactivityTimeout', self.yml["HDLC"]["inactivityTimeout"])
        self.classDlms.CommunicationParam.HDLCParam.InterFrameTimeout = self.argv.get('HDLC_interFrameTimeout', self.yml["HDLC"]["interFrameTimeout"])
        self.classDlms.CommunicationParam.HDLCParam.ResponseTimeout = self.argv.get('HDLC_responseTimeout', self.yml["HDLC"]["responseTimeout"])


    def configIp(self):
        """
        配置GPRS模式连接参数
        """
        info("** SYSTEM INFO ** : Connecting via IP...")

        # 配置Remote通信模式
        self.classDlms.SetCommunicationType(2)    # 2-网络直连走Wrap协议模式
        self.classDlms.iConnectType = 0

        # 配置Remote通信参数
        self.classDlms.CommunicationParam.GprsParam.ServerIpAddress = self.argv.get("DCU_ServerIpAddress", self.yml['DCU']['ServerIpAddress'])
        self.classDlms.CommunicationParam.GprsParam.ServerIpPort = str(self.argv.get("DCU_ServerIpPort", self.yml['DCU']['ServerIpPort']))
        self.classDlms.CommunicationParam.GprsParam.DestinedAddr = self.argv.get("DCU_SapId", self.yml['DCU']['SapId'])



    def connectMeterByPublic(self, communication):
        """
        使用Public 账号连接电表

        :param communication:     连接方式（HDLC/IP）
        """
        if communication == "HDLC":
            self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress = self.argv.get('DCU_Public_clientMacAddress', self.yml["DCU"]['Public']["clientMacAddress"])
        if communication == "IP":
            self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("DCU_Public_SourceAddr", self.yml['DCU']['Public']['clientMacAddress'])

        # AARQ params
        self.classDlms.CommunicationParam.AARQParam.UsageGBT = self.argv.get('DCU_usageGBT', self.yml["DCU"]["usageGBT"])
        self.classDlms.CommunicationParam.AARQParam.ClientMaxReceivePDUSize = self.argv.get('DCU_clientMaxReceivePDUSize', self.yml["DCU"]["clientMaxReceivePDUSize"])
        self.classDlms.CommunicationParam.AARQParam.CallingApTitle = self.argv.get('DCU_systemTitleClient', self.yml["DCU"]["systemTitleClient"])
        self.classDlms.CommunicationParam.AARQParam.CallingAeQualifier = self.argv.get('DCU_callingAeQualifier', self.yml["DCU"]["callingAeQualifier"])
        self.classDlms.CommunicationParam.AARQParam.ApplicationContextName = self.argv.get('DCU_Public_applicationContextName', self.yml["DCU"]['Public']["applicationContextName"])
        self.classDlms.CommunicationParam.AARQParam.AlgorithmType = MechanismEnum.get(self.argv.get('DCU_Public_mechanism', self.yml["DCU"]['Public']["mechanism"]))

        protectionType = self.argv.get('DCU_Public_protectionType', self.yml["DCU"]['Public']["protectionType"])
        if protectionType is not None:
            self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType = GeneralProtectionTypeEnum.get(protectionType)
            self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey = UsageDedicatedKeyEnum.get(protectionType)

        accessLevel = self.argv.get('DCU_Public_accessLevel', self.yml["DCU"]['Public']["accessLevel"])
        self.classDlms.CommunicationParam.AARQParam.MechanismName = accessLevel
        if accessLevel == "No Security":
            self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = False
        else:
            self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = True

        # Public Account Connect
        res = self.classDlms.DeviceConnect()
        if int(res) == 1:
            info("** SYSTEM INFO ** : Public Connect Meter Success")
        else:
            error("** SYSTEM INFO ** : Public Connect Meter Failed, Error reason: %s" % ConnectStatus[str(res)])
            raise Exception("Public Connect Meter Failed, Error reason: %s" % ConnectStatus[str(res)])


        projectName = Singleton().Project
        if projectName.lower() == "cetus02":
            # 获取Cetus电表的Invocation Counter
            self.classDlms.ClassActionFrameCounter.OBISCode = "00002B010" + str(self.yml["DCU"]["Admin"]["clientMacAddress"]) + "FF"
            self.classDlms.ClassActionFrameCounter.MethodID = 1
            if self.classDlms.ClassActionFrameCounter.ExcuteCommand():
                self.classDlms.FrameCounter = self.classDlms.ClassActionFrameCounter.FrameCounter
                info("** SYSTEM INFO ** : Invocation Counter: %s" % str(self.classDlms.FrameCounter))
            else:
                error("** SYSTEM INFO ** : Get Invocation Counter Failed")
                self.classDlms.DeviceDisconnect(True)
                return

        # elif projectName.lower() == "amber51":
        else:
            # 获取 Invocation Counter
            self.classDlms.ClassData.OBISCode = "00002B0100FF"
            self.classDlms.ClassData.AttributeID = 2
            if self.classDlms.ClassData.GetRequest():
                self.classDlms.FrameCounter = self.classDlms.ClassData.Value
                info("** SYSTEM INFO ** : Invocation Counter: %s" % str(self.classDlms.FrameCounter))
            else:
                error("** SYSTEM INFO ** : Get Invocation Counter Failed")
                self.classDlms.DeviceDisconnect(True)
                return

        # 断开 Public 连接
        # self.classDlms.DlmsDisconnect()       # Dlms协议层断开
        self.classDlms.DeviceDisconnect(True)   # 物理层断开
        info("** SYSTEM INFO ** : Public Connect Disconnect")


    def connectMeterByAdmin(self, communication):
        """
        使用 Admin 账号连接电表

        :param communication:     连接方式（HDLC/IP）
        """
        if communication == "HDLC":
            self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress = self.argv.get('HDLC_Admin_clientMacAddress', self.yml["HDLC"]['Admin']["clientMacAddress"])
        if communication == "IP":
            self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("DCU_Admin_clientMacAddress", self.yml['DCU']['Admin']['clientMacAddress'])

        # AARQ params
        self.classDlms.CommunicationParam.AARQParam.ApplicationContextName = self.argv.get('DCU_Admin_applicationContextName', self.yml["DCU"]['Admin']["applicationContextName"])
        self.classDlms.CommunicationParam.AARQParam.AlgorithmType = MechanismEnum.get(self.argv.get('DCU_Admin_mechanism', self.yml["DCU"]['Admin']["mechanism"]))

        protectionType = self.argv.get('DCU_Admin_protectionType', self.yml["DCU"]['Admin']["protectionType"])
        if protectionType is not None:
            self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType = GeneralProtectionTypeEnum.get(protectionType)
            self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey = UsageDedicatedKeyEnum.get(protectionType)
        # Signing 数据报文签名保护
        self.classDlms.bGeneralCiphering_Signing = self.argv.get('DCU_Admin_signing', self.yml["DCU"]['Admin']["signing"])

        accessLevel = self.argv.get('DCU_Admin_accessLevel', self.yml["DCU"]['Admin']["accessLevel"])
        if accessLevel is not None:
            self.classDlms.CommunicationParam.AARQParam.MechanismName = accessLevel
            if accessLevel == "No Security":
                self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = False
            else:
                self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = True

        # Key params
        self.classDlms.CommunicationParam.SecInfo.UsingLlsKey = self.argv.get('DCU_llsKey', self.yml["DCU"]["llsKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingHlsKey = self.argv.get('DCU_hlsKey', self.yml["DCU"]["hlsKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingAuthenticationKey = self.argv.get('DCU_aKey', self.yml["DCU"]["aKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingEncryptionKey = self.argv.get('DCU_eKey', self.yml["DCU"]["eKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingMasterKey = self.argv.get('DCU_kekKey', self.yml["DCU"]["kekKey"])

        # SC params
        self.classDlms.SC_SecurityControl = self.argv.get('DCU_Admin_securityPolicy', self.yml["DCU"]['Admin']["securityPolicy"])

        # HLS7 Signing Key
        keyPairInfo = KeyPairInfo()
        keyPairInfo.PrivateKeyClient = self.argv.get('DCU_privateKeyClient', self.yml["DCU"]["privateKeyClient"])
        keyPairInfo.PublicKeyServer = self.argv.get('DCU_publicKeyServer', self.yml["DCU"]["publicKeyServer"])
        self.classDlms.KeyPair_Signing = keyPairInfo
        
        res = self.classDlms.DeviceConnect()
        if int(res) == 1:
            info("** SYSTEM INFO ** : Admin Connect DCU Success")
        else:
            self.classDlms.DeviceDisconnect(True)
            error("** SYSTEM INFO ** : Admin Connect DCU Failed, Error reason: %s" % ConnectStatus[str(res)])
            raise Exception("Admin Connect DCU Failed, Error reason: %s" % ConnectStatus[str(res)])

        # 提升权限
        if self.classDlms.Identification():
            info("** SYSTEM INFO ** : High Security Identification Success")
        else:
            self.classDlms.DeviceDisconnect(True)
            error("** SYSTEM INFO ** : High Security Identification Failed")
            raise Exception("High Security Identification Failed")



    def connect(self):
        """
        连接电表
        """
        # 获取全局变量
        communication = self.argv.get('communication', Singleton().Communication).upper()

        filename = os.path.join(os.path.dirname(__file__), f"../conf/ConnParam/dcu.yaml")
        with open(filename, encoding="utf-8") as f:
            self.yml = yaml.load(f, Loader=yaml.FullLoader)

        #是否打印详细日志，如KeyAgreement协商过程步骤的日志
        self.classDlms.bWriteDlmsLog = True
        # 指定详细日志文件的存储路径
        # self.classDlms.WriteDlmsLogPath = "logs"
        #是否需要检查Wrap包头
        self.classDlms.IsCheckWrapHeader = True
        #是否预连接
        self.classDlms.bPreEstablished = False
        #是否保存解密后的报文
        # self.classDlms.bSaveDecryptPduLog = True

        # 配置日志代理
        self.classDlms.OnSentData = CommunicationLog(CommunicationDelegate.showCommunicationInfo)
        self.classDlms.OnReceivedData = CommunicationLog(CommunicationDelegate.showCommunicationInfo)

        # 配置DLMSStateChange代理
        # self.classDlms.OnStateChange = DLMSStateChange(DLMSStateChangeDelegate.showStateChangeInfo)

        # 将密钥保存到全局环境中 (不能移到电表连接成功后再赋值)
        Singleton().EKey = self.argv.get('DCU_eKey', self.yml["DCU"]["eKey"])
        Singleton().AKey = self.argv.get('DCU_aKey', self.yml["DCU"]["aKey"])
        Singleton().SystemTitleClient = self.argv.get('DCU_systemTitleClient', self.yml['DCU']['systemTitleClient'])
        Singleton().ServerPublicKeySigning = self.argv.get('DCU_publicKeyServer', self.yml['DCU']['publicKeyServer'])
        Singleton().ClientPublicKeySigning = self.argv.get('DCU_publicKeyClient', self.yml['DCU']['publicKeyClient'])

        # 红外连接电表
        if communication == "HDLC":
            self.configInfrared()
        # IP连接电表
        if communication == "IP":
            self.configIp()


        # 用public账号连接
        isPublicConnFirst = int(self.argv.get('DCU_isPublicConnFirst',self.yml['DCU']['isPublicConnFirst']))
        if isPublicConnFirst == 1:
            self.connectMeterByPublic(communication)
        # 用admin账号连接
        self.connectMeterByAdmin(communication)


        # 如果用到 dedicatedKey, 解密报文时需用 dedicatedKey 替换 eKey
        if self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey:
            info(self.classDlms.CommunicationParam.AARQParam.DedicatedKey)
            Singleton().EKey = self.classDlms.CommunicationParam.AARQParam.DedicatedKey

            self.classDlms.FrameCounter = 1


    def disconnect(self):
        """
        断开电表连接
        """
        try:
            # 断开 DLMS 连接
            self.classDlms.DlmsDisconnect()
            # 断开物理连接
            self.classDlms.DeviceDisconnect(True)
            info("** SYSTEM INFO ** : DisConnect OK")
        except AttributeError as ex:
            error(f"disconnect() failed!\n{ex}")


    def receiveXmlOrPdu(self, xmlOrPdu):
        """
        接收XML或PDU数据

        :param xmlOrPdu:   xml或pdu字符串
        :return:           电表返回数据
        """
        # 接收XML或PDU数据
        sender = Dcu.isXmlOrPdu(xmlOrPdu)
        if sender == 'xml':
            info(f"Send Pdu: {PduXml.PhaseXml2Pdu(xmlOrPdu)}")
            info(f"Send Xml: {formatXmlString(xmlOrPdu)}")
            response = self.classDlms.DirectlySendAndRecvXml(xmlOrPdu).replace('\r', '')
            if len(response) == 0:
                error(f"Recv Xml: 'NO RESPONSE ~~~ !'" )
            else:
                info(f"Recv Pdu: {PduXml.PhaseXml2Pdu(response)}")
                info(f"Recv Xml:\n{response}")
            return response

        elif sender == 'pdu':
            xmlOrPdu = xmlOrPdu.replace(' ','')
            recv = self.classDlms.DirectlySendAndRecvPdu(xmlOrPdu)
            return recv

        else:
            error("** SYSTEM INFO ** : The input is not xml or Pdu")


    @staticmethod
    def isXmlOrPdu(s):
        """
        判断目标字符串是Pdu, xml 或其它类型

        :param s:    字符串
        :return:     字符串类型（xml/pdu/Unknow）
        """
        if s[0] == '<' and s[-1] == '>':
            return 'xml'
        elif len([item for item in s if not (item.upper() in "0123456789ABCEDF ")]) == 0:
            return 'pdu'
        else:
            return 'Unknow'



def disconnectDcu(conn):
    """
    断开设备连接

    :param conn:  连接对象
    """
    if conn is not None:
        if isinstance(conn, Dcu):
            conn.disconnect()
