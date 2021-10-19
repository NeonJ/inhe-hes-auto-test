# -*- coding:utf-8 -*-

import logging
from .ApduParser import *
from libs.Singleton import Singleton


class DlmsLogger(object):
    def __init__(self):
        self._dlmsLogger = None

    def dlmsLog(self, casename):
        if self._dlmsLogger:
            return self._dlmsLogger

        timestamp = time.strftime('(%H%M%S)',time.localtime(time.time()))
        fh = logging.FileHandler(os.path.join("logs", kfLog.datetime, casename + "_" + timestamp + ".log"))
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(message)s'))

        self._dlmsLogger = logging.getLogger('dlmsLog')
        self._dlmsLogger.addHandler(fh)
        self._dlmsLogger.setLevel(logging.INFO)
        return self._dlmsLogger


class CommunicationDelegate(object):
    TestCase = ''
    DlmsInfo = None

    @staticmethod
    def showCommunicationInfo(pdu):
        # warn(pdu)

        # 如果用例名发生改变, 则新创建一个文件用于记录日志
        if CommunicationDelegate.TestCase != Singleton().TestCase:
            CommunicationDelegate.TestCase = Singleton().TestCase
            CommunicationDelegate.DlmsInfo = DlmsLogger().dlmsLog(CommunicationDelegate.TestCase).info

        # 记录原始报文
        CommunicationDelegate.DlmsInfo(pdu.replace('\r\n', ""))

        # 解析pdu
        try:
            parsedData = ApduParser().parsePdu(pdu)

            # 解析后的报文内容为空 (非法报文/不识别的报文)
            if parsedData is None:
                CommunicationDelegate.DlmsInfo("-" * 100 + "\n\n")

            else:
                # 解密后的DLMS层数据
                parsedPdu = parsedData.pop()
                parsedPdu = parsedPdu.replace("\r", "")

                if len(str(parsedPdu).strip()) > 0:
                    # CommunicationDelegate.DlmsInfo("DLMS Layer: " + str(parsedPdu) + "\n")
                    CommunicationDelegate.DlmsInfo("Dciphering  DLMS PDU: " + splitHexWithSpace(str(parsedPdu)) + "\n")

                if parsedData is not None:
                    CommunicationDelegate.DlmsInfo("\n".join(parsedData).replace("\r", ""))
                    CommunicationDelegate.DlmsInfo("-" * 100 + "\n\n")

        except Exception as e:
            CommunicationDelegate.DlmsInfo(f"Parse PDU failed!\n{e}\n\n")



# class DLMSStateChangeDelegate(object):
#     @staticmethod
#     def showStateChangeInfo(msg):
#         print(msg)
#         info(msg)
