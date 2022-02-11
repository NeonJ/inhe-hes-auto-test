# -*- coding: UTF-8 -*-

from .UsefulAPI import *


def getLSB(dec):
    """
    返回10进制数的最低bit

    :param dec:  10进制数
    :return: 1 or 0
    """
    return int(dec) & 1


def calcHDLCAddr(hx):
    """
    将16 进制的 HDLC 地址转换成对应的 10 进制地址

    :param hx:
    :return:               10进制数
    """
    return int(hx, 16) >> 1


def getHdlcAddr(hexList):
    """
    从16进制字符串报文中获取 HDLC 目的/源地址

    :param hexList:  16进制字符串列表
    :return:         HDLC 目的/源地址
    """
    address = ""
    while True:
        addr = hexList.pop()
        address += " " + addr
        if getLSB(hex_toDec(addr)) == 1:
            break
    return [calcHDLCAddr(addr) for addr in address.strip().split(" ")]


def parseHdlcFrame(hexList):
    """
    解析HDLC 帧的用户数据部分的字段
    :param hexList: 只包含用户数据部分的16进制字符串
    :return:
    """

    hexList.pop()  # format identifer
    hexList.pop()  # group identifer
    hexList.pop()  # group length

    transmitLen = ""
    receiveLen = ""
    transmitWindow = ""
    receiveWindow = ""

    while True:
        params = hexList.pop()
        if params == "05":
            paramsLen = hex_toDec(hexList.pop())
            for i in range(paramsLen):
                transmitLen += hexList.pop()

        elif params == "06":
            paramsLen = hex_toDec(hexList.pop())
            for i in range(paramsLen):
                receiveLen += hexList.pop()

        elif params == "07":
            paramsLen = hex_toDec(hexList.pop())
            for i in range(paramsLen):
                transmitWindow += hexList.pop()

        elif params == "08":
            paramsLen = hex_toDec(hexList.pop())
            for i in range(paramsLen):
                receiveWindow += hexList.pop()

        else:
            hexList.append(params)
            break

    return hex_toDec(transmitLen), hex_toDec(receiveLen), hex_toDec(transmitWindow), hex_toDec(receiveWindow)


def parseControlField(hexStr, clientSend=True):
    """
    解析 HDLC 中的控制字

    :param hexStr:      16 进制字符串
    :param clientSend:  True (客户端发送请求), False (客户端接收响应)
    :return:            控制字
    """

    binStr = "{:08b}".format(int(hex_toDec(str(hexStr))))
    PF = '0'
    if int(binStr[3]) == 1:
        PF = 'P' if clientSend else 'F'

    if int(binStr[-1]) == 0:  # Information Frame
        RRR = int("".join(binStr[:3]), 2)
        SSS = int("".join(binStr[4:7]), 2)
        return f'"I" Frame N(R)={RRR}, N(S)={SSS}, P/F={PF}'

    elif int(binStr[-2]) == 0:  # Supervisory Frame
        RRR = int("".join(binStr[:3]), 2)
        if int(binStr[5]) == 0:
            return f'"RR" Frame N(R)={RRR}, P/F={PF}'
        elif int(binStr[5]) == 1:
            return f'"RNR" Frame N(R)={RRR}, P/F={PF}'
        else:
            return f'"S" Frame N(R)={RRR}, P/F={PF}'

    else:
        if binStr == '10010011':  # SNRM Frame (Need response, P=1)
            return f'"SNRM" Frame, P/F=P'
        if binStr == '01010011':  # DISC Frame (Need response, P=1)
            return f'"DISC" Frame, P/F=P'
        if binStr == '01110011':  # UA Frame (Nedd response, F=1)
            return f'"UA" Frame, P/F=F'
        if binStr == '00001111':  # DM Frame (Not need response, F=0)
            return f'"DM" Frame, P/F=0'


def assembleHdlcFrame(**argv):
    """
    组装 HDLC 报文

    :param argv:          传入一个字典
    :return:              HDLC 报文
    """
    clientRequest = argv.get("clientRequest", True)
    segment = argv.get("segment", False)
    clientAddr = argv['clientAddr']
    serverUpperAddr = argv['serverUpperAddr']
    serverLowerAddr = argv['serverLowerAddr']
    control = argv['control']
    userInfo = argv.get('userInfo', "")

    hexList = list()
    if segment:
        hexList.append('A8')
    else:
        hexList.append('A0')

    clientAddrHex = hex((int(clientAddr) << 1) + 1)[2:].rjust(2, '0')
    serverUpperAddrHex = hex(int(serverUpperAddr) << 1)[2:].rjust(2, '0')
    serverLowerAddrHex = hex((int(serverLowerAddr) << 1) + 1)[2:].rjust(2, '0')

    if clientRequest:
        hexList.append(clientAddrHex)
        hexList.append(serverUpperAddrHex)
        hexList.append(serverLowerAddrHex)
    else:
        hexList.append(serverUpperAddrHex)
        hexList.append(serverLowerAddrHex)
        hexList.append(clientAddrHex)

    hexList.append(str(control))

    userInfo = str(userInfo).replace(" ", "")
    infoLen = len(userInfo)
    if infoLen == 0:
        hdlcLen = hex(len(hexList) + 1 + 2)[2:].rjust(2, '0')
        hexList.insert(1, hdlcLen)
        hcs = crc16("".join(hexList))
        hexList.append(hcs)

    else:
        hdlcLen = hex(len(hexList) + infoLen // 2 + 1 + 2 + 2)[2:].rjust(2, '0')
        hexList.insert(1, hdlcLen)
        hcs = crc16("".join(hexList))
        hexList.append(hcs)
        hexList.append(userInfo)
        fcs = crc16("".join(hexList))
        hexList.append(fcs)

    return "7E" + "".join(hexList).upper() + "7E"
