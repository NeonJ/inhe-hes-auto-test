# -*- coding: UTF-8 -*-


from libs.Constants import *
from .XmlPdu import *


class DlmsClass(object):

    def __init__(self, conn, obis, classId):
        self.conn = conn
        self.classId = classId

        if isinstance(obis, list) and len(obis) > 0:
            self.obis = obis[0]
            self.obisList = obis
        else:
            self.obis = obis
            self.obisList = [obis]

    def getRequest(self, attrId):
        """
        向电表发送Get请求，获取电表返回数据

        :param attrId:  attr id（十进制数）
        :return:        电表返回数据
        """
        # 获取电表响应
        # attrId 指定访问的属性
        getReq = GetService(classId=self.classId, obis=self.obis, attrId=attrId).getRequestNormal()

        # 打印方法调用信息到日志
        self.showMethodInfo('get', self.classId, self.obis, attrId)
        return self.conn.receiveXmlOrPdu(GetService.XmlObjToString(getReq))

    def getRequestWithObis(self, attrId, obis):
        """
        使用指定OBIS向电表发送Get请求，获取电表返回数据

        :param attrId:  attr id（十进制数）
        :param obis:    obis
        :return:        电表返回数据
        """
        # 获取电表响应
        # attrId 指定访问的属性
        getReq = GetService(classId=self.classId, obis=obis, attrId=attrId).getRequestNormal()

        # 打印方法调用信息到日志
        self.showMethodInfo('get', self.classId, obis, attrId)
        return self.conn.receiveXmlOrPdu(GetService.XmlObjToString(getReq))

    def getRequestByTime(self, attrId, startTime, endTime, captureObjects):
        """
        使用时间范围抄读电表数据

        :param attrId:         attr id（十进制数）
        :param startTime:      开始时间（字符串）
        :param endTime:        结束时间（字符串）
        :param captureObjects: 捕获对象（字典）
        :return:               电表返回数据
        """
        # 获取电表响应
        # attrId 指定访问的属性
        getReq = GetService(classId=self.classId, obis=self.obis, attrId=attrId).getRequestByTime(startTime, endTime,
                                                                                                  captureObjects)

        # 打印方法调用信息到日志
        data = {
            'startTime': startTime,
            'endTime': endTime,
            'captureObjects': captureObjects,
        }
        self.showMethodInfo('get', self.classId, self.obis, attrId, data=data)
        return self.conn.receiveXmlOrPdu(GetService.XmlObjToString(getReq))

    def getRequestByEntry(self, attrId, startEntry, endEntry, startCaptureIndex, endCaptureIndex):
        """
        使用by entry方式抄读电表数据

        :param attrId:            attr id（十进制数）
        :param startEntry:        指定第几条开始抄读（十进制数）
        :param endEntry:          指定第几条结束抄读（十进制数）
        :param startCaptureIndex: 指定捕获对象开始的index（十进制数）
        :param endCaptureIndex:   指定捕获对象结束的index（十进制数）
        :return:                  电表返回数据
        """
        # 获取电表响应
        # attrId 指定访问的属性
        getReq = GetService(classId=self.classId, obis=self.obis, attrId=attrId).getRequestByEntry(startEntry, endEntry,
                                                                                                   startCaptureIndex,
                                                                                                   endCaptureIndex)

        # 打印方法调用信息到日志
        data = {
            'startEntry': startEntry,
            'endEntry': endEntry,
            'startCaptureIndex': startCaptureIndex,
            'endCaptureIndex': endCaptureIndex,
        }
        self.showMethodInfo('get', self.classId, self.obis, attrId, data=data)
        return self.conn.receiveXmlOrPdu(GetService.XmlObjToString(getReq))

    def getRequestByEntryWithObis(self, attrId, obis, startEntry, endEntry, startCaptureIndex, endCaptureIndex):
        """
        使用指定OBIS并用by entry方式抄读电表数据

        :param attrId:            attr id（十进制数）
        :param obis:              obis（十六进制数）
        :param startEntry:        指定第几条开始抄读（十进制数）
        :param endEntry:          指定第几条结束抄读（十进制数）
        :param startCaptureIndex: 指定捕获对象开始的index（十进制数）
        :param endCaptureIndex:   指定捕获对象结束的index（十进制数）
        :return:                  电表返回数据
        """
        # 获取电表响应
        # attrId 指定访问的属性
        getReq = GetService(classId=self.classId, obis=obis, attrId=attrId).getRequestByEntry(startEntry, endEntry,
                                                                                              startCaptureIndex,
                                                                                              endCaptureIndex)

        # 打印方法调用信息到日志
        data = {
            'startEntry': startEntry,
            'endEntry': endEntry,
            'startCaptureIndex': startCaptureIndex,
            'endCaptureIndex': endCaptureIndex,
        }
        self.showMethodInfo('get', self.classId, obis, attrId, data=data)
        # self.showMethodInfo('get', self.classId, obis, attrId, data=f'startEntry: {startEntry}, endEntry: {endEntry}, startCaptureIndex: {startCaptureIndex}, endCaptureIndex: {endCaptureIndex}')
        return self.conn.receiveXmlOrPdu(GetService.XmlObjToString(getReq))

    def setRequest(self, attrId, data, dataType, originalData=None):
        """
        向电表发送Set请求

        :param attrId:              attr id（十进制数）
        :param data:                需要设置的数据
        :param dataType:
        :param originalData:
        :return:                    KFResult对象
        """
        # 连接对象不存在时, 返回对应的XML结构体
        if self.conn is None:
            if isinstance(data, etree._Element):
                return etree.tostring(data).decode('ascii')
            return f'<{dataType} Value="{data}" />'

        # 连接对象存在时, 下发SetRequest请求
        setReq, valueNode = SetService(classId=self.classId, obis=self.obis, attrId=attrId).setRequestNormal()
        if dataType.lower() == "array" or dataType.lower() == "struct":
            valueNode.append(data)
        else:
            etree.SubElement(valueNode, dataType).set("Value", data)

        # 打印方法调用信息到日志
        if originalData is None:
            if not isinstance(data, etree._Element):
                self.showMethodInfo('set', self.classId, self.obis, attrId, data)
            else:
                self.showMethodInfo('set', self.classId, self.obis, attrId, None)
        else:
            self.showMethodInfo('set', self.classId, self.obis, attrId, originalData)

        xmlString = SetService.XmlObjToString(setReq)
        response = getSingleDataFromSetResp(self.conn.receiveXmlOrPdu(xmlString))
        if response.lower() == 'success':
            return KFResult(True, response)
        else:
            return KFResult(False, response)

    def actionRequest(self, methodId, data, dataType, originalData=None):
        """
        向电表发送Action请求

        :param methodId:            方法id
        :param data:                需要传入的数据
        :param dataType:            数据类型
        :param originalData:        未转化成XML的原始数据
        :return:                    KFResult对象
        """
        # 连接对象不存在时, 返回对应的XML结构体
        if self.conn is None:
            if isinstance(data, etree._Element):
                return etree.tostring(data).decode('ascii')
            return f'<{dataType} Value="{data}" />'

        # 连接对象存在时, 下发ActionRequest请求
        actReq, methodParams = ActionService(classId=self.classId, obis=self.obis,
                                             methodId=methodId).actionRequestNormal()
        if dataType.lower() == "array" or dataType.lower() == "structure":
            methodParams.append(data)
        else:
            etree.SubElement(methodParams, dataType).set("Value", data)
        xmlString = ActionService.XmlObjToString(actReq)

        # 打印方法调用信息到日志
        if originalData is None:
            if not isinstance(data, etree._Element):
                self.showMethodInfo('act', self.classId, self.obis, methodId, data)
            else:
                self.showMethodInfo('act', self.classId, self.obis, methodId, None)
        else:
            self.showMethodInfo('act', self.classId, self.obis, methodId, originalData)

        response = self.conn.receiveXmlOrPdu(xmlString)
        result = getSingleDataFromSetResp(response)
        if result.lower() == 'success':
            return KFResult(True, getDataFromActionResp(response))
        else:
            return KFResult(False, result)

    @staticmethod
    def showMethodInfo(mode, classId, obis, index, data=None):

        interfaceClass = ClassInterfaceMap[str(classId)]
        cls = __import__(f'dlms.base', fromlist=[interfaceClass])

        if mode == 'act':
            methodName = 'act_' + getattr(cls, interfaceClass).action_index_dict[int(index)]
        elif mode == 'set':
            methodName = 'set_' + getattr(cls, interfaceClass).attr_index_dict[int(index)]
        else:
            methodName = 'get_' + getattr(cls, interfaceClass).attr_index_dict[int(index)]

        logicalName = getLogicalNameByObis(obis)
        if logicalName:
            obis = f'{obis} [{logicalName}]'

        if data is None:
            info(
                f'## Request  ## : Class: "{interfaceClass}", Service: "{methodName}", Object: "{classId, obis, index}"')
        else:
            info(
                f'## Request  ## : Class: "{interfaceClass}", Service: "{methodName}", Object: "{classId, obis, index}", Data: "{formatDict(data, isInputData=True)}"')
