# -*- coding: UTF-8 -*-

from lxml import etree


class Service(object):

    @staticmethod
    def convertDataFormat(invokeId, classId, obis, attrId):
        """
        将给定的数据转为期望长度的16进制字符串

        :param invokeId:   invoke Id
        :param classId:    class Id
        :param obis:       obis
        :param attrId:     attr Id
        :return:     转化后的数据格式
        """

        # 如果invokeId是整形, 转换成16进制, 并补齐长度为2位
        if isinstance(invokeId, int):
            invokeId = dec_toHexStr(str(invokeId)).rjust(2, '0')
        # 如果cinvokeId是字符串, 齐长度为2位
        if isinstance(invokeId, str):
            invokeId = str(invokeId).rjust(2, '0')

        # 如果classId是整形, 转换成16进制, 并补齐长度为4位
        if isinstance(classId, int):
            classId = dec_toHexStr(str(classId)).rjust(4, '0')
        # 如果classId是字符串, 齐长度为4位
        if isinstance(classId, str):
            classId = str(classId).rjust(4, '0')

        # 如果obis长度不等于12, 则认为是点分十进制形式的字符串(0-0:1.0.0.255)
        # for obis 1-0:98.1.4.1(came billing vz)
        if re.search(r"[\.:]", obis) or len(obis) != 12:
            obis = obis_toHex(obis)

        # 如果attrId是整形, 转换成16进制, 并补齐长度为2位
        if isinstance(attrId, int):
            attrId = dec_toHexStr(str(attrId)).rjust(2, '0')
        # 如果classId是字符串, 齐长度为2位
        if isinstance(attrId, str):
            attrId = str(attrId).rjust(2, '0')

        return invokeId, classId, obis, attrId

    @staticmethod
    def XmlObjToString(tree, pretty=False):
        """
        将给定的xml对象转为字符串

        :param tree:      xml object
        :param pretty:    enables formatted XML.
        :return:          xml字符串
        """
        if pretty:
            return str(etree.tostring(tree, method="xml", pretty_print=True), encoding="utf-8")
        else:
            return str(etree.tostring(tree), encoding="utf-8")


class GetService(Service):

    def __init__(self, **argv):
        """
        备注:
        1. classId, attrId, invokeId 将数值识别成10进制, 将字符串识别成16进制
        2. obis 将长度为12的字符串识别成16进制OBIS, 否则识别成点分十进制的OBIS
        """
        self.invokeId = argv.get("invokeId", "C1")
        self.classId = argv['classId']
        self.obis = argv['obis']
        self.attrId = argv['attrId']

    def baiscRequestBody(self):
        """
        构造基础的Get请求XML
        """
        self.invokeId, self.classId, self.obis, self.attrId = super(GetService, self).convertDataFormat(self.invokeId,
                                                                                                        self.classId,
                                                                                                        self.obis,
                                                                                                        self.attrId)
        getRequest = etree.Element("GetRequest")
        getRequestNormal = etree.SubElement(getRequest, "GetRequestNormal")
        etree.SubElement(getRequestNormal, "InvokeIdAndPriority").set("Value", self.invokeId.upper())
        attribDesc = etree.SubElement(getRequestNormal, "AttributeDescriptor")
        etree.SubElement(attribDesc, "ClassId").set("Value", self.classId.upper())
        etree.SubElement(attribDesc, "InstanceId").set("Value", self.obis.upper())
        etree.SubElement(attribDesc, "AttributeId").set("Value", self.attrId.upper())
        return getRequest, getRequestNormal

    def getRequestNormal(self):
        """
        构造基础的GetRequestNorml结构体

        :return:  紧凑型的XML字符串
        """

        # 返回格式化后的xml字符串
        # formatRoot = str(etree.tostring(getRequest, pretty_print=True), encoding="utf-8")

        getRequest, _ = self.baiscRequestBody()
        return getRequest

    def getRequestByTime(self, startTime, endTime, captureObjects):
        """
        基于时间抄表
        :param startTime:               起始时间 (2019-05-01 00:00:00)
        :param endTime:                 结束时间 (2019-05-01 23:59:59)
        :param captureObjects:          捕获对象列表
        :return:                        XML对象
        """
        acsSelection = etree.Element("AccessSelection")
        etree.SubElement(acsSelection, "AccessSelector").set("Value", "01")
        acsParams = etree.SubElement(acsSelection, "AccessParameters")
        struct = etree.SubElement(acsParams, "Structure")
        struct.set("Qty", "0004")

        # time range
        subStruct = etree.SubElement(struct, "Structure")
        subStruct.set("Qty", "0004")
        etree.SubElement(subStruct, "LongUnsigned").set("Value", "0008")
        etree.SubElement(subStruct, "OctetString").set("Value", "0000010000FF")  # Clock OBIS
        etree.SubElement(subStruct, "Integer").set("Value", "02")
        etree.SubElement(subStruct, "LongUnsigned").set("Value", "0000")
        # start_time
        if startTime.find("-") == -1 or startTime.find(":") == -1:
            # 如果start_time是16进制, 则不进行数据格式转换
            etree.SubElement(struct, "OctetString").set("Value", startTime)
        else:
            etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(startTime))
        # end_time
        if endTime.find("-") == -1 or endTime.find(":") == -1:
            # 如果end_time是16进制, 则不进行数据格式转换
            etree.SubElement(struct, "OctetString").set("Value", endTime)
        else:
            etree.SubElement(struct, "OctetString").set("Value", dateTime_toHex(endTime))

        # selected_values
        if captureObjects is None or len(captureObjects) == 0:
            etree.SubElement(struct, "Array").set("Qty", "0000")
        else:
            subArray = etree.SubElement(struct, "Array")
            subArray.set("Qty", dec_toHexStr(len(captureObjects), 4))
            for _, value in captureObjects.items():
                if isinstance(value, list):
                    classId, obis, attrId = [str(e) for e in value][:3]
                else:
                    classId, obis, attrId = value.split(',')
                sub2Struct = etree.SubElement(subArray, "Structure")
                sub2Struct.set("Qty", "0004")
                etree.SubElement(sub2Struct, "LongUnsigned").set("Value", dec_toHexStr(classId.strip(), 4))
                etree.SubElement(sub2Struct, "OctetString").set("Value", obis_toHex(obis.strip()))
                etree.SubElement(sub2Struct, "Integer").set("Value", dec_toHexStr(attrId.strip(), 2))
                etree.SubElement(sub2Struct, "LongUnsigned").set("Value", "0000")

        getRequest, getRequestNormal = self.baiscRequestBody()
        getRequestNormal.append(acsSelection)
        return getRequest

    def getRequestByEntry(self, startEntry, endEntry, startCaptureIndex, endCaptureIndex):
        """
        基于条目数抄表 (索引起始值都为"1")

        :param startEntry:              起始条目数 (10)
        :param endEntry:                结束条目数 (50)
        :param startCaptureIndex:       起始capture_object索引
        :param endCaptureIndex:         结束capture_object索引
        :return:                        XML对象
        """

        acsSelection = etree.Element("AccessSelection")
        etree.SubElement(acsSelection, "AccessSelector").set("Value", "02")
        acsParams = etree.SubElement(acsSelection, "AccessParameters")
        struct = etree.SubElement(acsParams, "Structure")
        struct.set("Qty", "04")

        # from_entry
        etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(startEntry, 8))
        # to_entry
        etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(endEntry, 8))
        # from_selected_value
        etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(startCaptureIndex, 4))
        # to_selected_value
        etree.SubElement(struct, "LongUnsigned").set("Value", dec_toHexStr(endCaptureIndex, 4))

        getRequest, getRequestNormal = self.baiscRequestBody()
        getRequestNormal.append(acsSelection)
        return getRequest


class SetService(Service):

    def __init__(self, **argv):
        """
        备注:
        1. invokeId, classId, attrId 将数值识别成10进制, 将字符串识别成16进制
        2. obis 将长度为12的字符串识别成16进制OBIS, 否则识别成点分十进制的OBIS
        """
        self.invokeId = argv.get("invokeId", "C1")
        self.classId = argv['classId']
        self.obis = argv['obis']
        self.attrId = argv['attrId']

    # 构造xml结构体
    def setRequestNormal(self):
        """
        构造基础的Set请求XML
        """
        # 数据类型转换
        self.invokeId, self.classId, self.obis, self.attrId = super(SetService, self).convertDataFormat(self.invokeId,
                                                                                                        self.classId,
                                                                                                        self.obis,
                                                                                                        self.attrId)

        setRequest = etree.Element("SetRequest")
        setRequestNormal = etree.SubElement(setRequest, "SetRequestNormal")
        etree.SubElement(setRequestNormal, "InvokeIdAndPriority").set("Value", self.invokeId.upper())
        attribDesc = etree.SubElement(setRequestNormal, "AttributeDescriptor")
        etree.SubElement(attribDesc, "ClassId").set("Value", self.classId.upper())
        etree.SubElement(attribDesc, "InstanceId").set("Value", self.obis.upper())
        etree.SubElement(attribDesc, "AttributeId").set("Value", self.attrId.upper())
        values = etree.SubElement(setRequestNormal, 'Value')
        return setRequest, values


class ActionService(Service):

    def __init__(self, **argv):
        """
        备注:
        1. classId, attrId, invokeId 将数值识别成10进制, 将字符串识别成16进制
        2. obis 将长度为12的字符串识别成16进制OBIS, 否则识别成点分十进制的OBIS
        """
        self.invokeId = argv.get("invokeId", "C1")
        self.classId = argv['classId']
        self.obis = argv['obis']
        self.methodId = argv['methodId']

    # 构造xml结构体
    def actionRequestNormal(self):
        """
        构造基础的Action请求xml
        """
        # 数据类型转换
        self.invokeId, self.classId, self.obis, self.methodId = super(ActionService, self).convertDataFormat(
            self.invokeId, self.classId, self.obis, self.methodId)

        actionRequest = etree.Element("ActionRequest")
        actionRequestNorml = etree.SubElement(actionRequest, "ActionRequestNormal")
        etree.SubElement(actionRequestNorml, "InvokeIdAndPriority").set("Value", self.invokeId.upper())
        methodDesc = etree.SubElement(actionRequestNorml, "MethodDescriptor")
        etree.SubElement(methodDesc, "ClassId").set("Value", self.classId.upper())
        etree.SubElement(methodDesc, "InstanceId").set("Value", self.obis.upper())
        etree.SubElement(methodDesc, "MethodId").set("Value", self.methodId.upper())
        methodParams = etree.SubElement(actionRequestNorml, 'MethodInvocationParameters')
        return actionRequest, methodParams


if __name__ == '__main__':
    # tree, formatTree = GetService(classId=7, obis='1-0:99.1.1.255', attrId=2).getRequestNormal()
    # tree, formatTree = GetService(classId='a', obis='1-0:99.1.1.255', attrId='21', invokeId=193).getRequestNormal()
    # print(tree)
    # print(formatTree)

    # tree, val = SetService(classId=8, obis='0.0.1.0.0.255', attrId=2).setRequestNormal()
    # etree.SubElement(val, 'OctetString').set("Value", "07E3050FFF0E182DFF800000")
    # print(str(etree.tostring(tree, pretty_print=True), encoding="utf-8"))

    # action = ActionService(classId="14", obis="00000D0000FF", methodId="01").actionRequestNormal()
    # print(ActionService.XmlObjToString(action[0], True))

    # req = GetService(classId="0007", obis="0100630100FF", attrId="02").getRequestByTime("2019-05-01 00:00:00", "2019-05-01 23:59:59")
    # print(GetService.XmlObjToString(req, True))

    req = GetService(classId="0007", obis="0100630100FF", attrId="02").getRequestByEntry(10, 50)
    print(GetService.XmlObjToString(req, True))
