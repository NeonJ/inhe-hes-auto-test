# -*- coding:utf-8 -*-

import re
import os
import time
import datetime

import socket
from binascii import hexlify, unhexlify
from convertdate import persian
from libs.Singleton import Singleton


class KFResult(object):
    """
    定义返回结果的数据格式
    """
    def __init__(self, status, result):
        self.status = status
        self.result = result

    def __str__(self):
        return f'status: {self.status}, result: {self.result}'


def getLastDayofMonth(dateStr):
    """
    根据当前时间获取一个月中的最后一天

    :param dateStr:         日期字符串
    :return: string         返回当月最后一天的日期
    """
    if Singleton().Project == "diamond":
        year, month, day = dateStr[:10].split("-")
        if int(month) == 12:
            if persian.leap(int(year)):
                day = 30
            else:
                day = 29
        elif int(month) in range(1, 7):
            day = 31
        else:
            day = 30

        return f"{year}-{month}-{day}"
    else:
        year, month, day = dateStr[:10].split("-")
        current_date = datetime.date(int(year), int(month), int(day))
        next_month = current_date.replace(day=28) + datetime.timedelta(days=4)
        return str(next_month - datetime.timedelta(days=next_month.day))


def string_toTimestamp(st):
    """
    把时间字符串转换成时间戳

    :param st:         字符串("2019-01-01 11:26:39")
    :return:           floating point number

    >>> string_toTimestamp("2019-01-01 11:26:39")
    1546313199.0
    """
    if Singleton().Project == "diamond":
        st = persianToGregorian(st)
    return time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S"))


def timeDiff(responseTime, expectTime, errorRange=0):
    """
    检查两个时间字符串是否相等，可以设置误差范围errorRange（即在误差范围内也算相等）

    :param responseTime: 待校验的时间
    :param expectTime:   期望的时间
    :param errorRange:   允许的误差范围(单位: 秒, 默认为0)
    :return:  返回一个元组 (True/False, Information)

    >>> timeDiff("2019-01-01 00:00:00", "2019-01-01 00:00:00").status
    True
    >>> timeDiff("2019-01-01 00:00:03", "2019-01-01 00:00:00", 5).status
    True
    """
    # 如果responseTime是16进制字符串，则先进行转换
    if re.match(r'[0-9a-fA-F]{6,}', responseTime):
        responseTime = hex_toDateString(responseTime)
    try:
        if Singleton().Project != "diamond":
            datetime.datetime.strptime(responseTime, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return KFResult(False, f"'{responseTime}' is not valid datetime")

    if abs(int(string_toTimestamp(responseTime)) - int(string_toTimestamp(expectTime))) <= int(errorRange):
        return KFResult(True, "")
    else:
        return KFResult(False, f"The time difference between responseTime='{responseTime}' and expectTime='{expectTime}' is greater than errorRange='{errorRange}s'")


def getTimeSuffix():
    """
    获取不同项目DateTime后三位（deviation, clock status）

    :return:
    """
    if Singleton().Project.lower() in ["camel", "beryl06", "diamond", "dolphin", 'cusk']:
        return "FF800000"
    else:
        return "008000FF"


def dateTime_toHex(dateTime):
    """
    将dateTime字符串格式时间转换成16进制字符串

    :param dateTime:          日期时间字符串
    :return:                  十六进制字符串

    >>> dateTime_toHex("2019-05-01 14:30:30 00,8000,00")
    '07E30501030E1E1E00800000'
    """
    hexStr = ""
    dt = None

    # 处理通配符
    # Wildcard Time String： FFFF-01-32-FF-00-30-00-00-FFFF-FF
    dateTime = dateTime.strip()
    lst = re.split("[\,,\-,\:,\ ]", dateTime)
    if len(lst) == 10:
        for i in range(0, len(lst)):
            if i <= 6:
                if re.search("[A-F]", lst[i]):
                    hexStr += lst[i]
                else:
                    if i == 0:
                        hexStr += "{:04x}".format(int(lst[i]))
                    else:
                        hexStr += "{:02x}".format(int(lst[i]))
            else:
                # hundredths of second, deviation,clock status（后三位都为16进制）
                hexStr += lst[i]
        return hexStr.upper()

    if len(lst) > 1:
        # Diamond用的波斯历，此处将波斯历转为公历
        if Singleton().Project == "diamond":
            gregorianDateTime = persianToGregorian(dateTime)
            dt = datetime.datetime.strptime(gregorianDateTime[:19], '%Y-%m-%d %H:%M:%S')
        else:
            dt = datetime.datetime.strptime(dateTime[:19], '%Y-%m-%d %H:%M:%S')

    if len(lst) == 9:       # 2019-05-01 14:24:45 0,32768,0;   2019-05-01 14:30:30 00,8000,00
        # hexData 用于标记 HOS, Deviation, Clock Status 是否为 16 进制数据
        hexData = False
        for i in [6, 7, 8]:
            # 判断是否为16进制数据的依据 (判断仍不充分, 有误判的可能; 故建议尽可能地传 10 进制数)
            # 1. HOS, Deviation, Clock Status 三个字段中任意一个字段包含[a-zA-Z]即认为全是16进制数据
            # 2. HOS的长度为2, Deviation的长度为4, Clock Status的长度为2; 同时满足这三个条件即认为是16进制数据
            if re.search('[a-zA-Z]', lst[i]) or (len(str(lst[6])) == 2 and len(str(lst[7])) == 4 and len(str(lst[8])) == 2):
                hexData = True

        for index, item in enumerate(lst):
            if index == 0:
                hexStr += "{:04x}".format(int(item))
            if index in [1, 2, 3, 4, 5]:
                hexStr += "{:02x}".format(int(item))
            if index == 6 or index == 8:
                if hexData:
                    hexStr += str(item).rjust(2, "0")
                else:
                    hexStr += "{:02x}".format(int(item))
            if index == 7:
                if hexData:
                    hexStr += str(item).rjust(4, "0").upper()
                else:
                    hexStr += "{:04x}".format(int(item))
        return (hexStr[:8] + dec_toHexStr(dt.isoweekday(), 2) + hexStr[8:]).upper()

    if len(lst) == 6:   # 2019-05-1 14:24:45
        for index, item in enumerate(lst):
            if index == 0:
                hexStr += "{:04x}".format(int(item))
            else:
                hexStr += "{:02x}".format(int(item))
        # return (hexStr[:8] + 'FF' + hexStr[8:] + "00800000").upper()
        return (hexStr[:8] + dec_toHexStr(dt.isoweekday(), 2) + hexStr[8:] + getTimeSuffix()).upper()

    # 直接返回
    return dateTime


def persianToGregorian(dateTime):
    """
    将波斯历转为公历

    :param dateTime:
    :return:
    """

    dateList = [int(e) for e in (dateTime[:10]).split("-")]
    gregorianDate = persian.to_gregorian(*dateList)
    gregorianDate = [str(e).rjust(2, "0") for e in gregorianDate]
    gregorianDateTime = "-".join(gregorianDate) + dateTime[10:]
    return gregorianDateTime

def gregorianToPersian(dateTime):
    """
    将公历转为波斯历

    :param dateTime:
    :return:
    """

    dateList = [int(e) for e in (dateTime[:10]).split("-")]
    persianDate = persian.from_gregorian(*dateList)
    persianDate = [str(e).rjust(2, "0") for e in persianDate]
    persianDate = "-".join(persianDate) + dateTime[10:]
    return persianDate


def time_toHex(timeString):
    """
    将time字符串格式时间转换成16进制字符串

    :param timeString:     时间字符串
    :return:               16进制字符串

    >>> time_toHex("22:00:13")
    '16000D'
    """
    hexStr = ""
    lst = re.split(r"[\.,\:,\/,\-,\ ]", timeString)

    for item in lst:
        if len(str(item)) >= 4:
            if item.find("F") != -1:
                hexStr += item
            else:
                hexStr += "{:04x}".format(int(item))
        else:
            if item.find("F") != -1:
                hexStr += item
            else:
                hexStr += "{:02x}".format(int(item))
    return hexStr.upper()


def date_toHex(dateString, needWeek=False):
    """
    将date字符串格式时间转换成16进制

    :param dateString:         日期字符串
    :param needWeek:           是否需要Week
    :return:                   十六进制字符串

    >>> date_toHex("2019-03-18")
    '07E30312'
    """
    hexStr = ""
    lst = re.split("[\.,\:, \-]", dateString)
    for i in range(0, len(lst)):
        if re.search("[A-F]", lst[i]):
            hexStr += lst[i]
        else:
            if i == 0:
                hexStr += "{:04x}".format(int(lst[i]))
            else:
                hexStr += "{:02x}".format(int(lst[i]))

    if needWeek:
        weekday = datetime.datetime.strptime(dateString, '%Y-%m-%d').weekday() + 1
        hexStr += dec_toHexStr(weekday, 2)

    return hexStr.upper()


def seasonDateTime_toHex(dateTime):
    """
    将tariff season字符串格式时间转换成16进制

    :param dateTime:         日期字符串(month-day hour:minute:second status)
    :return:                 16进制字符串

    >>> seasonDateTime_toHex('02-01 12:30:00 0')
    'FFFF0201FF0C1E0000800000'
    """
    hexStr = ""
    lst = re.split("[\-,\:,\/,\-,\ ]", dateTime)
    for item in lst:
        hexStr += "{:02x}".format(int(item))
    return 'FFFF' + (hexStr[:4] + 'FF' + hexStr[4:10] + "008000" + hexStr[10:]).upper()


def dayDateTime_toHex(dayDateString):
    """
    将tariff day字符串格式时间转换成16进制

    :param dayDateString:             '12:30:40.0'  (hour:minute:second status)  ==>  0C1E2800
    :return:                          16进制字符串
    >>> dayDateTime_toHex('12:30:40.0')
    '0C1E2800'
    """

    return time_toHex(dayDateString)


def hex_toDateTimeString(hexDateStr):
    """
    将16进制时间转换成字符串格式时间

    :param hexDateStr:                16进制字符串
    :return:                          dateTime字符串

    >>> hex_toDateTimeString('07E30501030E1E1E00800000')
    '2019-05-01 14:30:30 00,8000,00'
    """

    # 如果日期是全F格式则不进行转换  "FFFF-FF-FF-FF-FF-FF-FF-FF-8000-09"
    datetime_str_list = [hexDateStr[:4], hexDateStr[4:6], hexDateStr[6:8], hexDateStr[10:12],hexDateStr[12:14], hexDateStr[14:16]]
    year, month, day, hour, minute, second = ["{:0d}".replace('d', str(len(e))).format(hex_toDec(e)) if e != "F"*len(e) else e for e in datetime_str_list]

    # hos = "{:d}".format(hex_toDec(hexDateStr[16:18]))
    # dev = "{:d}".format(hex_toDec(hexDateStr[18:22]))
    # status = "{:d}".format(hex_toDec(hexDateStr[22:24]))

    # hos = "0x" + hexDateStr[16:18]
    # dev = "0x" + hexDateStr[18:22]
    # status = "0x" + hexDateStr[22:24]

    hos = hexDateStr[16:18]
    dev = hexDateStr[18:22]
    status = hexDateStr[22:24]
    return f'{year}-{month}-{day} {hour}:{minute}:{second} {hos},{dev},{status}'
    # return f'{year}-{month}-{day} {hour}:{minute}:{second}'


def hex_toTimeString(hexTime):
    """
    将16进制时间转换成对应的

    :param hexTime:        16进制字符串
    :return:               time字符串(hour:minute:second:hundredths)

    >>> hex_toTimeString('0E1E1E00')
    '14:30:30:00'
    """
    hour = "{:02}".format(hex_toDec(hexTime[:2]))
    minute = "{:02}".format(hex_toDec(hexTime[2:4]))
    second = "{:02}".format(hex_toDec(hexTime[4:6]))
    hundredths = "{:02}".format(hex_toDec(hexTime[6:8]))
    return f'{hour}:{minute}:{second}:{hundredths}'


def hex_toDateString(hexDate):
    """
    将16进制时间转换成对应的date字符串 (year:month:day:week)

    :param hexDate:          16进制字符串
    :return:                 Date字符串(year:month:day:week)

    >>> hex_toDateString('07E30501030E1E1E00800000')
    '2019-05-01-03'
    """

    result = ""
    for index, value in enumerate([hexDate[:4],  hexDate[4:6], hexDate[6:8], hexDate[8:10]]):
        if not value.startswith("F"):
            if index == 0:
                value = "{:04}".format(hex_toDec(value))
            else:
                value = "{:02}".format(hex_toDec(value))
        result += value
        if index != 3:
            result = result + "-"

    return result


# 08020101FF02000000800000 => ('0802-01-01-FF-02-00-00-00-8000-00', 'year=2050, month=1, day=1, week=FF(not specified), hour=2, minute=0, second=0, hos=0, dev=8000(not specified), status=00')
def hex_toWildcardTimeString(hexDS):
    """
    将16进制时间转换成夏令时格式

    :param hexDS:           16进制字符串
    :return:                夏令时格式('0802-01-01-FF-02-00-00-00-8000-00')

    >>> hex_toWildcardTimeString('07E30501030E1E1E00800000')
    '07E3-05-01-03-0E-1E-1E-00-8000-00'
    """
    digitValue = list()

    year = hexDS[:4]
    digitValue.append(year)
    if year == "FFFF":
        year += "(not specified)"
    else:
        year = hex_toDec(year)

    month = hexDS[4:6]
    digitValue.append(month)
    if month == "FD":
        month += "(daylight_savings_end)"
    elif month == "FE":
        month += "(daylight_savings_begin)"
    elif month == "FF":
        month += "(not specified)"
    else:
        month = hex_toDec(month)

    day = hexDS[6:8]
    digitValue.append(day)
    if day == "FD":
        day += "(2[nd] last day of month)"
    elif day == "FE":
        day += "(last day of month)"
    elif day == "FD":
        day += "(not specified)"
    else:
        day = hex_toDec(day)

    week = hexDS[8:10]
    digitValue.append(week)
    if week == "FF":
        week += "(not specified)"
    else:
        week = hex_toDec(week)

    hour = hexDS[10:12]
    digitValue.append(hour)
    if hour == "FF":
        hour += "(not specified)"
    else:
        hour = hex_toDec(hour)

    minute = hexDS[12:14]
    digitValue.append(minute)
    if minute == "FF":
        minute += "(not specified)"
    else:
        minute = hex_toDec(minute)

    second = hexDS[14:16]
    digitValue.append(second)
    if second == "FF":
        second += "(not specified)"
    else:
        second = hex_toDec(second)

    hos = hexDS[16:18]
    digitValue.append(hos)
    if hos == "FF":
        hos += "(not specified)"
    else:
        hos = hex_toDec(hos)

    dev = hexDS[18:22]
    digitValue.append(dev)
    if dev == "8000":
        dev += "(not specified)"

    status = hexDS[22:24]
    digitValue.append(status)

    presentValue = f'year={year}, month={month}, day={day}, week={week}, hour={hour}, minute={minute}, second={second}, hos={hos}, dev={dev}, status={status}'
    # return  "-".join(digitValue), presentValue
    return "-".join(digitValue)


def hex_toDec(hD, dataType=None):
    """
    将16进制字符串转换成10进制数

    :param hD:         16进制数字符串
    :param dataType:   数据类型
    :return:           10进制数

    >>> hex_toDec("FF")
    255

    >>> hex_toDec('B6', dataType='Integer')
    -73
    """

    # dataType 为空， 或 dataType 含 'unsigned', 或 dataType 属于 'Enum' 类型
    if dataType is None or 'Unsigned' in dataType or dataType in ['Enum']:
        if len(str(hD).strip()) > 0:
            return int(str(hD), 16)
        return hD

    # 如果最高为是否为`1`, 则进行负数处理
    else:
        num = int(str(hD), 16)
        if int(str(hD)[0], 16) >> 3:
            num -= int('F' * len(str(hD)), 16) + 1
        return num


def dec_toHexStr(dec, length=0):
    """
    将10进制数转换成16进制数

    :param dec:        10进制数
    :param length:     返回十六进制数的长度，如果长度不够在左边补零
    :return:           16进制数

    >>> dec_toHexStr(15, 2)
    '0F'
    """
    if length == 0:
        response = hex(int(dec))[2:].upper()
        if len(response) in [1, 3, 5, 7]:
            return '0' + response
        return response
    else:
        return hex(int(dec))[2:].rjust(length, '0').upper()


def bit_toHexStr(bitStr):
    """
    将BitString转换为16进制格式

    :param bitStr:             BitString
    :return:                   16进制字符串

    >>> bit_toHexStr("0000000011111111")
    '00FF'
    """
    list_s = list()
    for i in range(0, len(bitStr), 4):
        list_s.append(hex(int(str(bitStr[i:i+4]), 2))[2:])
    return "".join(list_s).upper()


def hex_toBitStr(hexStr):
    """
    将16进制转换为BitString格式

    :param hexStr:           16进制字符串
    :return:                 BitString

    >>> hex_toBitStr('00FF')
    '0000000011111111'
    """
    list_s = list()
    for i in hexStr:
        list_s.append(str(bin(int(str(i), 16))[2:]).rjust(4, "0"))
    return "".join(list_s)


def hex_toAscii(hexStr):
    """
    将16进制字符串转换成ASCII

    :param hexStr:            16进制字符串
    :return:                  ASCII字符串

    >>> hex_toAscii('3030303231383036303046463A46463A3030')
    '0002180600FF:FF:00'
    """
    list_s = []
    for i in range(0, len(hexStr), 2):
        list_s.append(chr(int(hexStr[i:i+2], 16)))
    return ''.join(list_s)


def ascii_toHex(s):
    """
    将ASCII转换成16进制字符串

    :param s:           ASCII字符串
    :return:            16进制字符串

    >>> ascii_toHex('0002180600FF:FF:00')
    '3030303231383036303046463A46463A3030'
    """
    list_h = []
    for c in str(s):
        list_h.append(str(hex(ord(c))[2:]))
    return ''.join(list_h).upper()


def hex_toOBIS(hexOBIS):
    """
    将16进制字符串转换成OBIS

    :param hexOBIS:            16进制字符串
    :return:                   OBIS字符串

    >>> hex_toOBIS('000000010265')
    '0-0:0.1.2.101'
    """
    # 处理"000000010265" 格式
    if re.match(r'^[0-9a-fA-F]{12}$', hexOBIS):
        lst = re.findall(r'([0-9a-fA-F]{2})', hexOBIS)
        result = str(int(lst[0], 16)) + "-" + str(int(lst[1], 16)) + ":"
        for item in lst[2:]:
            result += str(int(item, 16)) + "."
        return result.strip(".")
    else:
        return hexOBIS


def obis_toHex(obis):
    """
    将 OBIS 转换成 16进制字符串

    :param obis:              OBIS字符串
    :return:                  16进制字符串
    >>> obis_toHex('0-0:0.1.2.101')
    '000000010265'
    """
    if obis == "":
        return ""                           # 处理字符串为空的情况

    elif not re.search("[\.,\-,\:]", obis): # 用于测试异常字符的情况'00#00A0064FF'
        return obis
    else:
        lst = re.split("[\.,\-,\:]", obis)
        if len([item for item in lst if int(item) > 255 or int(item) < 0]) == 0:
            return "".join(["{:02x}".format(int(item)) for item in lst]).upper()


def hex_toTimeZone(hexTZ):
    """
    将16进制字符串转换成TimeZone

    :param hexTZ:           16进制字符串
    :return:                TimeZone(10进制数)

    >>> hex_toTimeZone('FFC4')
    -60
    """
    decTZ = hex_toDec(hexTZ)
    if decTZ >> 15 == 1:
        return decTZ - 65536
    return decTZ


def timezone_toHex(tz):
    """
    将TimeZone转换成16进制字符串

    :param tz:          TimeZone(10进制数)
    :return:            16进制字符串

    >>> timezone_toHex(-60)
    'FFC4'
    """
    if int(tz) < 0:
        return hex(65536 + int(tz))[2:].upper()
    else:
        return hex(int(tz))[2:].rjust(4, '0').upper()


def hex_toClockStatus(hexCS):
    """
    将16进制数转成clock_status

    :param hexCS:           16进制数
    :return:                clock_status（example, "daylight saving active"/"invalid clock status"..）

    >>> hex_toClockStatus(8)
    'invalid clock status'
    """
    status = list()
    binString = "{:08b}".format(hex_toDec(hexCS))
    if binString == "11111111":
        status.append("not specified")
    else:
        if binString[0] == "1":
            status.append("daylight saving active")
        if binString[4] == "1":
            status.append("invalid clock status")
        if binString[5] == "1":
            status.append("different clock base")
        if binString[6] == "1":
            status.append("doubtful value")
        if binString[7] == "1":
            status.append("invalid value")
    return ", ".join(status)


def ipv4_toHex(ipaddr):
    """
    将IPv4地址转换成16进制数据

    :param ipaddr:        IPv4地址
    :return:              16进制字符串

    >>> ipv4_toHex('192.168.1.12')
    'C0A8010C'
    """
    return str(hexlify(socket.inet_aton(ipaddr)), encoding="utf8").upper()


def hex_toIPv4(hexIP):
    """
    将16进制数据转换成IPv4地址

    :param hexIP:            16进制字IPv4字符串
    :return:                 IPv4地址

    >>> hex_toIPv4('C0A8010C')
    '192.168.1.12'
    """
    return socket.inet_ntoa(unhexlify(bytes(hexIP, encoding="utf8")))


def linarizeXml(xmlStr):
    """
    将多行松散型XML转换成单行紧凑型

    :param xmlStr:           xml字符串（多行）
    :return:                 xml字符串（单行）
    """
    xmlLine = ""
    for i in xmlStr.splitlines():
        xmlLine += i.strip()
    return xmlLine


if __name__ == "__main__":
    print(seasonDateTime_toHex('02-01 12:30:00 0'))
