# -*- coding: UTF-8 -*-


from lxml import etree
from comms import *
from .Constants import *
from .Singleton import Singleton
from .DllLoader import *


# import os
# kaifDlmsDll = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dll\KaifaDlms")
#
# import clr
# clr.AddReference(kaifDlmsDll)
# # from Kaifa.DLMS import UsefulFunction, PduXml, ClassDLMS, KeyPairInfo, CommunicationLog, DLMSStateChange
# from Kaifa.DLMS import *


class ApduParser(object):

    def __init__(self):
        self.eKey = Singleton().EKey
        self.aKey = Singleton().AKey
        self.systemTitleClient = Singleton().SystemTitleClient
        self.systemTitleServer = Singleton().SystemTitleServer
        self.clientPublicKeySigning = Singleton().ClientPublicKeySigning
        self.serverPublicKeySigning = Singleton().ServerPublicKeySigning

    def decipheringApdu(self, apdu, direction):
        """
        破译APDU

        :param apdu:        apdu数据
        :param direction:   字符串（send/recv）
        :return:            解析后的数据
        """
        # 优先使用全局变量 SystemTitleServer
        if len(Singleton().SystemTitleServer) != 0:
            self.systemTitleServer = Singleton().SystemTitleServer

        if len(self.eKey) == 0 or len(self.aKey) == 0 or (len(self.systemTitleClient) == 0 and len(self.systemTitleServer) == 0):
            return apdu
        else:
            if direction == "send":  # 发送请求
                # decipherApdu = UsefulFunction.ByteArrayToOctetString(ClassDLMS().DecipheringApdu(self.eKey, self.aKey, "", self.systemTitleClient, self.clientPublicKeySigning, apdu))
                decipherApdu = decipheringApdu(eKey=self.eKey, aKey=self.aKey, sysTitleServer=self.systemTitleClient, pubKeySigning=self.clientPublicKeySigning, apdu=apdu)[0]
                # info(f"Send: eKey: {self.eKey}")
                # info(f"Send: aKey: {self.aKey}")
                # info(f"Send: systemTitleClient: {self.systemTitleClient}")
                # info(f"Send: systemTitleServer: {self.systemTitleServer}")
                # info(f"Send: clientPublicKeySigning: {self.clientPublicKeySigning}")
                # info(f"Send: apdu: {apdu}")
                # info(f"Send: decipherApdu: {decipherApdu}")
                return decipherApdu

            else:
                # decipherApdu = UsefulFunction.ByteArrayToOctetString(ClassDLMS().DecipheringApdu(self.eKey, self.aKey, self.systemTitleClient, self.systemTitleServer, self.serverPublicKeySigning, apdu))
                decipherApdu = decipheringApdu(eKey=self.eKey, aKey=self.aKey, sysTitleClient=self.systemTitleClient, sysTitleServer=self.systemTitleServer, pubKeySigning=self.serverPublicKeySigning, apdu=apdu)[0]
                # info(f"Recv: eKey: {self.eKey}")
                # info(f"Recv: aKey: {self.aKey}")
                # info(f"Recv: systemTitleClient: {self.systemTitleClient}")
                # info(f"Recv: systemTitleServer: {self.systemTitleServer}")
                # info(f"Recv: serverPublicKeySigning: {self.serverPublicKeySigning}")
                # info(f"Recv: apdu: {apdu}")
                # info(f"Recv: decipherApdu: {decipherApdu}")
                return decipherApdu

    def parsePdu(self, hexStr):
        """
        解析pdu

        :param hexStr:   16进制字符串
        :return:         解析后的pdu
        """
        # 删除首尾空格, 并转换成大写
        hexString = hexStr.strip().upper()

        # 标记是发送还是接收报文
        direction = ""
        if hexString.startswith("SEND"):
            direction = "send"
        if hexString.startswith("RECV"):
            direction = "recv"

        # 去除前导符('Send:14:14:33.613]', 'Recv:14:14:41.795]')
        if len(str(direction)) != 0:
            hexString = hexString[18:]

            # # 按空格切割字符串
            # hexLst = re.split(r'\s+', hexString)

            # 去除空格
            hexString = hexString.replace(' ', '')

            # FEP Header (去掉FEP头后即是标准WPDU报文)
            if hexString.startswith('68') and hexString.endswith('16'):
                hexString = hexString[90 : -4]

            # wrapper
            if hexString.startswith('0001'):
                # 反转 list
                hexLst = splitHexWithSpace(hexString, returnList=True)[::-1]
                return self.parseWrapperPdu(hexLst, direction)

            # HDLC
            if hexString.startswith('7E'):
                # 反转 list
                hexLst = splitHexWithSpace(hexString, returnList=True)[::-1]
                return self.parseHdlcPdu(hexLst, direction)

            # 直接返回None
            return None


    @staticmethod
    def parseWrapperPdu(hexLst, direction):
        """
        解析 Wrapper pdu

        :param hexLst:      16进制字符串列表
        :param direction:   字符串（send/recv）
        :return:            解析后的字符串
        """
        msg = list()
        # 插入aKey, eKey, SystemTitleClient, SystemTitleServer信息
        if len(Singleton().SystemTitleServer) != 0:
            msg.insert(0, f"SystemTitleServer: {Singleton().SystemTitleServer}")
        if len(Singleton().SystemTitleClient) != 0:
            msg.insert(0, f"SystemTitleClient: {Singleton().SystemTitleClient}")
        if len(Singleton().AKey) != 0:
            msg.insert(0, f"AuthenticationKey: {Singleton().AKey}")
        if len(Singleton().EKey) != 0:
            msg.insert(0, f"EncryptionKeyGlobal: {Singleton().EKey}")

        # WPDU (wrapper protocol data unit) 8bytes
        for i in range(8):
            hexLst.pop()

        pduName = hexLst[-1]
        try:
            apduClass = globals()[PduClassMap[pduName]]()
            msg.extend(apduClass.parsePdu(hexLst))
        except KeyError:
            apduClass = DlmsDataApduParser()
            msg.extend(apduClass.parseData(hexLst, direction))

        return msg


    @staticmethod
    def parseGbtPdu(hexLst, direction):
        """
        将GBT分片报文转换成XML格式

        :param hexLst:      16进制字符串列表
        :param direction:   字符串（send/recv）
        :return:            解析后的xml
        """
        originData = hexLst.copy()
        originData.reverse()
        xmlData = pdu2Xml("".join(originData))

        # 删除前导Tag ['E0']
        hexLst.pop()
        gbtStatus = hexLst.pop()
        gbt_LB_bit = int(gbtStatus, 16) >> 7
        gbt_STR_bit = (int(gbtStatus, 16) << 1 & 0xFF) >> 7
        blockNumber = int(hexLst.pop() + hexLst.pop(), 16)

        # 记录LB=1时BN的值 (为防止被覆盖, 用List存储, 最后只取第一个元素)
        if gbt_LB_bit == 1:
            if direction == "send":
                Singleton().GbtSendBNList.append(blockNumber)
            else:
                Singleton().GbtRecvBNList.append(blockNumber)

        # skip block-number-acknowledged
        hexLst.pop() + hexLst.pop()

        # length
        lensTag = hexLst.pop()
        if lensTag == '83':
            lens = int(hexLst.pop() + hexLst.pop() + hexLst.pop(), 16)
        elif lensTag == '82':
            lens = int(hexLst.pop() + hexLst.pop(), 16)
        elif lensTag == '81':
            lens = int(hexLst.pop(), 16)
        else:
            lens = int(lensTag, 16)

        # 判断GBT中是否有数据 (特殊情况: Send:15:47:38.960]7E A0 14 02 23 0D 18 85 17 E6 E6 00 E0 83 00 03 00 06 00 FC FC 7E)
        if lens > 0:
            # pdu data
            pdus = list()
            for i in range(lens):
                pdus.append(hexLst.pop())

            # 以字典的形式存储GBT, 有利于处理GBT丢包情况
            if direction == "send":
                Singleton().GbtSendPackages[int(blockNumber)] = pdus
            else:
                Singleton().GbtRecvPackages[int(blockNumber)] = pdus

            # GBT报文收集完成:  LB = 1 & STR = 0 &  BN = len(Singleton().GbtPackages)
            totalGbtPdus = list()
            if gbt_LB_bit == 1 and gbt_STR_bit == 0:
                # 处理接收的GBT数据
                if len(Singleton().GbtRecvBNList) > 0 and len(Singleton().GbtRecvPackages) == Singleton().GbtRecvBNList[0]:
                    for i in range(1, len(Singleton().GbtRecvPackages) + 1):
                        totalGbtPdus.extend(Singleton().GbtRecvPackages[i])
                    # 清空数据
                    Singleton().GbtRecvPackages = dict()
                    Singleton().GbtRecvBNList = list()
                    # 反转数据
                    totalGbtPdus.reverse()
                    return totalGbtPdus

                # 处理发送的GBT数据
                if len(Singleton().GbtSendBNList) > 0 and len(Singleton().GbtSendPackages) == Singleton().GbtSendBNList[0]:
                    for i in range(1, len(Singleton().GbtSendPackages) + 1):
                        totalGbtPdus.extend(Singleton().GbtSendPackages[i])
                    # 清空数据
                    Singleton().GbtSendPackages = dict()
                    Singleton().GbtSendBNList = list()
                    # 反转数据
                    totalGbtPdus.reverse()
                    return totalGbtPdus

            else:
                # 返回包含两个元素的一个元组; 第一个元素是XML格式的数据, 第二个元素是PDU格式的数据
                return xmlData, "".join(pdus)

        # 1. GBT报文中不包含有效信息数据时返回空
        # 2. GBT分片报文没有接收完时返回空 (一个GBT可以被切分成多个HDLC报文, 需要注意区分差别)
        return ""


    @staticmethod
    def parseHdlcPdu(hexLst, direction):
        """
        解析 hdlc pdu

        :param hexLst:      16进制字符串列表
        :param direction:   字符串（send/recv）
        :return:            解析后的字符串
        """
        msg = list()
        # 检查Frame的结束位是否为7E
        tailflag = hexLst.pop(0)
        if tailflag != "7E":
            return

        # 帧校验序列 (长度两个字节)     优先提取FCS的目的是, 防止FCS的值与特定Tag重名, 导致程序出现误判
        fcs = hexLst.pop(1) + hexLst.pop(0)

        # 弹出'7E'
        hexLst.pop()
        # 分析是否还有后续帧
        frameType = hexLst.pop()
        if (int(frameType, 16) << 4 & 0xFF) >> 7 == 1:
            msg.append("Segment: True")
        else:
            msg.append("Segment: False")

        # 帧长度子域
        frameLen = (int(frameType + hexLst.pop(), 16) << 5 & 0xFFFF) >> 5
        msg.append(f"FrameLength: {frameLen}")

        # 目的HDLC地址
        dstAddr = getHdlcAddr(hexLst)
        # 源HDLC地址
        srcAddr = getHdlcAddr(hexLst)
        if len(dstAddr) == 1:
            msg.append(f"Client address: {dstAddr[0]}")
            msg.append(f"Server address: Upper={srcAddr[0]}, Lower={srcAddr[1]}")
        else:
            msg.append(f"Client address: {srcAddr[0]}")
            msg.append(f"Server address: Upper={dstAddr[0]}, Lower={dstAddr[1]}")

        # 控制域
        control = hexLst.pop()
        try:
            msg.append(f"Control Field: {ControlMap[control]}")
        except KeyError:
            msg.append(f"Control Field: {parseControlField(control, clientSend=False) if len(dstAddr) == 1 else parseControlField(control, clientSend=True)}")

        # hexLst.insert(0, 'FF')
        if len(hexLst) == 0:
            msg.append(f"HCS={fcs}")
            # 增加一个空元素, 代表DLMS Layer为空
            msg.append("")

        else:
            # 帧头校验序列 (长度两个字节)
            hcs = hexLst.pop() + hexLst.pop()
            msg.append(f"HCS={hcs}")

            # 将帧校验序列加入self.msg
            msg.append(f"FCS={fcs}")

            # 如果是分片报文, 保存数据部分后直接返回
            if "Segment: True" in msg:
                # hexLst.pop(0)       # 丢弃添加的后缀
                hexLst.reverse()

                if direction == "send":
                    Singleton().FragmentSendPackages.extend(hexLst)
                else:
                    Singleton().FragmentRecvPackages.extend(hexLst)

                msg.append(f"** This is one of HDLC segment frames **")
                # 增加一个空元素, 代表DLMS Layer为空
                msg.append("")

            else:
                # 如果不是分片报文, 且HDLC控制域为'I', 则追加报文
                if re.search('Control Field: "I" Frame', "".join(msg)):
                    if direction == "send":
                        Singleton().FragmentSendPackages.reverse()
                        hexLst.extend(Singleton().FragmentSendPackages)
                        Singleton().FragmentSendPackages = list()           # 清空全局变量
                    else:
                        Singleton().FragmentRecvPackages.reverse()
                        hexLst.extend(Singleton().FragmentRecvPackages)
                        Singleton().FragmentRecvPackages = list()           # 清空全局变量

                # 为了避免遍历时溢出, 以及Tag误判, 添加一个后缀
                hexLst.insert(0, 'FF')

                # 信息域
                if control in ["93", "73", "53", "OF"]:  # HDCL Frame
                    transLen, recvLen, transWindow, recvWindow = parseHdlcFrame(hexLst)
                    msg.append(f"Max transmit = {transLen}")
                    msg.append(f"Max receive = {recvLen}")
                    msg.append(f"Window transmit size = {transWindow}")
                    msg.append(f"Window receive size = {recvWindow}")
                    # 增加一个空元素, 代表DLMS Layer为空
                    msg.append("")

                else:
                    # 插入aKey, eKey, SystemTitleClient, SystemTitleServer信息
                    msg.insert(0, "")
                    if len(Singleton().SystemTitleServer) != 0:
                        msg.insert(0, f"SystemTitleServer: {Singleton().SystemTitleServer}")
                    if len(Singleton().SystemTitleClient) != 0:
                        msg.insert(0, f"SystemTitleClient: {Singleton().SystemTitleClient}")
                    if len(Singleton().AKey) != 0:
                        msg.insert(0, f"AuthenticationKey: {Singleton().AKey}")
                    if len(Singleton().EKey) != 0:
                        msg.insert(0, f"EncryptionKeyGlobal: {Singleton().EKey}")

                    # llcHeader [E6 E6 00] [E6 E7 00]
                    if hexLst[-1] == 'E6' and (hexLst[-2] == 'E6' or hexLst[-2] == 'E7') and hexLst[-3] == '00':
                        hexLst.pop() + hexLst.pop() + hexLst.pop()

                    # 判断是否为GBT报文(Tag: 'E0')
                    if hexLst[-1] == 'E0':
                        hexLst = ApduParser.parseGbtPdu(hexLst, direction)
                        if len(hexLst) == 0:
                            msg.append("")
                            return msg
                        if isinstance(hexLst, tuple):
                            msg.append(hexLst[0])
                            msg.append(f"** This is one of GBT segment frames **")
                            msg.append(hexLst[1])
                            return msg

                    pduName = hexLst[-1]
                    try:
                        apduClass = globals()[PduClassMap[pduName]]()
                        msg.extend(apduClass.parsePdu(hexLst))
                    except KeyError:
                        apduClass = DlmsDataApduParser()
                        msg.extend(apduClass.parseData(hexLst, direction))
        return msg


class AARQApduParser(ApduParser):
    """
    <xsd:complexType name="AARQ-apdu">

        <xsd:sequence>

            <xsd:element name="protocol-version" minOccurs="0">

                <xsd:simpleType>

                    <xsd:union memberTypes="BitString">

                        <xsd:simpleType>

                            <xsd:list>

                                <xsd:simpleType>

                                    <xsd:restriction base="xsd:token">

                                        <xsd:enumeration value="version1"/>

                                    </xsd:restriction>

                                </xsd:simpleType>

                            </xsd:list>

                        </xsd:simpleType>

                    </xsd:union>

                </xsd:simpleType>

            </xsd:element>

            <xsd:element name="application-context-name" type="Application-context-name"/>

            <xsd:element name="called-AP-title" minOccurs="0" type="AP-title"/>

            <xsd:element name="called-AE-qualifier" minOccurs="0" type="AE-qualifier"/>

            <xsd:element name="called-AP-invocation-id" minOccurs="0" type="AP-invocation-identifier"/>

            <xsd:element name="called-AE-invocation-id" minOccurs="0" type="AE-invocation-identifier"/>

            <xsd:element name="calling-AP-title" minOccurs="0" type="AP-title"/>

            <xsd:element name="calling-AE-qualifier" minOccurs="0" type="AE-qualifier"/>

            <xsd:element name="calling-AP-invocation-id" minOccurs="0" type="AP-invocation-identifier"/>

            <xsd:element name="calling-AE-invocation-id" minOccurs="0" type="AE-invocation-identifier"/>

            <xsd:element name="sender-acse-requirements" minOccurs="0" type="ACSE-requirements"/>

            <xsd:element name="mechanism-name" minOccurs="0" type="Mechanism-name"/>

            <xsd:element name="calling-authentication-value" minOccurs="0" type="Authentication-value"/>

            <xsd:element name="implementation-information" minOccurs="0" type="Implementation-data"/>

            <xsd:element name="user-information" minOccurs="0" type="Association-information"/>

        </xsd:sequence>

    </xsd:complexType>
    """

    def __init__(self, **argv):

        super(AARQApduParser, self).__init__()
        self.applicationContextName = argv.get("applicationContextName", "")
        self.callingApTitle = argv.get("callingApTitle", "")
        self.senderAcseRequirements = argv.get("senderAcseRequirements", "")
        self.mechanismName = argv.get("mechanismName", "")
        self.callingAuthenticationValue = argv.get("callingAuthenticationValue", "")
        self.userInformation = argv.get("userInformation", "")

    def toXml(self):
        """
        生成 XML 格式的 AARQ

        :return:    xml
        """
        decipherData = ""
        initiateRequestXml = ""

        root = etree.Element("AssociationRequest")
        if self.applicationContextName:
            etree.SubElement(root, "ApplicationContextName").set("Value", str(self.applicationContextName))
        if self.callingApTitle:
            etree.SubElement(root, "CallingAPTitle").set("Value", str(self.callingApTitle))
        if self.senderAcseRequirements:
            etree.SubElement(root, "SenderACSERequirements").set("Value", str(self.senderAcseRequirements))
        if self.mechanismName:
            etree.SubElement(root, "MechanismName").set("Value", str(self.mechanismName))
        if self.callingAuthenticationValue:
            etree.SubElement(root, "CallingAuthenticationValue").set("Value", str(self.callingAuthenticationValue))
        if self.userInformation:
            etree.SubElement(root, "CipheredInitiateRequest").set("Value", str(self.userInformation))
            try:
                # decrypting user-information
                decipherData = self.decipheringApdu(self.userInformation, direction="send")
                initiateRequestXml = pdu2Xml(decipherData)
            except:
                # no ciphered information
                decipherData = ""
                initiateRequestXml = pdu2Xml(self.userInformation)

        xmlStr = etree.tostring(root, encoding="utf-8", pretty_print=True).decode()
        if len(xmlStr) != 0:
            return xmlStr + "\n" + initiateRequestXml, decipherData
        else:
            return initiateRequestXml, decipherData

    def parsePdu(self, hexList):
        """
        解析 AARQ APDU

        :param hexList: 60 63 A1 09 06 07 60 85 74 05 08 01 03 A6 0A 04 08 49 4E 44 01 02 03 04 05 8A 02 07 80 8B 07 60 85 74 05 08 02 06 AC 18 80 16 5C 52 27 6A 41 64 79 4E 29 2D 29 59 24 54 4A 24 52 23 7D 2F 4E 2E BE 23 04 21 21 1F 30 00 00 13 8C F9 70 0E F1 53 8A CE 17 F2 84 3A 88 13 3E 65 08 AD A0 E6 63 DB D4 7B 8D 30 8E
                         -- 注： 传入进来的list 是反序的
        :return:   xml
        """
        if hexList.pop() != "60":
            raise Exception("Not AARQ APDU Frame!")
        hexList.pop()  # length of the AARQ's contents

        while len(hexList) > 0:
            tag = hexList.pop()
            if tag.upper() == "A1":  # application-context-name
                hexList.pop()  # length of application-context-name
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()  # lenght of value
                for i in range(hex_toDec(tagLen)):
                    self.applicationContextName = hexList.pop()  # In fact , I only need the last value, haha!

                # 将16进制application-context-name转换成可识别的字符串
                if self.applicationContextName == "01":
                    self.applicationContextName = "LN"
                if self.applicationContextName == "03":
                    self.applicationContextName = "LNC"

            elif tag.upper() == "A6":  # calling-AP-title
                hexList.pop()  # length of calling-AP-title
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):
                    self.callingApTitle += hexList.pop()

            elif tag.upper() == "8A":  # sender-acse-requirements
                hexList.pop()  # length of sender-acse-requirements
                hexList.pop()  # data type of tag
                self.senderAcseRequirements = hex_toDec(hexList.pop()) >> 7

            elif tag.upper() == "8B":  # mechanism-name
                tagLen = hexList.pop()  # length of mechanism-name
                for i in range(hex_toDec(tagLen)):
                    self.mechanismName = hexList.pop()
                self.mechanismName = MechanismMap[str(hex_toDec(self.mechanismName))]

            elif tag.upper() == "AC":  # calling-authentication-value
                hexList.pop()  # length of calling-authentication-value
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):
                    self.callingAuthenticationValue += hexList.pop()

            elif tag.upper() == "BE":  # user-information
                hexList.pop()  # length of user-information
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):
                    self.userInformation += hexList.pop()

        return self.toXml()


class InitRequestApduParser(ApduParser):
    """
    <xsd:complexType name="InitiateRequest">

        <xsd:sequence>

            <xsd:element name="dedicated-key" minOccurs="0" type="xsd:hexBinary"/>

            <xsd:element name="response-allowed" default="true" type="xsd:boolean"/>

            <xsd:element name="proposed-quality-of-service" minOccurs="0" type="Integer8"/>

            <xsd:element name="proposed-dlms-version-number" type="Unsigned8"/>

            <xsd:element name="proposed-conformance" type="Conformance"/>

            <xsd:element name="client-max-receive-pdu-size" type="Unsigned16"/>

        </xsd:sequence>

    </xsd:complexType>
    """

    def __init__(self, **argv):

        super(InitRequestApduParser, self).__init__()
        self.dedicatedKey = argv.get("dedicatedKey", "")
        self.responseAllowed = argv.get("responseAllowed", "")
        self.proposedQualityOfService = argv.get("proposedQualityOfService", "")
        self.proposedDlmsVersion = argv.get("proposedDlmsVersion", "")
        self.proposedConformance = argv.get("proposedConformance", "")
        self.clientMaxReceivePduSize = argv.get("clientMaxReceivePduSize", "")

    def toXml(self):
        """
        生成 XML 格式的 InitiateRequest

        :return:   xml
        """
        root = etree.Element("InitiateRequest")
        if self.dedicatedKey != "00":
            etree.SubElement(root, "DedicatedKey").set("Value", str(self.dedicatedKey))
        if self.responseAllowed != "00":
            etree.SubElement(root, "ResponseAllowed").set("Value", str(self.responseAllowed))
        if self.proposedQualityOfService != "00":
            etree.SubElement(root, "ProposedQualityOfService").set("Value", str(self.proposedQualityOfService))
        if self.proposedDlmsVersion:
            etree.SubElement(root, "ProposedDlmsVersion").set("Value", str(self.proposedDlmsVersion))
        if self.proposedConformance:
            conformance = etree.SubElement(root, "ProposedConformance")
            for index, item in enumerate(self.proposedConformance):
                if int(item) == 1:
                    etree.SubElement(conformance, "ConformanceBit").set("Name", ConformanceMap[str(index)])
        if self.clientMaxReceivePduSize:
            etree.SubElement(root, "ProposedMaxPduSize").set("Value", str(self.clientMaxReceivePduSize))

        return etree.tostring(root, encoding="utf-8", pretty_print=True).decode()

    def parsePdu(self, hexList):
        """
        解析 InitiateRequest

        :param hexList:   解密后的字符串 01 00 00 00 06 5F 1F 04 00 60 1A 5D 00 EF
        :return:  xml
        """
        if hexList.pop() != "01":
            raise Exception("Not InitiateRequest Frame!")

        self.dedicatedKey = hexList.pop()
        self.responseAllowed = hexList.pop()
        self.proposedQualityOfService = hexList.pop()
        self.proposedDlmsVersion = hexList.pop()

        # proposed-conformance
        hexList.pop()  # 5F
        hexList.pop()  # 1F
        # length of conformance
        tagLen = hexList.pop()  # 04
        # data type of proposed-conformance
        hexList.pop()
        # content of proposed-conformance
        for i in range(hex_toDec(tagLen) - 1):
            self.proposedConformance += "{:08b}".format(hex_toDec(hexList.pop()))

        # client-max-receive-pdu-size (Unsigned16)
        self.clientMaxReceivePduSize += hexList.pop() + hexList.pop()

        return self.toXml()


class AAREApduParser(ApduParser):
    """
    <xsd:complexType name="AARE-apdu">

        <xsd:sequence>

            <xsd:element name="protocol-version" minOccurs="0">

                <xsd:simpleType>

                    <xsd:union memberTypes="BitString">

                        <xsd:simpleType>

                            <xsd:list>

                                <xsd:simpleType>

                                    <xsd:restriction base="xsd:token">

                                        <xsd:enumeration value="version1"/>

                                    </xsd:restriction>

                                </xsd:simpleType>

                            </xsd:list>

                        </xsd:simpleType>

                    </xsd:union>

                </xsd:simpleType>

            </xsd:element>

            <xsd:element name="application-context-name" type="Application-context-name"/>

            <xsd:element name="result" type="Association-result"/>

            <xsd:element name="result-source-diagnostic" type="Associate-source-diagnostic"/>

            <xsd:element name="responding-AP-title" minOccurs="0" type="AP-title"/>

            <xsd:element name="responding-AE-qualifier" minOccurs="0" type="AE-qualifier"/>

            <xsd:element name="responding-AP-invocation-id" minOccurs="0" type="AP-invocation-identifier"/>

            <xsd:element name="responding-AE-invocation-id" minOccurs="0" type="AE-invocation-identifier"/>

            <xsd:element name="responder-acse-requirements" minOccurs="0" type="ACSE-requirements"/>

            <xsd:element name="mechanism-name" minOccurs="0" type="Mechanism-name"/>

            <xsd:element name="responding-authentication-value" minOccurs="0" type="Authentication-value"/>

            <xsd:element name="implementation-information" minOccurs="0" type="Implementation-data"/>

            <xsd:element name="user-information" minOccurs="0" type="Association-information"/>

        </xsd:sequence>

    </xsd:complexType>
    """

    def __init__(self, **argv):

        super(AAREApduParser, self).__init__()
        self.applicationContextName = argv.get("applicationContextName", "")
        self.result = argv.get("result", "")
        self.resultSourceDiagnostic = argv.get("resultSourceDiagnostic", "")
        self.respondingApTitle = argv.get("respondingApTitle", "")
        self.responderAcseRequirements = argv.get("responderAcseRequirements", "")
        self.mechanismName = argv.get("mechanismName", "")
        self.respondingAuthenticationValue = argv.get("respondingAuthenticationValue", "")
        self.userInformation = argv.get("userInformation", "")

    def toXml(self):
        """
        生成 XML 格式的 AARQ

        :return:   xml
        """
        decipherData = ""
        initiateResponseXml = ""

        root = etree.Element("AssociationResponse")
        if self.applicationContextName:
            etree.SubElement(root, "ApplicationContextName").set("Value", str(self.applicationContextName))
        if self.result:
            etree.SubElement(root, "AssociationResult").set("Value", str(self.result))
        if self.resultSourceDiagnostic:
            acseServiceUser = etree.SubElement(root, "ResultSourceDiagnostic")
            etree.SubElement(acseServiceUser, "AcseServiceUser").set("Value", str(self.resultSourceDiagnostic))
        if self.respondingApTitle:
            etree.SubElement(root, "RespondingAPTitle").set("Value", str(self.respondingApTitle))
        if self.responderAcseRequirements:
            etree.SubElement(root, "ResponderACSERequirement").set("Value", str(self.responderAcseRequirements))
        if self.mechanismName:
            etree.SubElement(root, "MechanismName").set("Value", str(self.mechanismName))
        if self.respondingAuthenticationValue:
            etree.SubElement(root, "RespondingAuthenticationValue").set("Value", str(self.respondingAuthenticationValue))
        if self.userInformation:
            etree.SubElement(root, "CipheredInitiateResponse").set("Value", str(self.userInformation))

            try:
                # decrypting user-information
                decipherData = self.decipheringApdu(self.userInformation, direction="recv")
                initiateResponseXml = pdu2Xml(decipherData)
            except:
                # no ciphered information
                decipherData = ""
                initiateResponseXml = pdu2Xml(self.userInformation)

        try:
            # 从解密后的PDU中提取Conformance (decipherData[-8:-2])
            Singleton().Conformance = bin(int(decipherData[-8:-2], 16)).replace('0b', '').rjust(24, '0')
        except:
            # 从明文PDU中提取Conformance
            Singleton().Conformance = bin(int(self.userInformation[-14:-8], 16)).replace('0b', '').rjust(24, '0')

        xmlStr = etree.tostring(root, encoding="utf-8", pretty_print=True).decode()
        if len(xmlStr) != 0:
            return xmlStr + "\n" + initiateResponseXml, decipherData
        else:
            return initiateResponseXml, decipherData

    def parsePdu(self, hexList):
        """
        解析 AARE APDU

        :param hexList: 61 6F A1 09 06 07 60 85 74 05 08 01 03 A2 03 02 01 00 A3 05 A1 03 02 01 0E A4 0A 04 08 4B 46 4D 10 70 00 00 2D 88 02 07 80 89 07 60 85 74 05 08 02 06 AA 18 80 16 DF AA 75 0B 22 49 14 CF 77 D5 4D F8 76 D5 81 F7 10 BB 60 82 84 7E BE 23 04 21 28 1F 30 00 00 01 26 7C E1 55 C6 F9 32 C2 9E 95 6C C1 35 9C E3 C9 6C F1 FF 88 55 90 D8 8B CC 65 0B
                         -- 注： 传入进来的list 是反序的
        :return:  xml
        """
        if hexList.pop() != "61":
            raise Exception("Not AARE APDU Frame!")
        hexList.pop()  # length of the AAEQ's contents

        while len(hexList) > 0:
            tag = hexList.pop()
            if tag.upper() == "A1":  # application-context-name
                hexList.pop()  # length of application-context-name
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()  # lenght of value
                for i in range(hex_toDec(tagLen)):
                    self.applicationContextName = hexList.pop()  # In fact , I only need the last value, haha!

                # 将16进制application-context-name转换成可识别的字符串
                if self.applicationContextName == "01":
                    self.applicationContextName = "LN"
                if self.applicationContextName == "03":
                    self.applicationContextName = "LNC"

            elif tag.upper() == "A2":  # result
                hexList.pop()  # lenght of tag
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()  # length of content
                for i in range(hex_toDec(tagLen)):
                    self.result += hexList.pop()

            elif tag.upper() == "A3":  # result-source-diagnostic
                hexList.pop()  # length of tag
                hexList.pop()  # data type of tag
                hexList.pop()  # length of content
                hexList.pop()  # subElement (associate-source-diagnostics)
                subTagLen = hexList.pop()  # length of subElement
                for i in range(hex_toDec(subTagLen)):
                    self.resultSourceDiagnostic += hexList.pop()

            elif tag.upper() == "A4":  # responding-AP-title
                hexList.pop()  # lenght of tag
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()  # length of content
                for i in range(hex_toDec(tagLen)):
                    self.respondingApTitle += hexList.pop()

                # 修改全局变量
                Singleton().SystemTitleServer = self.respondingApTitle
                # print(f"*** SystemTitleServer = {self.respondingApTitle} ***")

            elif tag.upper() == "88":  # responder-acse-requirements
                hexList.pop()  # length of tag
                hexList.pop()  # data type of tag
                self.responderAcseRequirements = hex_toDec(hexList.pop()) >> 7

            elif tag.upper() == "89":  # mechanism-name
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):
                    self.mechanismName = hexList.pop()
                self.mechanismName = MechanismMap[str(hex_toDec(self.mechanismName))]

            elif tag.upper() == "AA":  # responding-authentication-value
                hexList.pop()  # length of tag
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()  # length of content
                for i in range(hex_toDec(tagLen)):
                    self.respondingAuthenticationValue += hexList.pop()

            elif tag.upper() == "BE":  # user-information
                hexList.pop()  # length of user-information
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):
                    self.userInformation += hexList.pop()

        return self.toXml()


class InitResponseApduParser(ApduParser):
    """
    <xsd:complexType name="InitiateResponse">
        <xsd:sequence>
            <xsd:element name="negotiated-quality-of-service" minOccurs="0" type="Integer8"/>
            <xsd:element name="negotiated-dlms-version-number" type="Unsigned8"/>
            <xsd:element name="negotiated-conformance" type="Conformance"/>
            <xsd:element name="server-max-receive-pdu-size" type="Unsigned16"/>
            <xsd:element name="vaa-name" type="ObjectName"/>      // the value of the vaa-name is 0x0007 in LN referencing
        </xsd:sequence>
    </xsd:complexType>
    """

    def __init__(self, **argv):

        super(InitResponseApduParser, self).__init__()
        self.proposedQualityOfService = argv.get("proposedQualityOfService", "")
        self.proposedDlmsVersion = argv.get("proposedDlmsVersion", "")
        self.proposedConformance = argv.get("proposedConformance", "")
        self.serverMaxReceivePduSize = argv.get("serverMaxReceivePduSize", "")
        self.vaaName = argv.get("vaaName", "")

    def toXml(self):
        """
        生成 XML 格式的 InitiateRequest

        :return:   xml字符串
        """
        root = etree.Element("InitiateResponse")
        if self.proposedQualityOfService != "00":
            etree.SubElement(root, "NegotiatedQualityOfService").set("Value", str(self.proposedQualityOfService))
        if self.proposedDlmsVersion:
            etree.SubElement(root, "NegotiatedDlmsVersionNumber").set("Value", str(self.proposedDlmsVersion))
        if self.proposedConformance:
            conformance = etree.SubElement(root, "NegotiatedConformance")
            for index, item in enumerate(self.proposedConformance):
                if int(item) == 1:
                    etree.SubElement(conformance, "ConformanceBit").set("Name", ConformanceMap[str(index)])
        if self.serverMaxReceivePduSize:
            etree.SubElement(root, "NegotiatedMaxPduSize").set("Value", str(self.serverMaxReceivePduSize))
        if self.vaaName:
            etree.SubElement(root, "VaaName").set("Value", str(self.vaaName))

        return etree.tostring(root, encoding="utf-8", pretty_print=True).decode()

    def parsePdu(self, hexList):
        """
        解析 InitiateResponse

        :param hexList:   解密后的字符串 08 00 06 5F 1F 04 00 60 1A 5D 00 EF 00 07
        :return:   xml字符串
        """
        if hexList.pop() != "08":
            raise Exception("Not InitiateResponse Frame!")

        self.proposedQualityOfService = hexList.pop()
        self.proposedDlmsVersion = hexList.pop()

        # proposed-conformance
        hexList.pop()  # 5F
        hexList.pop()  # 1F
        # length of conformance
        tagLen = hexList.pop()  # 04
        # data type of proposed-conformance
        hexList.pop()
        # content of proposed-conformance
        for i in range(hex_toDec(tagLen) - 1):
            self.proposedConformance += "{:08b}".format(hex_toDec(hexList.pop()))

        # server-max-receive-pdu-size (Unsigned16)
        self.serverMaxReceivePduSize += hexList.pop() + hexList.pop()

        # vaa-name Integer16
        self.vaaName += hexList.pop() + hexList.pop()

        return self.toXml()


class RLRQApduParser(ApduParser):
    """
    <xsd:complexType name="RLRQ-apdu">

        <xsd:sequence>

            <xsd:element name="reason" minOccurs="0" type="Release-request-reason"/>

            <xsd:element name="user-information" minOccurs="0" type="Association-information"/>

        </xsd:sequence>

    </xsd:complexType>
    """

    def __init__(self, **argv):

        super(RLRQApduParser, self).__init__()
        self.reason = argv.get("reason", "")
        self.userInformation = argv.get("userInformation", "")

    def toXml(self):
        """
        生成 XML 格式的 RLRQ

        :return:   xml字符串
        """
        decipherData = ""
        initateRequestXml = ""

        root = etree.Element("RLRQ-apdu")
        if self.reason:
            etree.SubElement(root, "reason").set("Value", str(self.reason))
        if self.userInformation:
            etree.SubElement(root, "user-information").set("Value", str(self.userInformation))
            try:
                # decrypting user-information
                decipherData = self.decipheringApdu(self.userInformation, direction="send")
                initateRequestXml = pdu2Xml(decipherData)
            except:
                # no ciphered information
                decipherData = ""
                initateRequestXml = pdu2Xml(self.userInformation)

        xmlStr = etree.tostring(root, encoding="utf-8", pretty_print=True).decode()
        if len(xmlStr) != 0:
            return xmlStr + "\n" + initateRequestXml, decipherData
        else:
            return initateRequestXml, decipherData

    def parsePdu(self, hexList):
        """
        解析 RLRQ APDU

        :param hexList:  62 28 80 01 00 BE 23 04 21 21 1F 30 00 00 76 C8 91 98 68 7F 6F B6 1C 6B 7A A7 31 4D C3 7B 68 33 C0 A6 E5 22 DE FC D6 BD 7A 03 CB
                         -- 注： 传入进来的list 是反序的
        :return:        xml字符串
        """
        if hexList.pop() != "62":
            raise Exception("Not RLRQ APDU Frame!")
        hexList.pop()  # length of the RLRQ's contents

        while len(hexList) > 0:
            tag = hexList.pop()
            if tag.upper() == "80":  # reason
                tagLen = hexList.pop()  # length of reason
                for i in range(hex_toDec(tagLen)):  # contents of reason
                    self.reason += hexList.pop()

            elif tag.upper() == "BE":  # user-information
                hexList.pop()  # length of user-information
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):  # contents of user-information
                    self.userInformation += hexList.pop()

        return self.toXml()


class RLREApduParser(ApduParser):
    """
    <xsd:complexType name="RLRE-apdu">

        <xsd:sequence>

            <xsd:element name="reason" minOccurs="0" type="Release-response-reason"/>

            <xsd:element name="user-information" minOccurs="0" type="Association-information"/>

        </xsd:sequence>

    </xsd:complexType>
    """

    def __init__(self, **argv):

        super(RLREApduParser, self).__init__()
        self.reason = argv.get("reason", "")
        self.userInformation = argv.get("userInformation", "")

    def toXml(self):
        """
        生成 XML 格式的 AARQ

        :return:
        """
        decipherData = ""
        initiateResponseXml = ""

        root = etree.Element("RLRE-apdu")
        if self.reason:
            etree.SubElement(root, "reason").set("Value", str(self.reason))
        if self.userInformation:
            etree.SubElement(root, "user-information").set("Value", str(self.userInformation))

            try:
                # decrypting user-information
                decipherData = self.decipheringApdu(self.userInformation, direction="recv")
                initiateResponseXml = pdu2Xml(decipherData)
            except:
                # no ciphered information
                decipherData = ""
                initiateResponseXml = pdu2Xml(self.userInformation)

        xmlStr = etree.tostring(root, encoding="utf-8", pretty_print=True).decode()
        if len(xmlStr) != 0:
            return xmlStr + "\n" + initiateResponseXml, decipherData
        else:
            return initiateResponseXml, decipherData

    def parsePdu(self, hexList):
        """
        解析 AARQ APDU

        :param hexList:  63 15 80 01 00 BE 10 04 0E 08 00 06 5F 1F 04 00 00 10 15 04 00 00 07
                         -- 注： 传入进来的list 是反序的
        :return:
        """
        if hexList.pop() != "63":
            raise Exception("Not RLRE APDU Frame!")
        hexList.pop()  # length of the RLRE's contents

        while len(hexList) > 0:
            tag = hexList.pop()
            if tag.upper() == "80":  # reason
                tagLen = hexList.pop()  # length of reason
                for i in range(hex_toDec(tagLen)):  # contents of reason
                    self.reason += hexList.pop()

            elif tag.upper() == "BE":  # user-information
                hexList.pop()  # length of user-information
                hexList.pop()  # data type of tag
                tagLen = hexList.pop()
                for i in range(hex_toDec(tagLen)):  # contents of user-information
                    self.userInformation += hexList.pop()

        return self.toXml()


class DlmsDataApduParser(ApduParser):

    def __init__(self):
        super(DlmsDataApduParser, self).__init__()
        self.userInformation = ""

    @staticmethod
    def lastResponseDataBlock(xmlString):
        """
        判断是否最后一个DLMS分片报文

        :param xmlString:    xml字符串
        :return:
        """
        try:
            root = ET.fromstring(xmlString)
            if root[0].tag == "GetResponsewithDataBlock":
                if root[0][1][2][0].tag == "RawData":
                    Singleton().FragmentRecvDlmsData += root[0][1][2][0].attrib['Value']
                if int(root[0][1][0].attrib['Value']) == 1:  # <LastBlock Value="01" />
                    Singleton().LastRecvDlmsBlock = 1
                else:
                    Singleton().LastRecvDlmsBlock = 0
            else:
                Singleton().LastRecvDlmsBlock = 0
        except:
            pass


    def toXml(self):
        """
        生成 XML 格式的 data

        :return:
        """
        xmlString = pdu2Xml(self.userInformation).strip()
        DlmsDataApduParser.lastResponseDataBlock(xmlString)

        if Singleton().LastRecvDlmsBlock == 0:
            return xmlString, self.userInformation
        else:
            longPduData = Singleton().FragmentRecvDlmsData
            Singleton().FragmentRecvDlmsData = ""
            return pdu2Xml("FF" + longPduData), longPduData


    def parseData(self, hexList, direction):
        """
        解析 data APDU

        :param hexList:  CB 40 30 00 00 13 8D 9B C8 E2 94 97 A9 34 EB C0 E6 3F 22 25 32 9A DE DF D7 9E 89 17 2C DE A2 F1 80 88 F4 AA 19 81 79 35 A8 BD 8C 34 C9 20 6D AA 19 C6 76 89 3C 6B A3 F2 99 51 F3 4F 48 14 BB B4 42 9B
                         -- 注： 传入进来的list 是反序的
        :param direction: 用于标记是发送报文还是接收报文(send: 发送, recv: 接收)
        :return:
        """
        pduTag = hexList[-1]  # APDU Tag

        if pduTag == "62":
            rlrqApduParser = RLRQApduParser(eKey=self.eKey, aKey=self.aKey, systemTitleClient=self.systemTitleClient, systemTitleServer=self.systemTitleServer,
                                            publicKeySigning=self.clientPublicKeySigning)
            return rlrqApduParser.parsePdu(hexList)

        elif pduTag == "63":
            rlreApduParser = RLREApduParser(eKey=self.eKey, aKey=self.aKey, systemTitleClient=self.systemTitleClient, systemTitleServer=self.systemTitleServer,
                                            publicKeySigning=self.serverPublicKeySigning)
            return rlreApduParser.parsePdu(hexList)

        else:
            self.userInformation = "".join(hexList.pop() for _ in range(len(hexList)))
            # 匹配到指定TAG时, 解密报文
            if hex_toDec(pduTag) in [200, 201, 202, 203, 204, 205, 207] + [208, 209, 210, 211, 212, 213, 215] + [219, 220, 221, 223, 224]:  # glo-*-request + ded-*--request + general apdus
                self.userInformation = self.decipheringApdu(self.userInformation, direction)
                return self.toXml()
            # 未匹配指定TAG时, 不解密直接返回XML
            else:
                return self.toXml()

def splitHexWithSpace(hexStr, returnList=False):
    """
    将连续的16进制字符串用空格进行分割
    :param  hexStr:     16进制字符串
    :param  returnList:
    :return:

    >>> splitHexWithSpace('C001C100070100630200FF0300')
    C0 01 C1 00 07 01 00 63 02 00 FF 03 00
    """
    lst = re.findall(r'([0-9a-fA-F]{2})', hexStr.upper())
    if returnList:
        return lst
    return " ".join(lst)

if __name__ == "__main__":

    hex15 = "7E A8 8D 03 02 23 74 B9 0C E6 E7 00 CC 82 01 F5 30 00 00 01 59 D0 FC F0 C2 21 5D E2 E4 5F B5 31 7C D3 5F C4 83 1A 7C 7F 43 9D 65 72 0F 1C 79 2D 07 25 D7 85 E0 27 75 DA 01 BD 99 97 6F 1C 9D 13 84 7F CC 8A 52 F2 1F AB 82 27 A7 3D B3 B7 6D DD 52 51 9E DB E4 CC D2 5A 80 F3 6D CC 24 31 F2 31 7C 6B 4B 07 ED B5 58 CE BC 4D 6B D7 64 9D 0B AD 43 DC 7C 80 C4 A7 B4 A1 C5 83 57 88 BF A6 E1 6E 89 EB 7B CE 1A 03 3E 2E 2E A6 0A 85 F0 FC 7E "
    hex16 = "7E A8 8A 03 02 23 76 77 1F 34 96 7D 7D 13 A5 7C 02 C4 58 50 1E F3 AB 40 10 56 80 87 D1 CE 5B E7 AD AE 79 F4 5F 11 3B 0A EF 81 66 35 BB C4 54 2D 82 1F E1 43 DC F9 A3 65 FF BB F3 37 CC A9 FA F0 4F 29 05 BE E9 B7 61 8D E3 66 51 F1 18 3D 95 72 7B 48 D4 B8 48 CD F7 AF E4 D8 42 A8 29 02 7C A2 FD 25 19 82 5D 1E B8 1A D5 17 D0 05 CC 46 E8 7F 01 33 E1 43 AC 5B 58 9C D6 0A 02 70 D6 87 11 93 DA 9C 9D 1D 79 F8 14 B8 28 DB B1 7E "
    hex17 = "7E A8 8A 03 02 23 78 09 F6 DF 97 88 30 8F F9 CC 6D 2E CE A3 9C 84 8C E6 50 0F 5D 13 B7 57 4A 7C AB 91 0E 18 27 82 15 2D 8E 42 87 D8 0C BB 50 C1 B0 E6 1C 54 D6 BD F5 7B ED 7E 1F 6D CF 00 71 A2 DD 7E 5D D7 53 DA C3 A6 99 0D CB 63 B4 BB B8 D9 A6 05 D1 85 6D 8C 58 17 D0 57 CE 0C 8F 2D F0 E5 D7 71 07 9A 31 CA 06 6C FF EC 24 22 8C 4E BE 83 61 F5 2B 76 CD 7C A9 56 47 6E 6B BE 40 2D 84 37 8C 03 94 88 4A F8 EE 15 70 80 DA 7E "
    hex18 = "7E A0 83 03 02 23 7A 27 A5 E0 CC 23 B6 93 09 2B C3 CB D9 8E 1A 20 54 45 FF 34 CA AE 4B B9 9C 78 66 3F 8A 7C 87 6D AD F2 EF C9 2E 25 AC 1F 1B A2 D9 C1 6D 6E 09 0B 03 B0 A1 2E CA 40 2A DD 7A 4B 97 78 EB 27 69 86 E2 B6 C3 D7 76 B9 9D 88 F9 11 01 8A 37 F1 FF 66 0F 30 1B BC EF 09 9A 97 DA 11 44 E7 2E 09 CD D1 BD 11 A6 0A FD 8D 63 AA 61 98 70 DF FE 68 64 1F 68 C3 8E 52 D0 BA E5 E2 12 A1 73 FA B8 3C 7E "

    Singleton().EKey = "FEE0FEE0FEE0FEE0FEE0FEE0FEE0FEE0"
    Singleton().AKey = "FEA0FEA0FEA0FEA0FEA0FEA0FEA0FEA0"
    Singleton().SystemTitleClient = "0000000000000000"
    Singleton().SystemTitleServer = "4B464D0000000001"

    apduParser = ApduParser()
    for i in [hex15, hex16, hex17, hex18]:
        print("\n".join(apduParser.parsePdu(i)))
        print("-" * 100)
