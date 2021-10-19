# -*- coding: UTF-8 -*-

import os
kaifDlmsDll = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dll\KaifaDlms")

import clr
clr.AddReference(kaifDlmsDll)
from Kaifa.DLMS import *
from Kaifa.DLMS import UsefulFunction, PduXml, ClassDLMS, KeyPairInfo, CommunicationLog, DLMSStateChange, EncryptAlgorithm, Security, EncryptType


# 用于引入 String 类型
from System import String

# clr.AddReference('System.Collections')
# from System.Collections.Generic import List







def encryptDataUseAES(masterKey, plainText):
    """
    基于 Wrap 对数据进行加密 (对应 AESWrapData)

    :param masterKey:           kek密钥
    :param plainText:           待加密的数据
    :return:  加密后的数据
    """
    temp = UsefulFunction.OctetStringToString(plainText)
    plainTextBuf = UsefulFunction.StringToByteArray(temp)

    temp = UsefulFunction.OctetStringToString(masterKey)
    masterKeyBuf = UsefulFunction.StringToByteArray(temp)

    return EncryptAlgorithm().AESWrapData(plainTextBuf, masterKeyBuf, None)



def decryptDataUseAES(masterKey, cipherdText):
    """
    基于 Wrap 对数据进行解密 (对应 AESUnwrapData)

    :param masterKey:           kek密钥
    :param cipherdText:         已加密的数据
    :return:  解密后的数据
    """
    temp = UsefulFunction.OctetStringToString(cipherdText)
    cipherdTextBuf = UsefulFunction.StringToByteArray(temp)

    temp = UsefulFunction.OctetStringToString(masterKey)
    masterKeyBuf = UsefulFunction.StringToByteArray(temp)

    return EncryptAlgorithm().AESUnwrapData(cipherdTextBuf, masterKeyBuf, None)




def encryptDataUseCRC(masterKey, originalKey):
    """
    基于 Crc 对密钥进行加密 (对应 AESEncryptData)

    :param masterKey:    kek密钥
    :param originalKey:  待加密的明文密钥
    :return:    返回一个元组 (True / False, 加密后的数据 / 失败原因)
    """
    sc = Security(masterKey, EncryptType.AES)
    if sc.Init():
        encryptKeyValue = String("")
        result = sc.EncryptWithAES(originalKey, encryptKeyValue)
        if result[0]:
            return result
    return ""



def gcmAlgorithm(ekey, akey, sc, ic, sysTitle, data, aad="", isEncryption=True):
    """
    GCM 数据加/解密 (参考GreenBook: Figure 81)

    :param ekey:                接收16进制字符串, 不带前缀'0x'
    :param akey:
    :param sc:
    :param ic:
    :param sysTitle:
    :param data:
    :param aad:                 General-ciphering 模式下需要额外信息 (参考GreenBook: Table 38 )
    :param isEncryption:
    :return:
    """
    # ekeyByte 由 ekey 生成
    ekeyByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(ekey.replace(" ", "")))

    # ivByte 由 sysTitle + ic 生成
    ivByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString((sysTitle + ic).replace(" ", "")))

    # 根据 sc 取值不同, aadByte 的组成随之变化 (Green Book: Table 38)
    aadByte = ""
    if str(sc) == '10':     # Authentication only
        aadByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString((sc + akey + aad + data).replace(" ", "")))
    if str(sc) == '20':     # Encryption only
        aadByte = ""
    if str(sc) == '30':     # Authentication and Ecryption
        aadByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString((sc + akey + aad).replace(" ", "")))

    # bufByte 由 user-information 生成
    bufByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(data.replace(" ", "")))
    try:
        if isEncryption:
            return EncryptAlgorithm().GCMDecryptData(bufByte, ekeyByte, ivByte, aadByte, "")
        else:
            return EncryptAlgorithm().GCMEncryptData(bufByte, ekeyByte, ivByte, aadByte, "")
    except:
        return ""






def decryptGcmData(pdu, ekey, akey=""):
    """
    通过 GCM 解密数据

    :param pdu:     加密后的16 进制报文数据(以 'DB' 开头)
    :param ekey:    加密密钥
    :param akey:    解密密钥
    :return:
    """
    hexLst = pdu.upper().split(" ")
    hexLst.reverse()

    # Tag
    tag = hexLst.pop()
    if tag != 'DB':
        return ""

    # sys-T
    systemTitleLen = hexLst.pop()
    systemTitle = ""
    for i in range(int(systemTitleLen, 16)):
        systemTitle += hexLst.pop()

    # length of data
    lensTag = hexLst.pop()
    if lensTag == '83':
        lens = int(hexLst.pop() + hexLst.pop() + hexLst.pop(), 16)
    elif lensTag == '82':
        lens = int(hexLst.pop() + hexLst.pop(), 16)
    elif lensTag == '81':
        lens = int(hexLst.pop(), 16)
    else:
        lens = int(lensTag, 16)

    # security control
    sc = hexLst.pop()

    # invocation counter
    ic = ""
    for i in range(4):
        ic += hexLst.pop()

    # user-info
    # buf = ""
    # for i in range(lens - 5):
    #     buf += hexLst.pop()
    buf = ""
    for i in range(len(hexLst)):
        buf += hexLst.pop()

    bufByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(buf))
    keyByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(ekey))

    # iv = Sys-T || IC
    ivByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(systemTitle + ic))

    # aad -- Additional Authenticated Data
    # -- Authentication only:  SC || AK || (C) Information
    # -- Encryption only:  Null
    # -- Authenticated encryption:  SC || AK
    aadByte = ""
    if str(sc) == '10':     # Authentication only
        aadByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(sc + akey + buf))
    if str(sc) == '20':     # Encryption only
        aadByte = ""
    if str(sc) == '30':
        aadByte = UsefulFunction.StringToByteArray(UsefulFunction.OctetStringToString(sc + akey))

    try:
        pduData = EncryptAlgorithm().GCMDecryptData(bufByte, keyByte, ivByte, aadByte, "")[0]
        xmlData = PduXml.PhasePdu2xml('FF' + pduData[36:])
        return pduData, xmlData
    except:
        return ""



def getRandomString(length):
    """
    生成指定长度的16进制字符串

    :param length:  字符串长度 (注意: 一个单位长度对应两个16进制字符)
    :return:
    """
    return UsefulFunction.StringToOctetString(UsefulFunction.GetRandomString(length, True, True, True, True, ""))



def decipheringApdu(**args):
    """
    数据解密

    :param args:
    :return:
    """
    eKey = args.get('eKey', '')
    aKey = args.get('aKey', '')
    sysTitleClient = args.get('sysTitleClient', '')
    sysTitleServer = args.get('sysTitleServer', '')
    pubKeySigning = args.get('pubKeySigning', '')
    apdu = args.get('apdu', '')

    decryptedPdu = UsefulFunction.ByteArrayToOctetString(ClassDLMS().DecipheringApdu(eKey, aKey, sysTitleClient, sysTitleServer, pubKeySigning, apdu))
    xmlString = PduXml.PhasePdu2xml(decryptedPdu)

    return decryptedPdu, xmlString



def pdu2Xml(pduData):
    """
    将PDU数据转换成XML格式
    :param pduData:
    :return:
    """
    return PduXml.PhasePdu2xml(pduData)


def xml2Pdu(xmlData):
    """
    将XML数据转换成PDU格式
    :param xmlData:
    :return:
    """
    return PduXml.PhaseXml2Pdu(xmlData)



def pduToXml(pduData):
    """
    将PDU数据转换成XML格式
    :param pduData:
    :return:
    """
    from .XmlPduSwitch import XmlPdu
    return XmlPdu(XmlPduString=pduData).toXml()


def xmlToPdu(xmlData):
    """
    将XML数据转换成PDU格式
    :param xmlData:
    :return:
    """

    from .XmlPduSwitch import XmlPdu
    return XmlPdu(XmlPduString=xmlData).toXml()





if __name__ == '__main__':

    originalKey = "00000000000000000000000000000000"
    masterKey = "00112233445566778899AABBCCDDEEFF"

    print(encryptDataUseAES(masterKey, originalKey))
    print(encryptDataUseCRC(masterKey, originalKey))
