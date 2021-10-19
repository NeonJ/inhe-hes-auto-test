# -*- coding:utf-8 -*-

import yaml
from .Delegate import *
from dlms import *
from libs.SerialLib import Serial
from .DllLoader import ClassDLMS, CommunicationLog, KeyPairInfo, UsefulFunction


class KaifaDLMS(object):

    def __init__(self, **argv):
        self.argv = argv
        # self.apduParser = ApduParser()
        self.classDlms = ClassDLMS()
        self.yml = None
        self.project = None
        self.clientId = None
        self.communication = None
        self.frameCounter = 0
        self.conformance = ''
        self.isPublicFirst = True
        self.isConnect = True
        self.isUseIEC = self.argv.get('isUseIEC')
        self.ServerLowerMACAddressValue = self.argv.get('ServerLowerMACAddressValue')
        self.comPort = self.argv.get('comPort')
        self.baudrate = self.argv.get('baudrate')
        self.ServerIpAddress = self.argv.get('ServerIpAddress')
        self.MeterSapId = self.argv.get('MeterSapId')

        # 执行连接
        self.connect()


    def configInfrared(self):
        """
        配置HDLC模式连接参数

        :return:   None
        """
        comPort = self.comPort or self.argv.get('HDLC_comPort', Singleton().ComPort) or self.yml['HDLC']['comPort']
        info(f"** SYSTEM INFO ** : Connecting via HDLC -- [Client Id: {self.clientId}, ComPort: {comPort}]...")

        # 配置红外连接模式
        self.classDlms.SetCommunicationType(0)
        self.classDlms.iConnectType = 0

        # 配置串口参数
        self.classDlms.CommunicationParam.CommPortParam.PortNumber = comPort
        self.classDlms.CommunicationParam.CommPortParam.Echoing = self.argv.get('HDLC_echoing', self.yml['HDLC']['echoing'])
        self.classDlms.CommunicationParam.IECParam.MaxBaud = self.baudrate or self.argv.get('HDLC_baudrate', self.yml['HDLC']['baudrate'])

        # HDLC params
        if self.isUseIEC is None:
            self.classDlms.CommunicationParam.HDLCParam.OpeningUsesIEC = self.argv.get('HDLC_useIEC', Singleton().useIEC) or self.argv.get('HDLC_useIEC', self.yml['HDLC']['useIEC'])
        else:
            self.classDlms.CommunicationParam.HDLCParam.OpeningUsesIEC = self.isUseIEC
        self.classDlms.CommunicationParam.HDLCParam.ServerAddressSize = self.argv.get('HDLC_serverAddressSize', self.yml["HDLC"]["serverAddressSize"])
        self.classDlms.CommunicationParam.HDLCParam.ServerUpperMACAddressValue = self.argv.get('HDLC_serverUpperMacAddress', self.yml["HDLC"]["serverUpperMacAddress"])
        self.classDlms.CommunicationParam.HDLCParam.ServerLowerMACAddressValue = self.ServerLowerMACAddressValue or self.argv.get('HDLC_serverLowerMacAddress', self.yml["HDLC"]["serverLowerMacAddress"])
        self.classDlms.CommunicationParam.HDLCParam.InactivityTimeout = self.argv.get('HDLC_inactivityTimeout', self.yml["HDLC"]["inactivityTimeout"])
        self.classDlms.CommunicationParam.HDLCParam.InterFrameTimeout = self.argv.get('HDLC_interFrameTimeout', self.yml["HDLC"]["interFrameTimeout"])
        self.classDlms.CommunicationParam.HDLCParam.ResponseTimeout = self.argv.get('HDLC_responseTimeout', self.yml["HDLC"]["responseTimeout"])


    def configGprs(self):
        """
        配置GPRS模式连接参数
        :return:   None
        """
        serverIpAddr = self.ServerIpAddress or self.argv.get('GPRS_ServerIpAddress', Singleton().ServerIpAddress) or self.yml['GPRS']['ServerIpAddress']
        info(f"** SYSTEM INFO ** : Connecting via GPRS -- [ServerIp: {serverIpAddr}]...")

        # 配置Remote通信模式
        self.classDlms.SetCommunicationType(2)  # 2-网络直连走Wrap协议模式
        self.classDlms.iConnectType = 0

        # 配置Remote通信参数
        self.classDlms.CommunicationParam.GprsParam.ServerIpAddress = serverIpAddr
        self.classDlms.CommunicationParam.GprsParam.ServerIpPort = str(self.argv.get("GPRS_ServerIpPort", self.yml['GPRS']['ServerIpPort']))
        self.classDlms.CommunicationParam.GprsParam.DestinedAddr = self.argv.get("GPRS_DestinedAddr", self.yml['GPRS']['DestinedAddr'])
        self.classDlms.CommunicationParam.GprsParam.Timeout = self.argv.get("GPRS_responseTimeout", self.yml['GPRS']['responseTimeout'])
        # self.classDlms.CommunicationParam.GprsParam.isIPv6UDP = False

    def configDcu(self):
        """
        配置DCU模式连接参数

        :return:   None
        """
        serverIpAddr = self.ServerIpAddress or self.argv.get('DCU_ServerIpAddress', Singleton().ServerIpAddress) or self.yml['DCU']['ServerIpAddress']
        sapId = self.MeterSapId or self.argv.get("DCU_MeterSapId", Singleton().MeterSapId) or self.yml['DCU']['MeterSapId']
        info(f"** SYSTEM INFO ** : Connecting via DCU -- [ServerIp: {serverIpAddr}, SapId : {sapId}]...")

        # 配置Remote通信模式
        self.classDlms.SetCommunicationType(2)  # 2-网络直连走Wrap协议模式
        self.classDlms.iConnectType = 0

        # 配置Remote通信参数
        self.classDlms.CommunicationParam.GprsParam.ServerIpAddress = serverIpAddr
        self.classDlms.CommunicationParam.GprsParam.ServerIpPort = str(self.argv.get("DCU_ServerIpPort", self.yml['DCU']['ServerIpPort']))
        # self.classDlms.CommunicationParam.GprsParam.DestinedAddr = 1  # DCU Sap ID 恒为 1
        self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("DCU_Admin_SourceAddr", self.yml['DCU']['Admin']['clientMacAddress'])
        self.classDlms.CommunicationParam.GprsParam.Timeout = int(self.argv.get("DCU_responseTimeout", self.yml['DCU']['responseTimeout']))
        # self.classDlms.CommunicationParam.GprsParam.Timeout = self.argv.get("DCU_responseTimeout", self.yml['DCU']['responseTimeout'])


    def configAARQParams(self, isAdmin=True):
        """
        配置AARQ参数

        :return:   None
        """
        self.classDlms.CommunicationParam.AARQParam.UsageGBT = self.argv.get('AARQ_usageGBT', self.yml["AARQ"]["usageGBT"])
        if isAdmin:
            if self.classDlms.CommunicationParam.AARQParam.UsageGBT:
                if self.project.lower() in ['cetus02']:
                    self.classDlms.bGbtAfterAARQ = False  # Identification 时不用GBT，连接完成之后才就根据usingGbtTrans进行GBT处理
        self.classDlms.CommunicationParam.AARQParam.ClientMaxReceivePDUSize = self.argv.get('AARQ_clientMaxReceivePDUSize', self.yml["AARQ"]["clientMaxReceivePDUSize"])
        self.classDlms.CommunicationParam.AARQParam.CallingApTitle = self.argv.get('AARQ_systemTitleClient', self.yml["AARQ"]["systemTitleClient"])
        self.classDlms.CommunicationParam.AARQParam.CallingAeQualifier = self.argv.get('AARQ_callingAeQualifier', self.yml["AARQ"]["callingAeQualifier"])


    def configPublicAccount(self):
        """
        配置public account参数

        :return:   None
        """
        if self.communication == "HDLC":
            self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress = self.argv.get('HDLC_Public_clientMacAddress', self.yml["HDLC"]['Public']["clientMacAddress"])
        if self.communication == "GPRS":
            self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("GPRS_Public_SourceAddr", self.yml['GPRS']['Public']['clientMacAddress'])
        if self.communication == "DCU":
            self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("DCU_Public_SourceAddr", self.yml['DCU']['Public']['clientMacAddress'])
            # self.classDlms.CommunicationParam.GprsParam.DestinedAddr = self.argv.get("DCU_MeterSapId", self.yml['DCU']['MeterSapId'])
            self.classDlms.CommunicationParam.GprsParam.DestinedAddr = self.argv.get("DCU_MeterSapId", Singleton().MeterSapId) or self.yml['DCU']['MeterSapId']

        # 配置 public 客户端的 AARQ 参数
        self.configAARQParams(isAdmin=False)
        self.classDlms.CommunicationParam.AARQParam.ApplicationContextName = self.argv.get('AARQ_Public_applicationContextName', self.yml["AARQ"]['Public']["applicationContextName"])
        self.classDlms.CommunicationParam.AARQParam.AlgorithmType = MechanismEnum.get(self.argv.get('AARQ_Public_mechanism', self.yml["AARQ"]['Public']["mechanism"]))
        protectionType = self.argv.get('AARQ_Public_protectionType', self.yml["AARQ"]['Public']["protectionType"])
        if protectionType is not None:
            self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType = GeneralProtectionTypeEnum.get(protectionType)
            self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey = UsageDedicatedKeyEnum.get(protectionType)
        accessLevel = self.argv.get('AARQ_Public_accessLevel', self.yml["AARQ"]['Public']["accessLevel"])
        self.classDlms.CommunicationParam.AARQParam.MechanismName = accessLevel
        if accessLevel == "High Security":
            self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = True
        else:
            self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = False


    def _queryFrameCounterByPublic(self):
        """
        通过 Public 客户端获取 FrameCounter

        :return:   None
        """
        # 如果指定了 frameCounter 参数, 则直接使用 frameCounter 参数
        if int(self.frameCounter) > 0:
            self.classDlms.FrameCounter = self.frameCounter

        else:
            # 通过调用 action 获取电表的 Invocation Counter
            if self.yml['Basic']['frameCounterMode'] == "action":
                # self.classDlms.ClassActionFrameCounter.OBISCode = "00002B010" + str(self.yml[self.communication]["Admin"]["clientMacAddress"]) + "FF"
                self.classDlms.ClassActionFrameCounter.OBISCode = self.yml['Basic']['frameCounterObis']
                self.classDlms.ClassActionFrameCounter.MethodID = 1
                if self.classDlms.ClassActionFrameCounter.ExcuteCommand():
                    self.classDlms.FrameCounter = self.classDlms.ClassActionFrameCounter.FrameCounter
                    info("** SYSTEM INFO ** : Invocation Counter: %s" % str(self.classDlms.FrameCounter))
                else:
                    error("** SYSTEM INFO ** : Get Invocation Counter Failed")
                    self.classDlms.DeviceDisconnect(True)

            # 通过调用 attribute 获取电表的 Invocation Counter
            if self.yml['Basic']['frameCounterMode'] == "attribute":
                self.classDlms.ClassData.OBISCode = self.argv.get('frameCounterObis',  self.yml['Basic']['frameCounterObis'])
                self.classDlms.ClassData.AttributeID = 2
                if self.classDlms.ClassData.GetRequest():
                    self.classDlms.FrameCounter = self.classDlms.ClassData.Value
                    info("** SYSTEM INFO ** : Read Invocation Counter: %s" % str(self.classDlms.FrameCounter))
                else:
                    error("** SYSTEM INFO ** : Read Invocation Counter Failed")
                    self.classDlms.DeviceDisconnect(True)


    def connectPublicAccount(self, isPublicOnly=False):
        """
        使用 public 账号连接电表

        :param isPublicOnly:     如果为False则获取FrameCounter， 反之不获取
        :return:                 None
        """
        self.configPublicAccount()
        res = self.classDlms.DeviceConnect()
        if int(res) == 1:
            info("** SYSTEM INFO ** : Public Client Connect Meter Succeed")
        else:
            error("** SYSTEM INFO ** : Public Client Connect Meter Failed, Error reason: '%s'" % ConnectStatus[str(res)])
            raise Exception("Public Client Connect Meter Failed, Error reason: '%s'" % ConnectStatus[str(res)])

        if not isPublicOnly:
            # 通过 Public 客户端获取 FrameCounter
            self._queryFrameCounterByPublic()

            # 断开 Public 连接
            # self.classDlms.DlmsDisconnect()       # Dlms协议层断开
            self.classDlms.DeviceDisconnect(True)   # 物理层断开
            info("** SYSTEM INFO ** : Public Client Disconnect Succeed")


    def configAdminAccount(self):
        """
        配置 Admin 账号参数

        :return:   None
        """

        if self.communication == "HDLC":
            self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress = self.argv.get('HDLC_Admin_clientMacAddress', self.yml["HDLC"]['Admin']["clientMacAddress"])
        if self.communication == "GPRS":
            self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("GPRS_Admin_SourceAddr", self.yml['GPRS']['Admin']['clientMacAddress'])
        if self.communication == "DCU":
            self.classDlms.CommunicationParam.GprsParam.SourceAddr = self.argv.get("DCU_Admin_SourceAddr", self.yml['DCU']['Admin']['clientMacAddress'])
            self.classDlms.CommunicationParam.GprsParam.DestinedAddr = self.argv.get("DCU_MeterSapId", Singleton().MeterSapId) or self.yml['DCU']['MeterSapId']

        # 配置 admin 客户端的 AARQ 参数
        self.configAARQParams()
        self.classDlms.CommunicationParam.AARQParam.ApplicationContextName = self.argv.get('AARQ_Admin_applicationContextName', self.yml["AARQ"]['Admin']["applicationContextName"])
        self.classDlms.CommunicationParam.AARQParam.AlgorithmType = MechanismEnum.get(self.argv.get('AARQ_Admin_mechanism', self.yml["AARQ"]['Admin']["mechanism"]))
        protectionType = self.argv.get('AARQ_Admin_protectionType', self.yml["AARQ"]['Admin']["protectionType"])
        if protectionType is not None:
            self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType = GeneralProtectionTypeEnum.get(protectionType)
            self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey = UsageDedicatedKeyEnum.get(protectionType)

        # Signing 数据报文签名保护
        self.classDlms.IsGeneralSigning = self.argv.get('AARQ_Admin_signing', self.yml["AARQ"]['Admin']["signing"])

        accessLevel = self.argv.get('AARQ_Admin_accessLevel', self.yml["AARQ"]['Admin']["accessLevel"])
        if accessLevel is not None:
            self.classDlms.CommunicationParam.AARQParam.MechanismName = accessLevel
            if accessLevel == "No Security":
                self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = False
            else:
                self.classDlms.CommunicationParam.AARQParam.SenderACSERequirements = True

        # Key params
        self.classDlms.CommunicationParam.SecInfo.UsingLlsKey = self.argv.get('Key_llsKey', self.yml["Key"]["llsKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingHlsKey = self.argv.get('Key_hlsKey', self.yml["Key"]["hlsKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingAuthenticationKey = self.argv.get('Key_aKey', self.yml["Key"]["aKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingEncryptionKey = self.argv.get('Key_eKey', self.yml["Key"]["eKey"])
        self.classDlms.CommunicationParam.SecInfo.UsingMasterKey = self.argv.get('Key_kekKey', self.yml["Key"]["kekKey"])

        # SC params
        self.classDlms.SC_SecurityControl = self.argv.get('AARQ_Admin_securityPolicy', self.yml["AARQ"]['Admin']["securityPolicy"])

        # HLS7 Signing Key
        keyPairInfo = KeyPairInfo()
        keyPairInfo.PrivateKeyClient = self.argv.get('Key_privateKeyClient', self.yml["Key"]["privateKeyClient"])
        keyPairInfo.PublicKeyServer = self.argv.get('Key_publicKeyServer', self.yml["Key"]["publicKeyServer"])
        self.classDlms.KeyPair_Signing = keyPairInfo


    def connectAdminAccount(self):
        """
        使用Admin账号连接电表

        :return:   None
        """

        # 先从文件里面读取FrameCounter, 不行再用public account获取
        if self.isPublicFirst == 1:
            for i in range(2):
                # 第一次尝试从文件中读取FrameCounter
                if i == 0:
                    frameCounter = readFrameCounter(self.project, self.clientId)
                    if frameCounter != -1:
                        self.classDlms.FrameCounter = frameCounter
                        info(f"** Current Invocation Counter: {frameCounter} **")
                    else:
                        # 如果无法从文件中获取到有效FrameCounter, 则通过Public客户端去获取
                        self.connectPublicAccount()

                # 如果从文件中读取的FrameCounter无法连接成功, 则通过Public客户端去获取
                else:
                    self.connectPublicAccount()

                # 用 admin 账号连接
                self.configAdminAccount()

                # 如果用到 dedicatedKey, Cetus05 需要预先存储 FrameCounter (还需 +1)
                if self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey:
                    writeFrameCounter(self.project, self.clientId, self.classDlms.FrameCounter+1)

                res = self.classDlms.DeviceConnect()
                if int(res) == 1:
                    # info("** SYSTEM INFO ** : Admin Connect Meter Success")
                    info("** SYSTEM INFO ** : HLS-Pass2 [AARE] Succeed")
                    break
                else:
                    self.classDlms.DeviceDisconnect(True)
                    error("** SYSTEM INFO ** : HLS-Pass2 [AARE] Failed, Error reason: '%s'" % ConnectStatus[str(res)])

                # 两次尝试连接都失败后，抛出异常
                if i == 1 and int(res) != 1:
                    raise Exception("HLS-Pass2 [AARE] Failed, Error reason: '%s'" % ConnectStatus[str(res)])
        # 直接使用文件里的FrameCounter连接
        elif self.isPublicFirst == 0:
            # 如果指定了 frameCounter 参数, 则直接使用 frameCounter 参数
            if int(self.frameCounter) > 0:
                self.classDlms.FrameCounter = self.frameCounter
            else:
                frameCounter = readFrameCounter(self.project, self.clientId)
                if frameCounter != -1:
                    self.classDlms.FrameCounter = frameCounter
                    info(f"** Current Invocation Counter: {frameCounter} **")

            # 用 admin 账号连接
            self.configAdminAccount()

            # 如果用到 dedicatedKey, Cetus05 需要预先存储 FrameCounter (还需 +1)
            if self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey:
                writeFrameCounter(self.project, self.clientId, self.classDlms.FrameCounter + 1)

            res = self.classDlms.DeviceConnect()
            if int(res) == 1:
                info("** SYSTEM INFO ** : HLS-Pass2 [AARE] Succeed")
            else:
                self.classDlms.DeviceDisconnect(True)
                error(
                    "** SYSTEM INFO ** : HLS-Pass2 [AARE] Failed, Error reason: '%s'" % ConnectStatus[str(res)])
                raise Exception("HLS-Pass2 [AARE] Failed, Error reason: '%s'" % ConnectStatus[str(res)])
        # 先用public account获取FrameCounter， 再连接电表
        elif self.isPublicFirst == 2:
            self.connectPublicAccount()

            # 用 admin 账号连接
            self.configAdminAccount()

            # 如果用到 dedicatedKey, Cetus05 需要预先存储 FrameCounter (还需 +1)
            if self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey:
                writeFrameCounter(self.project, self.clientId, self.classDlms.FrameCounter + 1)

            res = self.classDlms.DeviceConnect()
            if int(res) == 1:
                info("** SYSTEM INFO ** : HLS-Pass2 [AARE] Succeed")
            else:
                self.classDlms.DeviceDisconnect(True)
                error(
                    "** SYSTEM INFO ** : HLS-Pass2 [AARE] Failed, Error reason: '%s'" % ConnectStatus[str(res)])
                raise Exception("HLS-Pass2 [AARE] Failed, Error reason: '%s'" % ConnectStatus[str(res)])

        # 如果用到 dedicatedKey, 解密报文时需用 dedicatedKey 替换 eKey
        if self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey:
            info(f'** SYSTEM INFO ** : DedicatedKey -- {self.classDlms.CommunicationParam.AARQParam.DedicatedKey}')
            Singleton().EKey = self.classDlms.CommunicationParam.AARQParam.DedicatedKey


        # 提升权限
        if self.classDlms.Identification():
            # info("** SYSTEM INFO ** : High Security Identification Success")
            info("** SYSTEM INFO ** : HLS-Pass4 [S->C f(CtoS)] Succeed")
        else:
            self.classDlms.DeviceDisconnect(True)
            error("** SYSTEM INFO ** : HLS-Pass4 [S->C f(CtoS)] Failed")
            raise Exception("HLS-Pass4 [S->C f(CtoS)] Failed")


    def connect(self, **argv):
        """
        执行电表连接操作
        """
        if len(argv) != 0:
            self.argv = argv

        if Singleton().Communication != "HDLC":
            if not waitMeterRegistered(Singleton().ServerIpAddress).status:
                raise Exception("Wait register to Meter failed")

        # 指定 frameCounter (接收一个10进制数)
        self.frameCounter = int(self.argv.get('frameCounter', 0))
        # 指定 Conformance  (接收一个字符串List)
        self.conformance = self.argv.get('conformance', '')
        # 控制是否执行连接操作 (接收一个bool值)
        self.isConnect = self.argv.get('isConnect', True)

        try:
            # 如果连接对象仍然可用, 直接返回该连接对象
            if self.checkAlive():
                return self

            # 针对重连情况: 尝试先行断开连接，用以规避上次异常断开
            self.classDlms.DeviceDisconnect(True)
        except:
            pass

        # 获取全局变量
        self.communication = self.argv.get('communication', Singleton().Communication).upper()
        self.project = Singleton().Project.lower()

        # 读取配置文件
        self.clientId = self.argv.get('client', Singleton().Client)
        if self.clientId is None:
            self.clientId = 1
        conf = self.project + '_client' + str(self.clientId)
        filename = os.path.join(os.path.dirname(__file__), f"../conf/ConnParam/{self.project}/{conf}.yaml")
        with open(filename, encoding="utf-8") as f:
            self.yml = yaml.load(f, Loader=yaml.FullLoader)

        # 指定详细日志文件的存储路径
        # self.classDlms.WriteDlmsLogPath = "logs"
        # 是否保存解密后的报文
        # self.classDlms.bSaveDecryptPduLog = True

        # 是否打印详细日志，如KeyAgreement协商过程步骤的日志
        self.classDlms.bWriteDlmsLog = True
        # 是否需要检查Wrap包头
        self.classDlms.IsCheckWrapHeader = True
        # 是否预连接
        self.classDlms.bPreEstablished = self.argv.get('bPreEstablished', False)
        self.classDlms.bPreEstablished_WithHdlcConn = self.classDlms.bPreEstablished
        # GMAC连接进行Identification认证时，是否验证电表返回的随机数
        self.classDlms.IsVerifyFctos = self.argv.get('IsVerifyFctos', False)

        # 配置日志代理
        self.classDlms.OnSentData = CommunicationLog(CommunicationDelegate.showCommunicationInfo)
        self.classDlms.OnReceivedData = CommunicationLog(CommunicationDelegate.showCommunicationInfo)

        # 配置DLMSStateChange代理
        # self.classDlms.OnStateChange = DLMSStateChange(DLMSStateChangeDelegate.showStateChangeInfo)

        # 获取`isPublicFirst`
        self.isPublicFirst = self.argv.get('isPublicFirst', self.yml['Basic']['isPublicFirst'])

        # 将密钥保存到全局环境中
        Singleton().EKey = self.argv.get('Key_eKey', self.yml["Key"]["eKey"])
        Singleton().AKey = self.argv.get('Key_aKey', self.yml["Key"]["aKey"])
        Singleton().BKey = self.argv.get('Key_bKey', self.yml["Key"]["bKey"])
        Singleton().MasterKey = self.argv.get('Key_kekKey', self.yml["Key"]["kekKey"])
        Singleton().LlsKey = self.argv.get('Key_llsKey', self.yml["Key"]["llsKey"])
        Singleton().HlsKey = self.argv.get('Key_hlsKey', self.yml["Key"]["hlsKey"])
        Singleton().SystemTitleClient = self.argv.get('AARQ_systemTitleClient', self.yml['AARQ']['systemTitleClient'])
        Singleton().ServerPublicKeySigning = self.argv.get('Key_publicKeyServer', self.yml['Key']['publicKeyServer'])
        Singleton().ClientPublicKeySigning = self.argv.get('Key_publicKeyClient', self.yml['Key']['publicKeyClient'])

        # 红外连接电表
        if self.communication == "HDLC":
            self.configInfrared()
        # GPRS连接电表
        if self.communication == "GPRS":
            self.configGprs()
        # DCU连接电表
        if self.communication == "DCU":
            self.configDcu()

        # 配置 Conformance (self.conformance 是一个list)
        if len(self.conformance) > 0:
            result = self.setConformance(self.conformance)
            if not result.status:
                raise Exception(f"Config conformance failed, Error reason: '{result.result}'")

        # 用public账号连接
        if int(self.clientId) == 16:
            if self.isConnect:
                self.connectPublicAccount(isPublicOnly=True)
            else:
                self.configPublicAccount()

        # 用admin账号连接
        else:
            if self.isConnect:
                self.connectAdminAccount()
            else:
                self.configPublicAccount()
                self.configAdminAccount()


    def disconnect(self):
        """
        断开电表连接

        :return:
        """

        # 将 frameCounter 写入到文件中
        self.saveFrameCounter()

        # 断开连接
        self.classDlms.DeviceDisconnect(True)
        info("** SYSTEM INFO ** : DisConnect Meter Succeed")


    def receiveXmlOrPdu(self, xmlOrPdu):
        """
        接收XML或PDU命令，返回对应数据

        :param xmlOrPdu:   xml或pdu字符串
        :return:           电表返回数据
        """
        # # 接收XML或PDU数据
        sender = isXmlOrPdu(xmlOrPdu)
        # if sender == 'xml':
        #     pdu = xml2Pdu(xmlOrPdu)
        #     debug(f"Send Pdu: {pdu}")
        #     debug(f"Send Xml: {formatXmlString(xmlOrPdu)}")
        #     pdu = pdu.replace(' ', '')
        #     response = self.classDlms.DirectlySendAndRecvPdu(pdu)
        #     if len(response) == 0:
        #         error(f"Recv Xml: 'Not receive response ~~~ !'")
        #         return
        #     else:
        #         try:
        #             debug(f"Recv Pdu: {response}")
        #             debug(f"Recv Xml:\n{pdu2Xml(response)}")
        #         except:
        #             error(f"Pdu error: {response}")
        #
        #     return pdu2Xml(response)
        # elif sender == 'pdu':
        #     xmlOrPdu = xmlOrPdu.replace(' ', '')
        #     recv = self.classDlms.DirectlySendAndRecvPdu(xmlOrPdu)
        #     return recv
        # else:
        #     error("** SYSTEM INFO ** : The input is not xml or Pdu")


        if sender == 'xml':
            debug(f"Send Pdu: {xml2Pdu(xmlOrPdu)}")
            debug(f"Send Xml: {formatXmlString(xmlOrPdu)}")
            response = self.classDlms.DirectlySendAndRecvXml(xmlOrPdu).replace('\r', '')
            if len(response) == 0:
                error(f"Recv Xml: 'Not receive response ~~~ !'")
                return
            else:
                debug(f"Recv Pdu: {xml2Pdu(response)}")
                debug(f"Recv Xml:\n{response}")
                pass
            return response
        elif sender == 'pdu':
            xmlOrPdu = xmlOrPdu.replace(' ', '')
            recv = self.classDlms.DirectlySendAndRecvPdu(xmlOrPdu)
            return recv
        else:
            error("** SYSTEM INFO ** : The input is not xml or Pdu")


    def saveFrameCounter(self):
        """
        将 frameCounter 存储到文件中

        :return:   保存成功返回True, 反之返回False
        """
        try:
            if not self.classDlms.CommunicationParam.AARQParam.UsageDedicatedKey:
                if int(self.classDlms.FrameCounter) != 0:
                    writeFrameCounter(self.project, self.clientId, self.classDlms.FrameCounter)
            return True
        except:
            return False


    def forceHdlcDisconnect(self):
        """
        构造DISC (53) 帧发送给电表, 强制断开dlms连接

        :return:
        """
        pdu = assembleHdlcFrame(clientAddr=self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress,
                                serverUpperAddr=self.classDlms.CommunicationParam.HDLCParam.ServerUpperMACAddressValue,
                                serverLowerAddr=self.classDlms.CommunicationParam.HDLCParam.ServerLowerMACAddressValue,
                                control=53)
        ser = Serial(comPort=self.classDlms.CommunicationParam.CommPortParam.PortNumber)
        ser.sendCmdOnce(pdu)


    def checkAlive(self):
        """
        检查当前连接对象是否alive

        :return:    True / False
        """
        # 获取电表时间(0.0.1.0.0.255)
        response = self.classDlms.DirectlySendAndRecvPdu('C0 01 C1 00 08 00 00 01 00 00 FF 02 00'.replace(' ', ''))
        if len(response) != 0:
            return True
        return False

    def getMethod(self, classId, obis, attrId):
        """
        下发Get请求并获取响应
        :param classId:
        :param obis:
        :param attrId:
        :return:
        """
        try:
            cls = globals()[ClassInterfaceMap[str(classId)]](self, obis)
        except KeyError as ex:
            error(ex)
            return

        methodName = 'get_' + cls.attr_index_dict[int(attrId)]
        method = getattr(cls, methodName)
        return method()


    def setMethod(self, classId, obis, attrId, value):
        """
        下发Set请求并获取响应
        :param classId:
        :param obis:
        :param attrId:
        :param value:
        :return:
        """
        try:
            cls = globals()[ClassInterfaceMap[str(classId)]](self, obis)
        except KeyError as ex:
            error(ex)
            return

        methodName = 'set_' + cls.attr_index_dict[int(attrId)]
        method = getattr(cls, methodName)
        return method(value)


    def actMethod(self, classId, obis, attrId, value=None):
        """
        下发Action请求并获取响应
        :param classId:
        :param obis:
        :param attrId:
        :param value:
        :return:
        """
        try:
            cls = globals()[ClassInterfaceMap[str(classId)]](self, obis)
        except KeyError as ex:
            error(ex)
            return

        methodName = 'act_' + cls.action_index_dict[int(attrId)]
        method = getattr(cls, methodName)

        if value is not None:
            return method(value)
        else:
            return method()


    ###########################################################################################################


    def getConformance(self, proposedConformance=False):
        """
        获取 xDLMS Conformance block

        :param proposedConformance:  是否返回协商后的Conformance, 即服务端返回的Conformance;
                                     True:  返回服务器响应的Conformance
                                     False: 返回电表请求的Conformance

        :return: 返回一个元组,
            第一个元素是一个list: ['block-transfer-with-set-or-write', 'block-transfer-with-action', 'multiple-references', 'information-report', 'get', 'set', 'selective-access', 'event-notification', 'action']
            第二个元素是一个字符串(24bit):  011000000000111100011111
        """
        if proposedConformance:
            conformance = Singleton().Conformance
        else:
            conformance = self.classDlms.ConformanceBlock

        if conformance is None or len(str(conformance).strip()) == 0:
            conformanceList = ['0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','0','0','0','1','1','1','1','1']
            if self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType != 0:
                conformanceList[1] = '1'
            if self.classDlms.CommunicationParam.AARQParam.UsageGBT:
                conformanceList[2] = '1'
            return [ConformanceMap[str(index)] for index, item in enumerate(conformanceList) if item == '1'], "".join(conformanceList)
        else:
            return [ConformanceMap[str(index)] for index, item in enumerate(conformance) if item == '1'], conformance


    def setConformance(self, conformance):
        """
        设置 xDLMS Conformance block

        :param conformance:  接收一个BitString字符串, 或list(可参考 libs/Constants.py/ConformanceMap)
        :return:  返回一个 KFResult 对象

        Example
        ----------
        conformanceList = ['general-protection', 'general-block-transfer', 'get', 'set', 'action', 'check']
        result = conn.setConformance(conformanceList)
        info(result.status)
        info(result.result)
        """
        if isBitString(conformance) and len(conformance) == 24:
            self.classDlms.ConformanceBlock = conformance
            return KFResult(True, self.getConformance())

        conformanceList = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        for item in conformance:
            index = getKeyByValue(ConformanceMap, str(item).lower())
            if len(index) != 0:
                conformanceList[int(index[0])] = '1'
            else:
                return KFResult(False, f'Conformance block "{item}" not support!')

        self.classDlms.ConformanceBlock = "".join(conformanceList)
        return KFResult(True, self.getConformance())


    def getFrameCounter(self):
        """
        获取 FrameCounter (Invocation Counter)

        :return:    FrameCounter
        """
        return self.classDlms.FrameCounter


    def setFrameCounter(self , frameCounter):
        """
        设置 FrameCounter (Invocation Counter)

        :param frameCounter:   frame Counter
        :return:               KFResult对象
        """
        try:
            self.classDlms.FrameCounter = int(frameCounter)
            return KFResult(True, self.getFrameCounter())
        except Exception as ex:
            return KFResult(False, ex)


    def getServerAddressSize(self):
        """
        获取 HDLC ServerAddressSize

        :return:     十进制数
        """
        return self.classDlms.CommunicationParam.HDLCParam.ServerAddressSize


    def setServerAddressSize(self, serverAddressSize):
        """
        设置 HDLC ServerAddressSize

        :param serverAddressSize:      十进制数
        :return:                       KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.HDLCParam.ServerAddressSize = int(serverAddressSize)
            return KFResult(True, self.getServerAddressSize())
        except Exception as ex:
            return KFResult(False, ex)


    def getServerUpperAddress(self):
        """
        获取 HDLC Server Upper Address

        :return:          十进制数
        """
        return self.classDlms.CommunicationParam.HDLCParam.ServerUpperMACAddressValue


    def setServerUpperAddress(self, serverUpperAddress):
        """
        设置 HDLC Server Upper Address

        :param serverUpperAddress:   十进制数
        :return:                     KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.HDLCParam.ServerUpperMACAddressValue = int(serverUpperAddress)
            return KFResult(True, self.getServerUpperAddress())
        except Exception as ex:
            return KFResult(False, ex)


    def getServerLowerAddr(self):
        """
        获取 HDLC Server Lower Address

        :return:     十进制数
        """
        return self.classDlms.CommunicationParam.HDLCParam.ServerLowerMACAddressValue


    def setServerLowerAddr(self, serverLowerAddress):
        """
        设置 HDLC Server Lower Address

        :param serverLowerAddress:    十进制数
        :return:                      KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.HDLCParam.ServerLowerMACAddressValue = int(serverLowerAddress)
            return KFResult(True, self.getServerLowerAddr())
        except Exception as ex:
            return KFResult(False, ex)


    def getClientMacAddr(self):
        """
        获取 HDLC Client Address

        :return:           十进制数
        """
        return self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress


    def setClientMacAddr(self, clientAddress):
        """
        设置 HDLC Client Address

        :param clientAddress:   十进制数
        :return:                KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.HDLCParam.ClientMACAddress = int(clientAddress)
            return KFResult(True, self.getClientMacAddr())
        except Exception as ex:
            return KFResult(False, ex)


    def getAccessLevel(self):
        """
        获取 Client Access Level

        :return:   字符串（ex. High Security）
        """
        return self.classDlms.CommunicationParam.AARQParam.MechanismName


    def setAccessLevel(self, level):
        """
        设置 Client Access Level

        :param level:    字符串（ex. High Security）
        :return:         KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.AARQParam.MechanismName = level
            return KFResult(True, self.getAccessLevel())
        except Exception as ex:
            return KFResult(False, ex)


    def getSecurityPolicy(self):
        """
        获取 Security Policy

        :return:    返回16进制字符串, 例如: 0x00, 0x20, 0x30, 0x21, 0x31
        """
        return hex(self.classDlms.SC_SecurityControl)


    def setSecurityPolicy(self, sc):
        """
        设置 Security Policy

        :param sc:  接收16进制字符串, 例如: 0x00, 0x20, 0x30, 0x21, 0x31
        :return:    KFResult对象
        """
        try:
            self.classDlms.SC_SecurityControl = int(str(sc), 16)
            return KFResult(True, self.getSecurityPolicy())
        except Exception as ex:
            return KFResult(False, ex)


    def getAuthMechanism(self):
        """
        获取 Authentication mechanism

        :return:    返回16进制字符串, 例如: 0x00, 0x20, 0x30, 0x21, 0x31
        """
        return getKeyByValue(MechanismEnum, self.classDlms.CommunicationParam.AARQParam.AlgorithmType)[0]


    def setAuthMechanism(self, mechanism):
        """
        设置 Authentication mechanism

        :param mechanism:  可选值: default, md5, sha1, gmac, sha256, ecdsa
        :return:           KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.AARQParam.AlgorithmType = MechanismEnum[str(mechanism).strip().lower()]
            return KFResult(True, self.getAuthMechanism())
        except Exception as ex:
            return KFResult(False, ex)


    def getClientSystemTitle(self):
        """
        获取 Client System Title

        :return:    字符串
        """
        return self.classDlms.CommunicationParam.AARQParam.CallingApTitle


    def setClientSystemTitle(self, clientSystemTitle):
        """
        设置 Client System Title

        :param clientSystemTitle:    字符串
        :return:                     KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.AARQParam.CallingApTitle = clientSystemTitle
            return KFResult(True, self.getClientSystemTitle())
        except Exception as ex:
            return KFResult(False, ex)


    def getProtectionType(self):
        """
        获取 Protection Type

        :return:    字符串（ex. glo_ciphering/general_glo_ciphering）
        """
        return getKeyByValue(GeneralProtectionTypeEnum, self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType)[0]


    def setProtectionType(self, protectionType):
        """
        设置 Protection Type

        :param protectionType:  可选值有: glo_ciphering, ded_ciphering, general_glo_ciphering, general_ded_ciphering,
        general_ciphering, general_ciphering_with_signing
        :return:                KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.AARQParam.GeneralProtectionType = GeneralProtectionTypeEnum[str(protectionType).strip().lower()]
            return KFResult(True, self.getProtectionType())
        except Exception as ex:
            return KFResult(False, ex)


    def getApplicationContextName(self):
        """
        获取 applicationContextName

        :return:    字符串
        """
        return self.classDlms.CommunicationParam.AARQParam.ApplicationContextName


    def setApplicationContextName(self, applicationContextName):
        """
        设置 applicationContextName

        :param applicationContextName:  可选值有: LN (LN reference no ciphering); LNC (LN reference with ciphering)
        :return:                        KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.AARQParam.ApplicationContextName = str(applicationContextName).upper()
            return KFResult(True, self.getApplicationContextName())
        except Exception as ex:
            return KFResult(False, ex)


    def getLLSKey(self):
        """
        获取 LLS Key

        :return:     字符串
        """
        return self.classDlms.CommunicationParam.SecInfo.UsingLlsKey


    def setLLSKey(self, llsKey):
        """
        设置 LLS Key

        :param llsKey:   字符串
        :return:         KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.SecInfo.UsingLlsKey = llsKey
            return KFResult(True, self.getLLSKey())
        except Exception as ex:
            return KFResult(False, ex)


    def getHLSKey(self):
        """
        获取 HLS Key

        :return:   16进制字符串
        """
        return self.classDlms.CommunicationParam.SecInfo.UsingHlsKey


    def setHLSKey(self, hlsKey):
        """
        设置 HLS Key

        :param hlsKey:          16进制字符串
        :return:                KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.SecInfo.UsingHlsKey = hlsKey
            return KFResult(True, self.getHLSKey())
        except Exception as ex:
            return KFResult(False, ex)


    def getMasterKey(self):
        """
        获取 Master Key

        :return:   16进制字符串
        """
        return self.classDlms.CommunicationParam.SecInfo.UsingMasterKey


    def setMasterKey(self, masterKey):
        """
        设置 Master Key

        :param masterKey:   16进制字符串
        :return:            KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.SecInfo.UsingMasterKey = masterKey
            return KFResult(True, self.getMasterKey())
        except Exception as ex:
            return KFResult(False, ex)


    def getEncryptionKey(self):
        """
        获取 Encryption Key

        :return:   16进制字符串
        """
        return self.classDlms.CommunicationParam.SecInfo.UsingEncryptionKey


    def setEncryptionKey(self, ekey):
        """
        设置 Encryption Key

        :param ekey:   16进制字符串
        :return:       KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.SecInfo.UsingEncryptionKey = ekey
            # 底层使用DedicatedKey进行加密，所以要修改DedicatedKey后才会生效
            self.classDlms.CommunicationParam.AARQParam.DedicatedKey = ekey
            Singleton().EKey = ekey
            return KFResult(True, self.getEncryptionKey())
        except Exception as ex:
            return KFResult(False, ex)


    def getAuthenticationKey(self):
        """
        获取 Authentication Key

        :return:              16进制字符串
        """
        return self.classDlms.CommunicationParam.SecInfo.UsingAuthenticationKey


    def setAuthenticationKey(self, akey):
        """
        设置 Authentication Key

        :param akey:     16进制字符串
        :return:         KFResult对象
        """
        try:
            self.classDlms.CommunicationParam.SecInfo.UsingAuthenticationKey = akey
            Singleton().AKey = akey
            return KFResult(True, self.getAuthenticationKey())
        except Exception as ex:
            return KFResult(False, ex)


    def createAARQRequest(self, ctos=None, dedicatedKey=None, isXml=True):
        """
        构造 AARQ 请求结构体(XML 或 PDU)

        :param ctos:            challenge client to server (Random string 8-64 octets)
        :param dedicatedKey:
        :param isXml:           True: 返回XML数据, False: 返回PDU 数据
        :return:

        Example-1:

        ---------------------------------

        conn = KaifaDLMS()

        conn.setClientSystemTitle('0000000000001900')

        conn.setAuthMechanism('ecdsa')

        info(conn.createAARQRequest(getRandomString(32)))

        Response:

        ====================================================

        <AssociationRequest>
            <ApplicationContextName Value="LNC" />

            <SenderACSERequirements Value="1" />

            <CallingAPTitle Value="0000000000001900" />

            <MechanismName Value="HIGH_SECURITY_ECDSA" />

            <CallingAuthenticationValue Value="592D417C3C325D4E2E222E2352792A27453B6C7D283B4F3563727A5C73616970" />

            <CipheredInitiateRequest Value="21080102030405060708080000000000001900084B464D10300000010000001F3100002E7981
            0AD03D5DBCF668655F1C12B4239BDAD6021011B7A8F3FD4198" />
        </AssociationRequest>


        Example-2:

        ---------------------------------

        conn = KaifaDLMS()

        conn.setApplicationContextName('LN')

        conn.setClientSystemTitle('0000000000001900')

        conn.setAuthMechanism('ecdsa')

        info(conn.createAARQRequest(getRandomString(32)))

        Response:

        ====================================================

        <AssociationRequest>

            <ApplicationContextName Value="LN" />

            <SenderACSERequirements Value="1" />

            <CallingAPTitle Value="0000000000001900" />

            <MechanismName Value="HIGH_SECURITY_ECDSA" />

            <CallingAuthenticationValue Value="EC4C38889A3996E012DF9AF3B065175879823F749741AA5E378A76177200A18B" />

            <InitiateRequest>

                <ProposedDlmsVersionNumber Value="06" />

                <ProposedConformance>

                    <ConformanceBit Name="GeneralProtection" />

                    <ConformanceBit Name="GeneralBlockTransfer" />

                    <ConformanceBit Name="Action" />

                    <ConformanceBit Name="BlockTransferWithAction" />

                    <ConformanceBit Name="BlockTransferWithGet" />

                    <ConformanceBit Name="BlockTransferWithSet" />

                    <ConformanceBit Name="EventNotification" />

                    <ConformanceBit Name="Get" />

                    <ConformanceBit Name="InformationReport" />

                    <ConformanceBit Name="MultipleReferences" />

                    <ConformanceBit Name="SelectiveAccess" />

                    <ConformanceBit Name="Set" />

                </ProposedConformance>

                <ProposedMaxPduSize Value="FFFD" />

            </InitiateRequest>

        </AssociationRequest>


        Example-3:

        ---------------------------------

        conn = KaifaDLMS()

        conn.setClientSystemTitle('0000000000001900')

        conn.setAuthMechanism('ecdsa')

        info(conn.createAARQRequest(isXml=False))

        Response:

        ====================================================

        60 7B A1 09 06 07 60 85 74 05 08 01 03 A6 0A 04 08 00 00 00 00 00 00 98 00
        8A 02 07 80 8B 07 60 85 74 05 08 02 06 AC 12 80 10 30 99 DB 65 58 30 1E C2
        7F 37 CC 91 A3 D8 02 E3 BE 41 04 3F 21 08 01 02 03 04 05 06 07 08 08 00 00
        00 00 00 00 98 00 08 4B 46 4D 10 30 00 00 01 00 00 00 1F 31 00 00 2E 9F A5
        81 F3 34 79 01 3C 32 C3 6C 05 56 86 7F AC AC E5 C3 13 3A 60 C6 34 46 57 82
        """
        if ctos is not None:
            ctos = UsefulFunction.OctetStringToByteArray(ctos)
        if dedicatedKey is not None:
            dedicatedKey = UsefulFunction.OctetStringToByteArray(dedicatedKey)
        return self.classDlms.DlmsConnect_GetXMLorPDU(ctos, dedicatedKey, isXml)


    def sendAARQRequest(self, reqData):
        """
        发送自定义 AARQ 报文   (发送之前确保 HDLC 连接成功)

        :param reqData:  支持 XML 和 PDU
        :return:         KFResult对象
        """
        info(f'** AARQRequest: {reqData}')
        response = None
        if isXmlOrPdu(reqData) == 'xml':
            response = self.classDlms.DlmsConnect_SendXMLorPDU(reqData, True, "")
        if isXmlOrPdu(reqData) == 'pdu':
            response = self.classDlms.DlmsConnect_SendXMLorPDU(reqData, False, "")

        # 成功时, 返回的 response 是一个元组; 第一个元素是状态, 第二个元素是响应内容
        if response is not None and response[0] == 1:
            return KFResult(True, response[1])
        else:
            return KFResult(False, f'Status Code: {response[0]}; Response: {response[1]}')


    def createAuthenticationRequest(self, ctos=None, dedicatedKey=None, data=None, isXml=True):
        """
        构造 reply_to_HLS authentication (Pass 3: C -> S f(StoC)) 请求数据

        :param ctos:            challenge client to server (Random string 8-64 octets)
        :param dedicatedKey:
        :param isXml:   True: 返回XML数据, False: 返回PDU 数据
        :param data:    方法 reply_to_HLS_ authentication 携带的数据内容 (client’s response to the challenge)
        :return:

        Example-1:

        ---------------------------------

        conn = KaifaDLMS()

        conn.createAuthenticationRequest()

        Response:

        ====================================================

        <ActionRequest>

            <ActionRequestNormal>

                <InvokeIdAndPriority Value="C1" />

                <MethodDescriptor>

                    <ClassId Value="000F" />

                    <InstanceId Value="0000280000FF" />

                    <MethodId Value="01" />

                </MethodDescriptor>

                <MethodInvocationParameters>

                    <OctetString Value="D7F20A4EE93A772CB133BF32C8FBABFAD729A8F9ACDC590A7E9B74B34C154923" />

                </MethodInvocationParameters>

            </ActionRequestNormal>

        </ActionRequest>


        Example-2:

        ---------------------------------

        conn = KaifaDLMS()

        conn.createAuthenticationRequest(data='aaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbb')

        Response:

        ====================================================

        <ActionRequest>

            <ActionRequestNormal>

                <InvokeIdAndPriority Value="C1" />

                <MethodDescriptor>

                    <ClassId Value="000F" />

                    <InstanceId Value="0000280000FF" />

                    <MethodId Value="01" />

                </MethodDescriptor>

                <MethodInvocationParameters>

                    <OctetString Value="aaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbb" />

                </MethodInvocationParameters>

            </ActionRequestNormal>

        </ActionRequest>


        Example-2:

        ---------------------------------

        conn = KaifaDLMS()

        conn.createAuthenticationRequest(isXml=False)

        Response:

        ====================================================

        C3 01 C1 00 0F 00 00 28 00 00 FF 01 01 09 20 D7 F2 0A 4E E9 3A 77 2C B1 33 BF 32 C8 FB AB
        FA D7 29 A8 F9 AC DC 59 0A 7E 9B 74 B3 4C 15 49 23
        """
        status, response = self.classDlms.Identification_GetXMLorPDU(isXml, "")

        # 构造 Identification 报文前, 需要先构造 AARQRequest 报文
        if len(response) == 0:
            response = self.createAARQRequest(ctos=ctos, dedicatedKey=dedicatedKey, isXml=isXml)

        if isXml and data is not None:
            return re.sub('OctetString Value="(\w+)"', f'OctetString Value="{data}"', response)
        else:
            return response


    def sendAuthenticationRequest(self, reqData):
        """
        发送 reply_to_HLS authentication (Pass 3: C -> S f(StoC)) 请求  (发送之前确保 HDLC 连接成功)

        :param reqData:  支持 XML 和 PDU
        :return:         KFResult对象
        """
        info(f'** AuthenticationRequest: {reqData}')
        response = None
        if isXmlOrPdu(reqData) == 'xml':
            response = self.classDlms.Identification_SendXMLorPDU(reqData, True, "")
        if isXmlOrPdu(reqData) == 'pdu':
            response = self.classDlms.Identification_SendXMLorPDU(reqData, False, "")

        # 成功时, 返回的 response 是一个元组; 第一个元素是状态, 第二个元素是响应内容
        if response is not None and response[0] == 1:
            return KFResult(True, response[1])
        else:
            return KFResult(False, f'Status Code: {response[0]}; Response: {response[1]}')


    def sendPduDirectly(self, pdu):
        """
        直接发送 pdu 数据数据, 不做任何预处理 (发送之前确保 HDLC 连接成功)

        :param pdu:  待发送的PDU 数据
        :return:
        """
        pdu = pdu.strip().replace(" ", "")
        response = self.classDlms.DirectlySendAndRecvPdu_NonSecurity(pdu)
        try:
            return pdu2Xml(response)
        except:
            return response


    def hdlcConnect(self):
        """
        实现 HDLC 连接

        :return:    返回 KFResult 对象

        Example:
        ---------------------------------
        conn = KaifaDLMS(isConnect=False)
        conn.hdlcConnect()
        """
        response = self.classDlms.HdlcConnect()
        if int(response) == 1:
            return KFResult(True, '')
        else:
            return KFResult(False, ConnectStatus[str(response)])


    def hdlcDisconnect(self):
        """
        断开 HDLC 连接

        :return:    None

        Example:
        ---------------------------------
        conn = KaifaDLMS(isConnect=False)
        conn.hdlcDisconnect()
        """
        try:
            self.classDlms.HdlcDisconnect()
        except BaseException:
            pass



    ###########################################################################################################

    @formatResponse
    def getWithList(self, data):
        """
        获取多个obis的值

        :param data:
        :return:

        data = {
            # '7,1.0.99.1.0.255,2' : {1, startime, endtime, [capture_objects]},
            0 : {'7,1.0.99.1.0.255,2' : [1, '05740806FF093400008000FF', '05740806FF0A3300008000FF', ['8,0.0.1.0.0.255', '1,0.0.96.10.1.255,2,0']]},

            # '7,1.0.99.1.1.255,2' : {2, startentry, endentry, startCaptureIndex, endCaptureIndex},
            1 : {'7,1.0.99.1.0.255,2' : [2, 1, 100]},

            2 : {'7,1.0.99.1.0.255,2' : None},
        }
        """
        getRequest = etree.Element('GetRequest')
        requestWithList = etree.SubElement(getRequest, 'GetRequestWithList')
        etree.SubElement(requestWithList, 'InvokeIdAndPriority').set('Value', 'C1')
        attrList = etree.SubElement(requestWithList, 'AttributeDescriptorList')
        attrList.set('Qty', dec_toHexStr(len(data), 4))

        # 记录obis-list, 用于打印日志
        obisList = list()
        dataList = list()
        for obj in data.values():
            for key, value in obj.items():
                classId, obis, attrId = key.split(',')
                obisList.append((classId, obis, attrId))
                dataList.append(value)

                _attrDescWithSelect = etree.SubElement(attrList, '_AttributeDescriptorWithSelection')
                attrDesc = etree.SubElement(_attrDescWithSelect, 'AttributeDescriptor')
                etree.SubElement(attrDesc, 'ClassId').set('Value', dec_toHexStr(classId, 4))
                etree.SubElement(attrDesc, 'InstanceId').set('Value', obis_toHex(obis))
                etree.SubElement(attrDesc, 'AttributeId').set('Value', dec_toHexStr(attrId, 2))
                if value is not None and len(value) > 0:
                    accessSelect = etree.SubElement(_attrDescWithSelect, 'AccessSelection')
                    accessMode = value[0]

                    # by_range
                    if int(accessMode) == 1:
                        etree.SubElement(accessSelect, 'AccessSelector').set('Value', '01')
                        accessParams = etree.SubElement(accessSelect, 'AccessParameters')
                        struct = etree.SubElement(accessParams, 'Structure')
                        struct.set('Qty', '0004')

                        # time range
                        subStruct = etree.SubElement(struct, "Structure")
                        subStruct.set("Qty", "0004")
                        etree.SubElement(subStruct, "LongUnsigned").set("Value", "0008")
                        etree.SubElement(subStruct, "OctetString").set("Value", "0000010000FF")  # Clock OBIS
                        etree.SubElement(subStruct, "Integer").set("Value", "02")
                        etree.SubElement(subStruct, "LongUnsigned").set("Value", "0000")

                        # start_time
                        if value[1].find("-") == -1 or value[1].find(":") == -1:
                            # 如果start_time是16进制, 则不进行数据格式转换
                            etree.SubElement(struct, "OctetString").set("Value", str(value[1]))
                        else:
                            etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(value[1]))

                        # end_time
                        if value[2].find("-") == -1 or value[2].find(":") == -1:
                            # 如果end_time是16进制, 则不进行数据格式转换
                            etree.SubElement(struct, "OctetString").set("Value", str(value[2]))
                        else:
                            etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(value[2]))

                        # selected_values
                        if len(value) == 4 and isinstance(value[3], list) and len(value[3]) > 0:
                            subArray = etree.SubElement(struct, "Array")
                            subArray.set("Qty", dec_toHexStr(len(value[3]), 4))
                            for item in value[3]:
                                sub2Struct = etree.SubElement(subArray, "Structure")
                                sub2Struct.set("Qty", "0004")
                                etree.SubElement(sub2Struct, "LongUnsigned").set("Value", dec_toHexStr(item.split(',')[0], 4))
                                etree.SubElement(sub2Struct, "OctetString").set("Value", obis_toHex(item.split(',')[1]))
                                if len(item.split(',')) >= 3:
                                    etree.SubElement(sub2Struct, "Integer").set("Value", dec_toHexStr(item.split(',')[2], 2))
                                else:
                                    etree.SubElement(sub2Struct, "Integer").set("Value", "02")
                                if len(item.split(',')) == 4:
                                    etree.SubElement(sub2Struct, "LongUnsigned").set("Value", dec_toHexStr(item.split(',')[3], 4))
                                else:
                                    etree.SubElement(sub2Struct, "LongUnsigned").set("Value", "0000")
                        else:
                            etree.SubElement(struct, "Array").set("Qty", "0000")

                    # by_entry
                    if int(accessMode) == 2:
                        etree.SubElement(accessSelect, 'AccessSelector').set('Value', '02')
                        accessParams = etree.SubElement(accessSelect, 'AccessParameters')
                        struct = etree.SubElement(accessParams, 'Structure')
                        struct.set('Qty', '0004')

                        # from_entry
                        etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(value[1], 8))
                        # to_entry
                        etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(value[2], 8))
                        # from_selected_value
                        if len(value) >= 4:
                            etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(value[3], 4))
                        else:
                            etree.SubElement(struct, "LongUnsigned").set("Value", '0001')
                        # to_selected_value
                        # etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(endCaptureIndex, 4))
                        if len(value) == 5:
                            etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(value[4], 4))
                        else:
                            etree.SubElement(struct, "LongUnsigned").set("Value", '0000')

        info(f'## Request  ## : Class: "DlmsLib": Service: "GetWithList", Object: {formatDict(obisList, isInputData=True)}, Data: {formatDict(dataList, isInputData=True)}')
        response = self.receiveXmlOrPdu(etree.tostring(getRequest).decode('ascii'))

        if response is None or len(response.strip()) == 0:
            error('** SYSTEM ERROR ** : Cannot analysis response!')
            return

        # 数据切割, 提取`<Data>...</Data>`
        lst = re.split(r'<Data>|</Data>', response.replace("\n", "").replace("  ", ""))
        lst = [f'<Data>{item}</Data>' for item in lst if '<' in item and '/>' in item][1:]

        ret = dict()
        for index, item in enumerate(lst):
            for key, _ in data[index].items():
                classId, obis, attrId = key.split(",")
                # 根据 classId 获取对应的类对象
                cls = globals()[ClassInterfaceMap[classId]](None, obis)
                # 根据 attrId 获取对应的函数名字符串
                methodName = 'get_' + cls.attr_index_dict[int(attrId)]
                # 根据函数名字符串获取对应的函数
                method = getattr(cls, methodName)
                # 执行函数
                ret[index] = method(response=item)
        return ret



    def setWithList(self, data):
        """
        设置多个obis的值

        :param data:
        :return:

        data10 = '05740811FF0B3700008000FF'
        data9 = {
            0: [0, [['7:0', '0.0.10.0.100.255', '2'], ['11:0', '0.0.10.0.100.255', '1'], ['15:0', '0.0.10.0.100.255', '2'], ['23:0', '0.0.10.0.100.255', '2']]],
            1: [1, [['5:0', '0.0.10.0.100.255', '2'], ['17:0', '0.0.10.0.100.255', '1'], ['21:0', '0.0.10.0.100.255', '2']]]
        }
        data8 = {
            0: ['1', 0, 0, 0, 0, 0, 0, 0],
            1: ['2', 0, 0, 0, 0, 0, 0, 0]
        }
        data7 = {
            0: ['1', 'FFFF-01-02-FF-FF-FF-FF-FF-8000-00', '1'],
            1: ['2', 'FFFF-06-01-FF-FF-FF-FF-FF-8000-00', '2']
        }
        data = {
            0: {'20,0-0:13.0.0.255,9'  : data9},
            1: {'20,0-0:13.0.0.255,8'  : data8},
            2: {'20,0-0:13.0.0.255,7'  : data7},
            3: {'20,0-0:13.0.0.255,10' : data10},
        }
        """
        setRequest = etree.Element('SetRequest')
        requestWithList = etree.SubElement(setRequest, 'SetRequestNormalWithList')
        etree.SubElement(requestWithList, 'InvokeIdAndPriority').set('Value', 'C1')

        attrList = etree.SubElement(requestWithList, 'AttributeDescriptorList')
        attrList.set('Qty', dec_toHexStr(len(data), 4))

        # 记录obis-list, 用于打印日志
        obisList = list()
        dataList = list()
        for obj in data.values():
            for key in obj:
                classId, obis, attrId = key.split(',')
                obisList.append((classId, obis, attrId))
                dataList.append(obj[key])

                _attrDescWithSelect = etree.SubElement(attrList, '_AttributeDescriptorWithSelection')
                attrDesc = etree.SubElement(_attrDescWithSelect, 'AttributeDescriptor')
                etree.SubElement(attrDesc, 'ClassId').set('Value', dec_toHexStr(classId, 4))
                etree.SubElement(attrDesc, 'InstanceId').set('Value', obis_toHex(obis))
                etree.SubElement(attrDesc, 'AttributeId').set('Value', dec_toHexStr(attrId, 2))

        valList = etree.SubElement(requestWithList, 'ValueList')
        valList.set('Qty', dec_toHexStr(len(data), 4))
        for obj in data.values():
            for key, value in obj.items():
                classId, obis, attrId = key.split(",")
                # 根据 classId 获取对应的类对象
                cls = globals()[ClassInterfaceMap[classId]](None, obis)
                # 根据 attrId 获取对应的函数名字符串
                methodName = 'set_' + cls.attr_index_dict[int(attrId)]
                # 根据函数名字符串获取对应的函数
                method = getattr(cls, methodName)
                # 执行函数
                result = method(value)
                valList.append(etree.fromstring(result))

        info(f'## Request  ## : Class: "DlmsLib": Service: "SetWithList", Object: {formatDict(obisList, isInputData=True)}, Data: {formatDict(dataList, isInputData=True)}')
        response = self.receiveXmlOrPdu(etree.tostring(setRequest).decode('ascii'))
        if response is None or len(response.strip()) == 0:
            error('** SYSTEM ERROR ** : Cannot analysis response!')
            return
        return getResponseFromSetWithList(response)


    def actWithList(self, data):
        """
        :param data:
        :return:
        """
        actRequest = etree.Element('ActionRequest')
        actionWithList = etree.SubElement(actRequest, 'ActionRequestWithList')
        etree.SubElement(actionWithList, 'InvokeIdAndPriority').set('Value', 'C1')

        methodList = etree.SubElement(actionWithList, 'MethodDescriptorList')
        methodList.set('Qty', dec_toHexStr(len(data), 4))

        # 记录obis-list, 用于打印日志
        obisList = list()
        dataList = list()
        for obj in data.values():
            for key in obj:
                classId, obis, attrId = key.split(',')
                obisList.append((classId, obis, attrId))
                dataList.append(obj[key])

                _methodDescriptor = etree.SubElement(methodList, '_MethodDescriptor')
                etree.SubElement(_methodDescriptor, 'ClassId').set('Value', dec_toHexStr(classId, 4))
                etree.SubElement(_methodDescriptor, 'InstanceId').set('Value', obis_toHex(obis))
                etree.SubElement(_methodDescriptor, 'MethodId').set('Value', dec_toHexStr(attrId, 2))

        methodParams = etree.SubElement(actionWithList, 'MethodInvocationParameters')
        methodParams.set('Qty', dec_toHexStr(len(data), 4))
        for obj in data.values():
            for key, value in obj.items():
                classId, obis, attrId = key.split(",")
                # 根据 classId 获取对应的类对象
                cls = globals()[ClassInterfaceMap[classId]](None, obis)
                # 根据 attrId 获取对应的函数名字符串
                methodName = 'act_' + cls.action_index_dict[int(attrId)]
                # 根据函数名字符串获取对应的函数
                method = getattr(cls, methodName)
                # 执行函数
                result = method(value)
                methodParams.append(etree.fromstring(result))

        info(f'## Request  ## : Class: "DlmsLib": Service: "ActWithList", Object: {formatDict(obisList, isInputData=True)}, Data: {formatDict(dataList, isInputData=True)}')
        response = self.receiveXmlOrPdu(etree.tostring(actRequest).decode('ascii'))
        return response


    def accessRequest(self, data, selfDescriptive=False, processingOption=False, serviceClass=True, priority=False, sendTime=""):
        """
        :param data:
        :param selfDescriptive:
        :param processingOption:
        :param serviceClass:
        :param priority:
        :param sendTime:
        :return:

        data = {
            0: {'7,1.0.99.1.0.255,7,GET': ""},
            1: {'20,0-0:13.0.0.255,9,GET': ""},
            2: {'7,1-0:99.2.0.255,2,GET': ""},
            3: {'20,0-0:13.0.0.255,1,ACTION': ""},
        }
        conn = KaifaDLMS(conformance=['multiple-references', 'get', 'set', 'selective-access', 'action', 'access'])
        response = conn.accessRequest(data)
        """
        longInvokeIdAndPriority = ['0'] * 32
        if priority:
            longInvokeIdAndPriority[0] = '1'
        if serviceClass:
            longInvokeIdAndPriority[1] = '1'
        if processingOption:
            longInvokeIdAndPriority[2] = '1'
        if selfDescriptive:
            longInvokeIdAndPriority[3] = '1'
        longInvokeIdAndPriority = "".join(longInvokeIdAndPriority)


        accessRequest = etree.Element("AccessRequest")
        etree.SubElement(accessRequest, 'LongInvokeIdAndPriority').set("Value", dec_toHexStr(int(longInvokeIdAndPriority, 2), 8))
        etree.SubElement(accessRequest, 'OctetString').set("Value", dateTime_toHex(sendTime))
        requestBody = etree.SubElement(accessRequest, 'AccessRequestBody')
        requestList = etree.SubElement(requestBody, 'ListOfAccessRequestSpecification')
        requestList.set("Qty", dec_toHexStr(len(data), 4))

        valueList = etree.SubElement(requestBody, 'ValueList')
        valueList.set("Qty", dec_toHexStr(len(data), 4))

        # 记录obis-list, 用于打印日志
        obisList = list()
        dataList = list()
        for obj in data.values():
            for key, value in obj.items():
                classId, obis, attrId, category = key.split(",")
                obisList.append((classId, obis, attrId))
                dataList.append(value)

                # ListOfAccessRequestSpecification
                attributeDescriptor = None
                if category.lower() == 'get':
                    accessGet = etree.SubElement(requestList, 'AccessRequestGet')
                    attributeDescriptor = etree.SubElement(accessGet, 'AttributeDescriptor')

                if category.lower() == 'set':
                    accessSet = etree.SubElement(requestList, 'AccessRequestSet')
                    attributeDescriptor = etree.SubElement(accessSet, 'AttributeDescriptor')

                if category.lower() == 'action':
                    accessAction = etree.SubElement(requestList, 'AccessRequestAction')
                    attributeDescriptor = etree.SubElement(accessAction, 'AttributeDescriptor')

                etree.SubElement(attributeDescriptor, 'ClassId').set('Value', dec_toHexStr(classId, 4))
                etree.SubElement(attributeDescriptor, 'InstanceId').set('Value', obis_toHex(obis))
                etree.SubElement(attributeDescriptor, 'AttributeId').set('Value', dec_toHexStr(attrId, 2))

                # ValueList
                if value is not None and len(value) > 0:
                    if category.lower() == 'get':
                        accessSelect = etree.SubElement(valueList, 'AccessSelection')
                        accessMode = value[0]

                        # by_range
                        if int(accessMode) == 1:
                            etree.SubElement(accessSelect, 'AccessSelector').set('Value', '01')
                            accessParams = etree.SubElement(accessSelect, 'AccessParameters')
                            struct = etree.SubElement(accessParams, 'Structure')
                            struct.set('Qty', '0004')

                            # time range
                            subStruct = etree.SubElement(struct, "Structure")
                            subStruct.set("Qty", "0004")
                            etree.SubElement(subStruct, "LongUnsigned").set("Value", "0008")
                            etree.SubElement(subStruct, "OctetString").set("Value", "0000010000FF")  # Clock OBIS
                            etree.SubElement(subStruct, "Integer").set("Value", "02")
                            etree.SubElement(subStruct, "LongUnsigned").set("Value", "0000")

                            # start_time
                            if value[1].find("-") == -1 or value[1].find(":") == -1:
                                # 如果start_time是16进制, 则不进行数据格式转换
                                etree.SubElement(struct, "OctetString").set("Value", str(value[1]))
                            else:
                                etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(value[1]))

                            # end_time
                            if value[2].find("-") == -1 or value[2].find(":") == -1:
                                # 如果end_time是16进制, 则不进行数据格式转换
                                etree.SubElement(struct, "OctetString").set("Value", str(value[2]))
                            else:
                                etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(value[2]))

                            # selected_values
                            if len(value) == 4 and isinstance(value[3], list) and len(value[3]) > 0:
                                subArray = etree.SubElement(struct, "Array")
                                subArray.set("Qty", dec_toHexStr(len(value[3]), 4))
                                for item in value[3]:
                                    sub2Struct = etree.SubElement(subArray, "Structure")
                                    sub2Struct.set("Qty", "0004")
                                    etree.SubElement(sub2Struct, "LongUnsigned").set("Value", dec_toHexStr(item.split(',')[0], 4))
                                    etree.SubElement(sub2Struct, "OctetString").set("Value", obis_toHex(item.split(',')[1]))
                                    if len(item.split(',')) >= 3:
                                        etree.SubElement(sub2Struct, "Integer").set("Value", dec_toHexStr(item.split(',')[2], 2))
                                    else:
                                        etree.SubElement(sub2Struct, "Integer").set("Value", "02")
                                    if len(item.split(',')) == 4:
                                        etree.SubElement(sub2Struct, "LongUnsigned").set("Value", dec_toHexStr(item.split(',')[3], 4))
                                    else:
                                        etree.SubElement(sub2Struct, "LongUnsigned").set("Value", "0000")
                            else:
                                etree.SubElement(struct, "Array").set("Qty", "0000")

                        # by_entry
                        if int(accessMode) == 2:
                            etree.SubElement(accessSelect, 'AccessSelector').set('Value', '02')
                            accessParams = etree.SubElement(accessSelect, 'AccessParameters')
                            struct = etree.SubElement(accessParams, 'Structure')
                            struct.set('Qty', '0004')

                            # from_entry
                            etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(value[1], 8))
                            # to_entry
                            etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(value[2], 8))
                            # from_selected_value
                            if len(value) >= 4:
                                etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(value[3], 4))
                            else:
                                etree.SubElement(struct, "LongUnsigned").set("Value", '0001')
                            # to_selected_value
                            # etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(endCaptureIndex, 4))
                            if len(value) == 5:
                                etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(value[4], 4))
                            else:
                                etree.SubElement(struct, "LongUnsigned").set("Value", '0000')

                    if category.lower() == 'set':
                        # 根据 classId 获取对应的类对象
                        cls = globals()[ClassInterfaceMap[classId]](None, obis)
                        # 根据 attrId 获取对应的函数名字符串
                        methodName = 'set_' + cls.attr_index_dict[int(attrId)]
                        # 根据函数名字符串获取对应的函数
                        method = getattr(cls, methodName)
                        # 执行函数
                        result = method(value)
                        valueList.append(etree.fromstring(result))

                    if category.lower() == 'action':
                        # 根据 classId 获取对应的类对象
                        cls = globals()[ClassInterfaceMap[classId]](None, obis)
                        # 根据 attrId 获取对应的函数名字符串
                        methodName = 'act_' + cls.attr_index_dict[int(attrId)]
                        # 根据函数名字符串获取对应的函数
                        method = getattr(cls, methodName)
                        # 执行函数
                        result = method(value)
                        valueList.append(etree.fromstring(result))

                else:
                    etree.SubElement(valueList, 'NullData')

        info(f'## Request  ## : Class: "DlmsLib": Service: "AccessRequest", Object: {formatDict(obisList, isInputData=True)}, Data: {formatDict(dataList, isInputData=True)}')
        # 发送 XML 并获取响应
        response = self.receiveXmlOrPdu(etree.tostring(accessRequest).decode('ascii'))

        # 解析响应
        if response is None or len(response.strip()) == 0:
            error('** SYSTEM ERROR ** : Cannot analysis response!')
            return

        root = etree.fromstring(response)
        # 提取执行结果并存储到List中
        retList = list()
        for ret in root.xpath("//Result"):
            retList.append(ret.attrib['Value'])

        lineNo = list()
        # 提取标签 ListOfData 包含的子节点行号 (行号减 1)
        for node in root.xpath("//ValueList/*"):
            lineNo.append(node.sourceline - 1)

        # 提取标签 ListOfAccessResponseSpecification 的行号作为结束点 (行号减 2)
        for node in root.xpath("//ListOfAccessResponseSpecification"):
            lineNo.append(node.sourceline - 2)

        result = dict()
        # 将 response 切割成 list
        lines = response.split("\n")
        for index in range(len(lineNo) - 1):
            subResponse = ''.join(lines[lineNo[index]: lineNo[index + 1]]).strip()
            if 'NullData' in subResponse:
                result[index] = (retList[index], '')
            else:
                # 返回值不是'Array'或'Structure'时, 需要额外添加'<Data>'和'</Data>'标签, 否则解析失败
                if 'Array' not in subResponse and 'Structure' not in subResponse:
                    subResponse = '<Data>' + subResponse + '</Data>'

                for key, _ in data[index].items():
                    classId, obis, attrId, _ = key.split(",")
                    # 根据 classId 获取对应的类对象
                    cls = globals()[ClassInterfaceMap[classId]](None, obis)
                    # 根据 attrId 获取对应的函数名字符串
                    methodName = 'get_' + cls.attr_index_dict[int(attrId)]
                    # 根据函数名字符串获取对应的函数
                    method = getattr(cls, methodName)
                    # 执行函数
                    result[index] = (retList[index], method(response=subResponse))
        return result



    def timedWait(self, sec, reason, offset=0):
        """
        DCU和Ip模式连接时，长时间Sleep后会导致连接断开，需要重连（时间至少要大于一分钟才使用此方法）

        :param sec:       等待时间
        :param offset     偏移量（操作步骤比较多时DCU比红外耗时更久，可以通过减去这个偏移量保证sleep时间一致）
        """
        if Singleton().Communication != "HDLC":
            info(f"Sleep {sec}s, Reason: {reason} ...")

            # 默认连接操作会耗时30s
            self.disconnect()
            time.sleep(sec-30-offset)             # 此处减去断开重连所需要的时间

            # 计算实际连接所用的时间， 然后再sleep
            startTime = time.time()
            self.connect()
            elapsedTime = time.time() - startTime

            if 30 - elapsedTime > 0:
                time.sleep(30 - elapsedTime)
        else:
            timedWait(sec, reason)

def disconnectDevice(conn):
    """
    断开设备连接

    :param conn:  连接对象
    :return:
    """
    if conn is not None:
        if isinstance(conn, KaifaDLMS):
            try:
                conn.disconnect()
            except:
                pass



