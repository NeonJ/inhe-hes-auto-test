# -*- coding: UTF-8 -*-

import binascii
import re
import socket
import xml.etree.ElementTree as ET

import serial
from common.DataFormatAPI import hex_toDateTimeString
from libs.DllLoader import *
from libs.Singleton import Singleton

from common.Decorate import *
from common.KFLog import *


class P1Push(object):

    def __init__(self, **argv):
        """
        :param comPort:             串口号
        :param baudrate:            波特率
        :param ekey:                EKey
       :param skipFirstEntry:       是否去除读取的第一条数据, 可选值为: True, False
        """
        self.comPort = argv['comPort']
        self.baudrate = argv.get('baudrate', 2400)
        self.ekey = argv.get('ekey', '101112131415161718191A1B1C1D1E1F')
        self.skipFirstEntry = argv.get('skipFirstEntry', True)

    def __readFromConsole(self):
        """
        通过串口读取P1 Push 数据 (建议去除读取的第一条数据, 可以避免被缓存中的数据污染)
        :return:
        """
        self.comPort = "COM" + str(self.comPort).lower().replace("com", "")
        self.baudrate = int(self.baudrate)

        def splitHexDataWithSpace(hexData):
            ret = re.findall(r'[0-9a-zA-Z]{2}', hexData)
            return " ".join(ret)

        def readConsole(conn):
            pktList = list()
            for index in range(100):
                responses = ""
                for loop in range(300):
                    responses += conn.read().hex()
                    try:
                        # 定位MBus头位置
                        m = re.search(r"68\s?(\w{2})\s?\1\s?68", responses)
                        # 将非 '68 L L 68' 开头的数据剔除
                        responses = responses[m.start():]
                        # 提取报文长度
                        pktLen = int(m.group(1), 16)
                        if len(responses) / 2 == pktLen + 6:
                            break
                    except:
                        pass

                pktList.append(responses)
                # CI[tl] = 0x1[0-F] 时，即认为报文已收完
                if responses[12] == '1':
                    break

                # 为了预防读取数据失败, 轮询5次之后进行一次检查
                if index == 5 and len(pktList) == 0:
                    break

            return splitHexDataWithSpace("".join(pktList)).upper()

        ser = None
        try:
            ser = serial.Serial(self.comPort, baudrate=self.baudrate, bytesize=8, parity='N', stopbits=1, timeout=5)
            if self.skipFirstEntry:
                readConsole(ser)
            return readConsole(ser).strip()
        except Exception as ex:
            error(ex)
        finally:
            if ser is not None:
                ser.close()

    @staticmethod
    def __parseP1PushXml(xmlData):

        def arrayData(node):
            data = dict()
            for index, child in enumerate(node):
                if child.tag in ['DoubleLongUnsigned', 'LongUnsigned', 'Unsigned', 'Integer', 'Enum']:
                    data[index] = child.attrib['Value']
                if child.tag == "OctetString":
                    data[index] = child.attrib['Value']
                if child.tag == "Structure":
                    data[index] = structData(child)
                if child.tag == "Array":
                    data[index] = arrayData(child)
            return data

        def structData(node):
            data = dict()
            for index, child in enumerate(node):
                if child.tag in ['DoubleLongUnsigned', 'LongUnsigned', 'Unsigned', 'Integer', 'Enum']:
                    data[index] = child.attrib['Value']
                if child.tag == "OctetString":
                    data[index] = child.attrib['Value']
                if child.tag == "Structure":
                    data[index] = structData(child)
                if child.tag == "Array":
                    data[index] = arrayData(child)
            return data

        root = ET.fromstring(xmlData)
        return arrayData(root)

    @formatResponse
    def getPushData(self):
        # 从串口上读取数据
        hexData = self.__readFromConsole()
        if len(hexData) == 0:
            return ""

        mbusPkts = list()
        # 将报文切断
        indexs = [m.span()[0] for m in re.finditer(r"68\s?(\w{2})\s?\1\s?68", hexData)]
        for i in range(len(indexs) - 1):
            mbusPkts.append(hexData[indexs[i]: indexs[i + 1]])
        mbusPkts.append(hexData[indexs[len(indexs) - 1]:])

        pkts = ""
        for pkt in mbusPkts:
            hexLst = pkt.strip().split(" ")

            # 去头
            for i in range(9):
                hexLst.pop(0)
            # 去尾
            hexLst.pop()
            hexLst.pop()

            # GBT
            if hexLst[0].upper() == 'E0':
                for i in range(6):
                    hexLst.pop(0)
                # length
                if hexLst[0] == "83":
                    hexLst.pop(0) + hexLst.pop(0) + hexLst.pop(0) + hexLst.pop(0)
                elif hexLst[0] == "82":
                    hexLst.pop(0) + hexLst.pop(0) + hexLst.pop(0)
                elif hexLst[0] == "81":
                    hexLst.pop(0) + hexLst.pop(0)
                else:
                    hexLst.pop(0)
            pkts += " ".join(hexLst)

        info(f"P1 Push Data: {pkts}")
        result = decryptGcmData(pkts, self.ekey)
        if isinstance(result, tuple):
            pushData = P1Push.__parseP1PushXml(result[1])[0]
            import json
            info(f"P1 Push XML: {json.dumps(pushData, indent=4, check_circular=True)}")
            return pushData
        else:
            return result


class GPRSPush(object):

    def __init__(self, **argv):
        self.port = argv['port']
        self.eKey = argv.get('eKey', '')
        self.aKey = argv.get('aKey', '')
        self.keySign = argv.get('keySign', '')
        self.timeout = argv.get('timeout', 120)

    @staticmethod
    def parseGPRSPushXml(xmlData):

        def arrayData(node):
            data = dict()
            for index, child in enumerate(node):
                if child.tag == "Array":
                    data[index] = arrayData(child)
                elif child.tag == "Structure":
                    data[index] = structData(child)
                elif child.tag == "OctetString":
                    data[index] = child.attrib['Value']
                    # 字符串长度为24时, 推断为时间
                    if len(data[index].strip()) == 24:
                        data[index] = hex_toDateTimeString(data[index])
                else:
                    data[index] = child.attrib['Value']

            return data

        def structData(node):
            data = dict()
            for index, child in enumerate(node):
                if child.tag == "Array":
                    data[index] = arrayData(child)
                elif child.tag == "Structure":
                    data[index] = structData(child)
                elif child.tag == "OctetString":
                    data[index] = child.attrib['Value']
                    # 字符串长度为24时, 推断为时间
                    if len(data[index].strip()) == 24:
                        data[index] = hex_toDateTimeString(data[index])
                else:
                    data[index] = child.attrib['Value']
            return data

        root = ET.fromstring(xmlData)
        # if root.tag in ['EventNotificationRequest']:
        #     return arrayData(root[1])
        return arrayData(root)

    @staticmethod
    def parseEventNotificationRequest(xmlData):

        # header 存储请求头信息(Time、ClassId、InstanceId、AttributeId)
        # {'time': '07E40B0A0216141FFF800000', 'classId': '0028', 'attributeId': '0028', 'instanceId': '0004190900FF'}
        header = dict()

        # response 存储响应内容
        # {0: {0: '4B464D32303230383139303230303036', 1: '0004190900FF', 2: '01000000'}}
        response = None

        root = ET.fromstring(xmlData)
        for i in range(len(root)):
            if root[i].tag == 'Time':
                header['time'] = root[i].attrib['Value']
            if root[i].tag == 'AttributeDescriptor':
                for j in range(len(root[i])):
                    if root[i][j].tag == 'ClassId':
                        header['classId'] = root[i][j].attrib['Value']
                    if root[i][j].tag == 'InstanceId':
                        header['instanceId'] = root[i][j].attrib['Value']
                    if root[i][j].tag == 'AttributeId':
                        header['attributeId'] = root[i][j].attrib['Value']
            if root[i].tag == 'AttributeValue':
                value = ET.tostring(root[i]).decode('utf-8')
                response = GPRSPush.parseGPRSPushXml(value)

        return header, response

    def receivePush(self):
        def getIPv4ByPrefix(prefix='10.'):
            for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
                if ip.startswith(prefix):
                    return ip

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(int(self.timeout))
                # s.bind(('0.0.0.0', int(self.port)))
                s.bind((getIPv4ByPrefix(), int(self.port)))
                s.listen(0)
                conn, addr = s.accept()
                response = list()
                with conn:
                    while True:
                        data = conn.recv(4096)
                        if len(data) == 0:
                            break
                        response.append(binascii.b2a_hex(data).decode("ascii").upper())
                return response
        except socket.timeout:
            return ""

    def analysisForDeer(self):
        """
        适用于Deer GPRS Push 的数据
        00 01 00 01 00 10 00 3C DB 09 08 4B 46 4D 19 12 00 00 07 30 30 00 01 11 65 0B 4F E4 A3 36 EB AE 32 E9 DF 6F AB 58 AC CE B1 AA BE 7F F8 27 3D 13 A3 BA 69 85 28 E4 B1 56 22 35 BD 84 81 6C B7 8D 4F C5 05 94
        00 01 00 01 00 10 00 4A DB 09 08 4B 46 4D 19 12 00 00 07 3E 30 00 01 11 6A 6E 11 64 0B DF 76 C3 0E 0F 59 0C 44 92 F4 31 4E D9 3A 1A C2 CE A8 81 53 F3 7C 34 65 95 FD 9D 2B 48 05 0A 27 4B 74 4A 83 94 97 B0 C5 40 46 EB A0 BF 4A 34 4A 61 DD 28 5D 90
        """
        response = self.receivePush()
        if len(response) > 0:
            sysT = response[0][22:38]
            apdu = 'C0' + response[0][38:]

            decryptedPdu, xmlString = decipheringApdu(eKey=self.eKey, sysTitleServer=sysT, apdu=apdu)
            info(f"** GPRS Push PDU: {decryptedPdu}")
            info(f"** GPRS Push Xml: \n{xmlString}")
            return GPRSPush.parseGPRSPushXml(xmlString)

        info(f"** GPRS Push PDU: 'Not receive data!' **")
        return ''

    def analysisForNormal16(self):
        """
        适用于Normal16 GPRS Push 的数据 (支持GBT)
        00 01 00 01 00 01 00 48 DB 08 4B 46 4D 67 75 1B 2B 70 3D 31 00 00 00 97 B6 DE CE F5 52 D7 F3 7A 1F 28 31 5D 25 25 54 59 3D 5E 6C 2B 00 86 BA 33 E1 E4 05 16 D8 CA 01 36 06 83 88 83 3F 29 5D EA 24 22 58 EE F2 41 42 3D 40 F9 90 70 44 3C DB 62
        00 01 00 01 00 01 00 F9 DB 08 4B 46 4D 67 75 1B 2B 70 81 ED 31 00 00 00 96 59 03 1D 4D 87 14 48 99 2C 57 C0 47 60 A6 1C 16 01 35 D6 E9 6A 39 A3 BE B8 05 F6 0F 2B 05 D5 6F 60 48 27 46 18 A8 74 2D 2A AA 77 23 69 D4 30 EA 88 64 B3 C3 F6 E2 63 50 F1 80 F9 3A 53 B8 90 8E F5 CC 3D 43 61 EA 30 DD D6 6F 99 70 69 91 44 07 67 5B 5E 5C 3C 03 DD F2 60 7E 18 65 9A 9B F0 56 65 4F 8C 94 A3 3F 7F 85 D9 F0 1A 15 79 E8 48 7A D4 D9 95 D1 C0 7B B6 82 04 BC D4 82 FD 14 C0 A4 69 E5 04 A6 1E 57 37 63 F1 9E 30 FD 31 73 B5 D8 7F FE B5 61 5B 17 41 3D E7 DE 59 37 97 33 06 2F 9E DB 90 F5 68 95 7E 8F D0 C3 96 45 55 24 0C 07 A3 28 CF 98 BE CF F9 11 9E A0 13 19 C6 FA 54 31 AC 0F FC 61 93 E1 20 E5 9F 93 6F A3 77 C1 A9 BC 63 9E E8 A3 15 69 EF 78 3F 0F B3 7D CE 6F 9A 9C D7 6D 5E 0C 7B FE 37 3A
        """
        response = self.receivePush()
        apdu = ""
        for item in response:
            # 去除WPDU头
            tmp = item[16:]
            # GBT报文
            if tmp[:2].upper() == 'E0':
                # 去除GBT头
                tmp = tmp[12:]
                # 去除报文长度字段
                if tmp[:2] == '83':
                    apdu += tmp[8:]
                elif tmp[:2] == '82':
                    apdu += tmp[6:]
                elif tmp[:2] == '81':
                    apdu += tmp[4:]
                else:
                    apdu += tmp[2:]
            else:
                # 非GBT报文, 直接拼接数据
                apdu += tmp

        if len(apdu) > 0:
            info(f"** GPRS Push Data: {apdu.upper()}")
            # 提取 sysTitleServer
            sysT = apdu[4:20]

            decryptedPdu, xmlString = decipheringApdu(eKey=self.eKey, sysTitleServer=sysT, apdu=apdu)
            # DataNotification 数据格式需求去除头部再加上'FF'才能转换成XML
            if decryptedPdu.startswith('0F'):
                error('FF' + decryptedPdu[40:])
                xmlString = pdu2Xml('FF' + decryptedPdu[36:])

                info(f"** GPRS Push PDU: {decryptedPdu}")
                info(f"** GPRS Push Xml: \n{xmlString}")
                return GPRSPush.parseGPRSPushXml(xmlString)

        info(f"** GPRS Push PDU: 'Not receive data!' **")
        return ''

    # def analysisForCamel(self):
    #     """
    #     适用于Camel GPRS Push 的数据
    #     00 01 00 01 00 01 00 F9 DB 08 4B 46 4D 67 75 1B 2B 70 81 ED 31 00 00 00 96 59 03 1D 4D 87 14 48 99 2C 57 C0 47 60 A6 1C 16 01 35 D6 E9 6A 39 A3 BE B8 05 F6 0F 2B 05 D5 6F 60 48 27 46 18 A8 74 2D 2A AA 77 23 69 D4 30 EA 88 64 B3 C3 F6 E2 63 50 F1 80 F9 3A 53 B8 90 8E F5 CC 3D 43 61 EA 30 DD D6 6F 99 70 69 91 44 07 67 5B 5E 5C 3C 03 DD F2 60 7E 18 65 9A 9B F0 56 65 4F 8C 94 A3 3F 7F 85 D9 F0 1A 15 79 E8 48 7A D4 D9 95 D1 C0 7B B6 82 04 BC D4 82 FD 14 C0 A4 69 E5 04 A6 1E 57 37 63 F1 9E 30 FD 31 73 B5 D8 7F FE B5 61 5B 17 41 3D E7 DE 59 37 97 33 06 2F 9E DB 90 F5 68 95 7E 8F D0 C3 96 45 55 24 0C 07 A3 28 CF 98 BE CF F9 11 9E A0 13 19 C6 FA 54 31 AC 0F FC 61 93 E1 20 E5 9F 93 6F A3 77 C1 A9 BC 63 9E E8 A3 15 69 EF 78 3F 0F B3 7D CE 6F 9A 9C D7 6D 5E 0C 7B FE 37 3A
    #     00 01 00 01 00 04 00 41 DB 08 4B 46 4D 00 01 22 AE 44 36 30 00 00 00 26 78 F8 7B 53 04 EB C2 90 ED 2B 19 F0 AF 92 8B 6D 2B 15 B5 F0 F6 36 62 91 4C 60 C3 07 35 D7 B5 DB C4 A0 E1 1B E9 E6 30 8D 68 A2 66 DF 1F D0 98 47 B7
    #     """
    #     response = self.receivePush()
    #     apdu = ""
    #     for item in response:
    #         # 去除WPDU头
    #         tmp = item[16:]
    #         # GBT报文
    #         if tmp[:2].upper() == 'E0':
    #             # 去除GBT头
    #             tmp = tmp[12:]
    #             # 去除报文长度字段
    #             if tmp[:2] == '83':
    #                 apdu += tmp[8:]
    #             elif tmp[:2] == '82':
    #                 apdu += tmp[6:]
    #             elif tmp[:2] == '81':
    #                 apdu += tmp[4:]
    #             else:
    #                 apdu += tmp[2:]
    #         else:
    #             # 非GBT报文, 直接拼接数据
    #             apdu += tmp
    #
    #     if len(apdu) > 0:
    #         info(f"** GPRS Push Data: {apdu.upper()}")
    #         # 提取 sysTitleServer
    #         sysT = apdu[4:20]
    #
    #         decryptedPdu, xmlString = decipheringApdu(eKey=self.eKey, sysTitleServer=sysT, apdu=apdu)
    #         # DataNotification 数据格式需求去除头部再加上'FF'才能转换成XML
    #         if decryptedPdu.startswith('0F'):
    #
    #             # 注意: Camel DataNotification的数据格式中省略了`datetime`, 用`00`填充
    #             error('FF' + decryptedPdu[12:])
    #             xmlString = pdu2Xml('FF' + decryptedPdu[12:])
    #
    #             info(f"** GPRS Push PDU: {decryptedPdu}")
    #             info(f"** GPRS Push Xml: \n{xmlString}")
    #             return GPRSPush.__parseGPRSPushXml(xmlString)
    #
    #     info(f"** GPRS Push PDU: 'Not receive data!' **")
    #     return ''

    def analysisForCamel(self):
        """
        适用于Camel GPRS Push 的数据
        00 01 00 01 00 04 00 41 DB 08 4B 46 4D 00 01 22 AE 44 36 30 00 00 00 26 78 F8 7B 53 04 EB C2 90 ED 2B 19 F0 AF 92 8B 6D 2B 15 B5 F0 F6 36 62 91 4C 60 C3 07 35 D7 B5 DB C4 A0 E1 1B E9 E6 30 8D 68 A2 66 DF 1F D0 98 47 B7
        """
        response = self.receivePush()
        apdu = ""
        for item in response:
            # 去除WPDU头
            tmp = item.replace(' ', '')[16:]
            # GBT报文
            if tmp[:2].upper() == 'E0':
                # 去除GBT头
                tmp = tmp[12:]
                # 去除报文长度字段
                if tmp[:2] == '83':
                    apdu += tmp[8:]
                elif tmp[:2] == '82':
                    apdu += tmp[6:]
                elif tmp[:2] == '81':
                    apdu += tmp[4:]
                else:
                    apdu += tmp[2:]
            else:
                # 非GBT报文, 直接拼接数据
                apdu += tmp

        # C2 -> EventNotificationRequest
        if apdu.startswith('C2'):
            xmlString = pduToXml(apdu)
            info(f"** GPRS Push PDU: {apdu}")
            info(f"** GPRS Push Xml: \n{xmlString}")
            return GPRSPush.parseEventNotificationRequest(xmlString)

        info(f"** GPRS Push PDU: 'Not receive data!' **")
        return ''

    @formatResponse
    def getPushData(self):
        if Singleton().Project.lower() == 'deer':
            return self.analysisForDeer()
        elif Singleton().Project.lower() == 'normal16':
            return self.analysisForNormal16()
        elif Singleton().Project.lower() == 'camel':
            return self.analysisForCamel()
        else:
            return ''
