# -*- coding: UTF-8 -*-

import subprocess
import threading

from libs.PowerControlLib import PowerControl
from libs.Singleton import Singleton

from .DataFormatAPI import *
from .KFLog import info


def waitMeterRegistered(ip, timeout=120):
    """
    等待电表注册成功

    :param ip:
    :param timeout:
    :return:
    """
    info("Wait register to meter ...")
    cmds = "ping -n 1 " + ip
    start_time = time.time()
    while time.time() - start_time < timeout:
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            msg = line.decode("gbk", "ignore")
            if str(msg).find("往返行程的估计时间") != -1:
                time.sleep(10)  # 能ping成功后仍需等待几秒中才能连接成功
                return KFResult(True, "")
    return KFResult(False, "Wait register to failed")


def connectMeter(conn, num=5):
    """
    Wait for meter register to DCU or network after power up

    :param conn:     conn object
    :param num:      尝试连接次数
    """
    for _ in range(num):
        try:
            conn.connect()
            break
        except:
            timedWait(10)


def checkDataTypeIsNum(dataType):
    """
    检查数据类型是否是数字类型

    :param dataType:   数据类型
    :return:           返回KFResult（如果是数字类型返回True, 反之返回False）
    """
    if dataType in ["LongUnsigned", "DoubleLongUnsigned", "DoubleLong", "Long64Unsigned", "Enum", "Integer",
                    "Unsigned", "Bool", "Long"]:
        return KFResult(True, "")
    return KFResult(False, "")


def powerOnWithNoActiveEnergy():
    """
    通过继电器控制电表上电（不带负载）

    :return            返回KFResult对象（成功返回True, 失败返回False）
    """
    info('Power on via relay (without load)')
    # 通过 2 口控制电表上电和掉电
    result_1 = PowerControl(Singleton().PowerControlHost, Singleton().PowerControlCircuitIndexList[:2],
                            'on').controlCircuit()
    result_2 = PowerControl(Singleton().PowerControlHost, Singleton().PowerControlCircuitIndexList[2],
                            'off').controlCircuit()
    if result_1.status and result_2.status:
        return KFResult(True, "")
    elif not result_1.status:
        return result_1
    elif not result_2.status:
        return result_2


def powerOff():
    """
    电表掉电

    :return            返回KFResult对象（成功返回True, 失败返回False）
    """
    info('Power off via relay ')
    return PowerControl(Singleton().PowerControlHost, Singleton().PowerControlCircuitIndexList[1],
                        'off').controlCircuit()


def powerOnWithActiveEnergyImport():
    """
    通过继电器控制电表上电， 带（+A）负载

    :return            返回KFResult对象（成功返回True, 失败返回False）
    """
    info('Power on through relay with (+ A) load ')
    return PowerControl(Singleton().PowerControlHost, Singleton().PowerControlCircuitIndexList, 'on').controlCircuit()


#
def powerOnWithActiveEnergyExport():
    """
    通过继电器控制电表上电，带（-A）负载

    :return             返回KFResult对象（成功返回True, 失败返回False）
    """
    info('Power on through relay with (-A) load ')
    result_1 = PowerControl(Singleton().PowerControlHost, Singleton().PowerControlCircuitIndexList[1],
                            'on').controlCircuit()
    result_2 = PowerControl(Singleton().PowerControlHost,
                            [Singleton().PowerControlCircuitIndexList[0], Singleton().PowerControlCircuitIndexList[2]],
                            'off').controlCircuit()

    if result_1.status and result_2.status:
        return KFResult(True, "")
    elif not result_1.status:
        return result_1
    elif not result_2.status:
        return result_2


def timedWait(sec, reason=None):
    """
    暂停执行指定时间

    :param sec:         秒数
    :param reason:      执行sleep 的原因
    """
    if reason is None:
        info(f"Sleep {sec}s ...")
    else:
        info(f"Sleep {sec}s, Reason: {reason} ...")
    time.sleep(int(sec))


def checkBit(val, index):
    """
    检查指定的二进制位是否为1

    :param val:     十进制字符串
    :param index:   索引位, 从右到左, 从 0 到 32, 支持多个索引位同时检查; 带^ 表示期待检查位0, 否则为1
    :return:

    checkBit(val, '1')
    checkBit(val, '1/^3/5')
    """
    errorList = list()
    bitValue = '{:040b}'.format(int(val))  # Camel Billing Status 有40位
    indexs = str(index).split("/")
    for idx in indexs:
        if idx.strip().startswith('^'):
            if bitValue[39 - int(idx.strip().replace('^', ''))] != '0':
                errorList.append(f"bit({idx.strip()}) not equals to 0 in {val} [{bitValue}]")
        else:
            if bitValue[39 - int(idx.strip())] != '1':
                errorList.append(f"bit({idx.strip()}) not equals to 1 in {val} [{bitValue}]")
    if len(errorList) == 0:
        return KFResult(True, "")
    else:
        return KFResult(False, "\n".join(errorList))


def getCurrentTime():
    """
    返回系统当前时间

    :return:        返回系统当前时间，格式为（2019-08-08 14:25:39）
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def getExpectTime(dateTimeStr, seconds):
    """
    给定一个日期字符串和秒数，返回给定秒数后的日期字符串(秒数可以为负数，即返回当前时间X秒之前的日期)

    :param dateTimeStr:             时间字符串
    :param seconds:                 秒数
    :return:                        时间字符串

    >>> getExpectTime("2019-01-01 00:00:00", 20)
    '2019-01-01 00:00:20'
    """
    expectTime = datetime.datetime.strptime(dateTimeStr[:19], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=seconds)
    return expectTime.strftime('%Y-%m-%d %H:%M:%S') + dateTimeStr[19:]


def timestamp_toDateTime(tt):
    """
    将时间戳转换成时间类型数据 <class 'datetime.datetime'>

    :param tt:        数字
    :return:          datetime.datetime对象

    >>> timestamp_toDateTime(1546275661)
    2019-01-01 01:01:01
    """
    return datetime.datetime.strptime(timestamp_toString(tt), '%Y-%m-%d %H:%M:%S')


def string_toTimestamp(st):
    """
    字符串形式的时间转换成时间戳

    :param st:   时间字符串
    :return:     数字

    >>> string_toTimestamp('2019-01-01 01:01:01')
    1546275661
    """
    return int(time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S")))


def timestamp_toString(sp):
    """
    将时间戳转换成字符串形式时间

    :param sp:     数字
    :return:       时间字符串

    >>> timestamp_toString(1546275661)
    2019-01-01 01:01:01
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sp))


def getClassAttributeType(classId, obis, project):
    """
    从conf配置文件中获取对应类中obis所对应的数据类型（目前只判断C1，C3和C4中value属性对应的数据类型）

    :param classId:          class id
    :param obis:             obis
    :param project:          project name
    :return:                 obis的value属性的数据类型
    """

    obis = obis.replace("-", ".").replace(":", ".")
    config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          f"conf/C{classId}AttrType/{project}.ini")
    with open(config) as f:
        while True:
            line = f.readline()
            if not line:
                return
            if line.strip().find(obis) > -1:
                return f.readline().strip().split("%")[-1]


class createTimeList(object):
    """
    功能: 用于创建时间列表
    """

    def __init__(self, startTime, interval, deviation=2):
        """
        :param startTime:   起始时间, 格式为"1970-01-01 01:00:00"  注: 年份必须大于1970
        :param interval:    时间间隔, 单位: 分钟
        :param deviation:   时间偏差, 单位: 秒
        """
        self.startTime = startTime
        self.interval = interval
        self.deviation = deviation

    def createDateTime(self, counter):
        """
        :param counter:  产生时间点的个数
        :return:    返回一个迭代器, 每一个返回值由两个元素组成(hex_datetime, datetime)

        >>> for item in createTimeList("1990-02-01 12:00:00", 15).createDateTime(5): print(item)
        ('07C60201040C0000008000FF', '1990-02-01 12:00:00')
        ('07C60201040C0F00008000FF', '1990-02-01 12:15:00')
        ('07C60201040C1E00008000FF', '1990-02-01 12:30:00')
        ('07C60201040C2D00008000FF', '1990-02-01 12:45:00')
        ('07C60201040D0000008000FF', '1990-02-01 13:00:00')
        """
        timestamp = string_toTimestamp(self.startTime)
        timestamp -= int(self.deviation)
        for i in range(int(counter)):
            dt = timestamp_toString(timestamp)
            yield dateTime_toHex(dt).upper(), dt
            timestamp += int(self.interval) * 60


# 返回Today的时间范围 (例如: '2019-06-15 00:00:00', '2019-06-15 23:59:59')
def time_range_of_today():
    day = datetime.datetime.now()
    date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
    date_to = datetime.datetime(day.year, day.month, day.day, 23, 59, 59)
    return str(date_from), str(date_to)


# 返回Yesterday的时间范围 (例如: '2019-06-14 00:00:00', '2019-06-14 23:59:59')
def time_range_of_yesterday():
    day = datetime.datetime.now() - datetime.timedelta(days=1)
    date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
    date_to = datetime.datetime(day.year, day.month, day.day, 23, 59, 59)
    return str(date_from), str(date_to)


# 返回last week的时间返回 (例如: '2019-06-03 00:00:00', '2019-06-09 23:59:59')
def time_range_of_lastWeek():
    d = datetime.datetime.now()
    dayscount = datetime.timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = datetime.timedelta(days=6)
    dayfrom = dayto - sixdays
    date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    return str(date_from), str(date_to)


# 返回最近的一个周期的时间
def time_offset(get_time, offset):
    get_datetime = datetime.datetime.strptime(get_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=offset)
    return get_datetime.strftime('%Y-%m-%d %H:%M:%S')


# 判断捕获值的时间戳是否连续
def checkPeriod(data, capture_period):
    if not data:
        return KFResult(False, "No data in response")
    time_list = [item[0] for item in data.values()]
    if "NullData" in time_list:
        time_list = time_list[1:]
        if len(set(time_list)) != 1:
            return KFResult(False, "Check period failed!")
    else:
        time_list = [string_toTimestamp(e[:19]) for e in time_list]
        for i in range(len(time_list) - 1):
            if (time_list[i + 1] - time_list[i]) != capture_period:
                return KFResult(False, "Check period failed!")
    return KFResult(True, '')


# 获取靠近最近一个周期的时间
def get_time_with_period(targetDateTime, period, offset=0):
    """
    获取给定时间的下一个周期时间
    :param targetDateTime:         目标时间
    :param period:       捕获周期（分钟）
    :param offset:       偏移量（设置后得到下一个周期前offset秒的时间）
    :return:
    """
    targetTimestamp = string_toTimestamp(targetDateTime)

    # 计算传入时间字符串中time部分的秒数
    currentDateTime = datetime.datetime.strptime(targetDateTime, '%Y-%m-%d %H:%M:%S')
    timeSeconds = currentDateTime.hour * 3600 + currentDateTime.minute * 60 + currentDateTime.second

    # 返回下一条曲线的捕获时间
    return timestamp_toString(targetTimestamp + period * 60 - timeSeconds % (period * 60) - offset)


def isXmlOrPdu(s):
    """
    判断参数是 XML 格式的数据还是 PDU 数据
    :param s:
    :return:
    """
    if s[0] == '<' and s[-1] == '>':
        return 'xml'
    elif len([item for item in s if not (item.upper() in "0123456789ABCEDF ")]) == 0:
        return 'pdu'
    else:
        return 'Unknow'


def crc16(data, poly=0x8408):
    """
    CRC-16-CCITT Algorithm
    用于计算 HDLC 中的校验和 (可用于 HCS 和 FCS 计算)

    原报文: 7E A0 21 02 23 21 93 48 55 81 80 14 05 02 07 EE 06 02 07 EE 07 04 00 00 00 01 08 04 00 00 00 01 B5 D4 7E
    HCS 校验:  crc16('A0 21 02 23 21 93')
    FCS 校验:  crc16('A0 21 02 23 21 93 48 55 81 80 14 05 02 07 EE 06 02 07 EE 07 04 00 00 00 01 08 04 00 00 00 01')
    """
    data = bytearray(bytes.fromhex(data))
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return hex(crc & 0xFFFF)[2:].upper().rjust(4, '0')


def getKeyByValue(dictionary, value):
    """
    字典中通过 value 查找 key
    :param dictionary:   字典数据
    :param value:        值
    :return:
    """
    return [k for k, v in dictionary.items() if v == value]


def thread_run(func, **args):
    """
    这个函数会起一个线程，用指定参数来运行给定的函数，返回函数运行结果
    :param func:
    :param args:
    :return:
    """

    class MyThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(**args)

    it = MyThread()
    it.setDaemon(True)
    it.start()
    return it


def insert_run(func, **args):
    """
    这个函数会起一个线程, 在执行之前会通知其它相关线程暂停, 执行完后通知其它相关线程继续
    :param func:
    :param args:
    :return:
    """
    try:
        isStillPause = args.pop('isStillPause')
    except KeyError:
        isStillPause = False

    class MyThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(**args)

    # 获取 threading.Event() 对象并设置flag状态
    Singleton().Pause.set()
    time.sleep(5)

    it = MyThread()
    it.start()
    it.join()

    # 执行完操作后恢复flag状态
    if not isStillPause:
        Singleton().Pause.clear()
    return it


def getTimeStamp():
    """
    获取当前时间戳, 格式为"2019-09-04 15:29:12.865"
    :return:
    """
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


def isBitString(data):
    """
    判断 data 是否为 BitString 类型 (由'0' 和'1' 组成)
    :param data:   字符串类型数据
    :return:
    """
    if isinstance(data, str):
        for index in range(len(data)):
            if data[index] != '0' and data[index] != '1':
                return False
        return True
    return False


def splitHexWithSpace(hexStr):
    """
    将连续的16进制字符串用空格进行分割
    :param  hexStr:     16进制字符串
    :return:

    >>> splitHexWithSpace('C001C100070100630200FF0300')
    C0 01 C1 00 07 01 00 63 02 00 FF 03 00
    """
    lst = re.findall(r'([0-9a-fA-F]{2})', hexStr.upper())
    return " ".join(lst)


def dealWithLongerPath(path):
    """
    在Windows平台对路径长度有限制(256个字符串), 当路径过长时需要进行特殊处理

    :param path:
    :return:
    """
    # if len(str(path)) > 250 and not path.startswith("\\\\?\\"):
    #     path = "\\\\?\\" + path
    # return path

    if not path.startswith("\\\\?\\"):
        path = "\\\\?\\" + path
    return path


def getLogicalNameByObis(obis):
    """
    通过 OBIS 查找对应的逻辑名 (在每个项目的OBIS.py文件中查找)

    :param obis:
    :return:
    """

    projectName = Singleton().Project
    with open(f'projects/{projectName}/OBIS.py', encoding='utf-8') as f:
        content = f.read()
        if obis in content:
            match = re.search("(\w*)\s*=\s*'" + obis + "'", content)
            if match:
                return match.group(1).split('_')[1]

# if __name__ == '__main__':

# for item in createTimeList("1990-02-01 12:00:00", 15, ).createDateTime(10):
#     print(item)
#
# # from DataFormatAPI import *
# # print(dateTime_toHex(getCurrentTime()))

# result = checkBit(32, "1 / ^3 / 4")
# print(result.status)
# print(result.result)

#   getExpectTime("2019-01-01 16:42:41", 163)
