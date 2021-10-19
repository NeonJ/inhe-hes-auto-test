# -*- coding: UTF-8 -*-

import re
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


# 修改递归深度的值 (getBuffer解析成XML时容易出现异常 'RecursionError: maximum recursion depth exceeded in comparison')
# import sys
# sys.setrecursionlimit(10000)


DataAccessResultMap = {
    'success'                   : 0,
    'hardwarefault'             : 1,
    'temporaryfailure'          : 2,
    'readwritedenied'           : 3,
    'objectundefined'           : 4,
    'objectclassinconsistent'   : 9,
    'objectunavailable'         : 11,
    'typeunmatched'             : 12,
    'scopeofaccessviolated'     : 13,
    'datablockunavailable'      : 14,
    'longgetaborted'            : 15,
    'nolonggetinprogress'       : 16,
    'longsetaborted'            : 17,
    'nolongsetinprogress'       : 18,
    'datablocknumberinvalid'    : 19,
    'otherreason'               : 250,
}

ActionResultMap = {
    'success'                   : 0,
    'hardwarefault'             : 1,
    'temporaryfailure'          : 2,
    'readwritedenied'           : 3,
    'objectundefined'           : 4,
    'objectclassinconsistent'   : 9,
    'objectunavailable'         : 11,
    'typeunmatched'             : 12,
    'scopeofaccessviolated'     : 13,
    'datablockunavaliable'      : 14,
    'longactionaborted'         : 15,
    'nolongactioninprogress'    : 16,
    'otherreason'               : 255,
}

ExceptionStateErrorMap = {
    'ServiceNotAllowed'         : 1,
    'ServiceUnknown'            : 2,
}

ExceptionServiceErrorMap = {
    'OperationNotPossible'      : 1,
    'ServiceNotSupported'       : 2,
    'OtherReason'               : 3,
    'PduTooLong'                : 4,
    'DecipheringError'          : 5,
    'InvocationCounterError'    : 6,
}

ConformanceMap = {
    'reservedzero'                      : 0,
    'generalprotection'                 : 1,
    'generalblocktransfer'              : 2,
    'read'                              : 3,
    'write'                             : 4,
    'unconfirmedwrite'                  : 5,
    'reserved'                          : 6,
    'reservedseven'                     : 7,
    'attribute0supportedwithset'        : 8,
    'prioritymgmtsupported'             : 9,
    'attribute0supportedwithget'        : 10,
    'blocktransferwithget'              : 11,
    'blocktransferwithset'              : 12,
    'blocktransferwithaction'           : 13,
    'multiplereferences'                : 14,
    'informationreport'                 : 15,
    'datanotification'                  : 16,
    'access'                            : 17,
    'parameterizedaccess'               : 18,
    'get'                               : 19,
    'set'                               : 20,
    'selectiveaccess'                   : 21,
    'eventnotification'                 : 22,
    'action'                            : 23,
}

ConformanceReversedMap = {
    0   :   'ReservedZero',
    1   :   'GeneralProtection',
    2   :   'GeneralBlockTransfer',
    3   :   'Read',
    4   :   'Write',
    5   :   'UnconfirmedWrite',
    6   :   'Reserved',
    7   :   'Reserved',
    8   :   'Attribute0SupportedWithSet',
    9   :   'PriorityMgmtSupported',
    10  :   'Attribute0SupportedWithGet',
    11  :   'BlockTransferWithGet',
    12  :   'BlockTransferWithSet',
    13  :   'BlockTransferWithAction',
    14  :   'MultipleReferences',
    15  :   'InformationReport',
    16  :   'DataNotification',
    17  :   'Access',
    18  :   'ParameterizedAccess',
    19  :   'Get',
    20  :   'Set',
    21  :   'SelectiveAccess',
    22  :   'EventNotification',
    23  :   'Action',
}

DataTypeMap = {
    'NullData'              : 0,
    'Array'                 : 1,
    'Structure'             : 2,
    'Boolean'               : 3,
    'BitString'             : 4,
    'DoubleLong'            : 5,
    'DoubleLongUnsigned'    : 6,
    'OctetString'           : 9,
    'VisibleString'         : 10,
    'Utf8String'            : 12,
    'Bcd'                   : 13,
    'Integer'               : 15,
    'Long'                  : 16,
    'Unsigned'              : 17,
    'LongUnsigned'          : 18,
    'Long64'                : 20,
    'Long64Unsigned'        : 21,
    'Enum'                  : 22,
    'Float32'               : 23,
    'Float64'               : 24,
    'DateTime'              : 25,
    'Date'                  : 26,
    'Time'                  : 27,
}

ConfirmedServiceErrorMap = {
    1   :    'InitiateError'       ,
    2   :    'GetStatus'           ,
    3   :    'GetNameList'         ,
    4   :    'GetVariableAttribute',
    5   :    'Read'                ,
    6   :    'Write'               ,
    7   :    'GetDataSetAttribute' ,
    8   :    'GetTIAttribute'      ,
    9   :    'ChangeScope'         ,
    10  :    'Start'               ,
    11  :    'Stop'                ,
    12  :    'Resume'              ,
    13  :    'MakeUsable'          ,
    14  :    'InitiateLoad'        ,
    15  :    'LoadSegment'         ,
    16  :    'TerminateLoad'       ,
    17  :    'InitiateUpLoad'      ,
    18  :    'UpLoadSegment'       ,
    19  :    'TerminateUpLoad'     ,
}

ServiceErrorMap = {
    0   :   'ApplicationReference',
    1   :   'HardwareResource',
    2   :   'VdeStateError',
    3   :   'Service',
    4   :   'Definition',
    5   :   'Access',
    6   :   'Initiate',
    7   :   'LoadDataTest',
    8   :   'ChangeScope',
    9   :   'Task',
    10  :   'Other',

}

ServiceError_ApplicationReference = {
    0   :   'Other',
    1   :   'TimeElapsed',
    2   :   'ApplicationUnreachable',
    3   :   'ApplicationReferenceInvalid',
    4   :   'ApplicationContextUnsupported',
    5   :   'ProviderCommunicationError',
    6   :   'DecipheringError'
}

ServiceError_HardwareResource = {
    0   :   'Other',
    1   :   'MemoryUnavailable',
    2   :   'ProcessorResourceUnavailable',
    3   :   'MassStorageUnavailable',
    4   :   'OtherResourceUnavailable',
}

ServiceError_VdeStateErro = {
    0   :   'Other',
    1   :   'NoDlmsContext',
    2   :   'LoadingDataSet',
    3   :   'StatusNoChange',
    4   :   'StatusInoperable',
}

ServiceError_Service = {
    0   :   'Other',
    1   :   'PduSize',
    2   :   'ServiceUnsupported',
}

ServiceError_Definition = {
    0   :   'Other',
    1   :   'ObjectUndefined',
    2   :   'ObjectClassInconsistent',
    3   :   'ObjectAttributeInconsistent',
}

ServiceError_Access = {
    0   :   'Other',
    1   :   'ScopeOfAccessViolated',
    2   :   'ObjectAccessViolated',
    3   :   'HardwareFault',
    4   :   'ObjectUnavailable',
}

ServiceError_Initiate = {
    0   :   'Other',
    1   :   'DlmsVersionTooLow',
    2   :   'IncompatibleConformance',
    3   :   'PduSizeTooShort',
    4   :   'RefusedByTheVDEHandler',
}

ServiceError_LoadDataSet= {
    0   :   'Other',
    1   :   'PrimitiveOutOfSequence',
    2   :   'NotLoadable',
    3   :   'DatasetSizeTooLarge',
    4   :   'NotAwaitedSegment',
    5   :   'InterpretationFailure',
    6   :   'StorageFailure',
    7   :   'DatasetNotReady',
}

ServiceError_Task = {
    0   :   'Other',
    1   :   'NoRemoteControl',
    2   :   'TiStopped',
    3   :   'TiRunning',
    4   :   'TiUnusable',
}






def arrayList(tagList, xmlBody):
    while len(tagList) > 0:
        tag, value = tagList[-1]
        if tag == 'Array':
            xmlBody.append(f'<Array Qty="{value}">')
            tagList.pop()
            for _ in range(int(value, 16)):
                if len(tagList) > 0:
                    tag, value = tagList[-1]
                    if tag == 'Array':
                        arrayList(tagList, xmlBody)
                    elif tag == 'Structure':
                        structList(tagList, xmlBody)
                    else:
                        xmlBody.append(f'<{tag} Value="{value}" />')
                        tagList.pop()
            xmlBody.append('</Array>')

        elif tag == 'Structure':
            structList(tagList, xmlBody)

        else:
            normalList(tagList, xmlBody)


def structList(tagList, xmlBody):
    while len(tagList) > 0:
        tag, value = tagList[-1]
        if tag == 'Array':
            arrayList(tagList, xmlBody)

        elif tag == 'Structure':
            xmlBody.append(f'<Structure Qty="{value}">')
            tagList.pop()
            for _ in range(int(value, 16)):
                if len(tagList) > 0:
                    tag, value = tagList[-1]
                    if tag == 'Array':
                        arrayList(tagList, xmlBody)
                    elif tag == 'Structure':
                        structList(tagList, xmlBody)
                    else:
                        xmlBody.append(f'<{tag} Value="{value}" />')
                        tagList.pop()
            xmlBody.append('</Structure>')

        else:
            normalList(tagList, xmlBody)


def normalList(tagList, xmlBody):
    while len(tagList) > 0:
        tag, value = tagList[-1]
        if tag == 'Array':
            arrayList(tagList, xmlBody)

        elif tag == 'Structure':
            structList(tagList, xmlBody)

        else:
            xmlBody.append(f'<{tag} Value="{value}" />')
            tagList.pop()


def splitWithSpace(hexStr):
    lst = re.findall(r'([0-9a-fA-F]{2})', hexStr.upper())
    return lst[::-1]


def dec_toHexStr(dec, length=0):
    if length == 0:
        return hex(int(dec))[2:].upper()
    else:
        return hex(int(dec))[2:].rjust(length, '0').upper()


def calcDataLength(data):
    length = len(data) // 2
    if length < 128:
        return dec_toHexStr(length, 2)
    elif length < 256:
        return '81' + dec_toHexStr(length, 2)
    elif length < 65536:
        return '82' + dec_toHexStr(length, 4)


def formatXmlString(xmlString):
    """
    格式化XML字符串(带缩减和换号)

    :param xmlString:
    :return:               格式化后的字符串
    """
    xmlBody = ET.tostring(ET.fromstring(xmlString), encoding='utf-8', method='xml')
    return parseString(xmlBody).toprettyxml(indent="  ", newl="\n").replace('<?xml version="1.0" ?>', '')


def getKeyByValue(dictionary, value):
    """
    字典中通过 value 查找 key
    :param dictionary:   字典数据
    :param value:        值
    :return:
    """
    return [k for k, v in dictionary.items() if v == value]



class XmlPdu(object):

    XmlPduString = ''

    def __init__(self, XmlPduString):

        self.data = XmlPduString
        XmlPdu.XmlPduString = XmlPduString


    def toPdu(self):
        xmlData = xmltodict.parse(self.data)
        root = list(xmlData.keys())[0]

        # import json
        # print(json.dumps(xmlData[root]))

        if root == 'GetRequest':
            return GetRequest(xmlData[root]).toPdu()
        if root == 'GetResponse':
            return GetResponse(xmlData[root]).toPdu()

        if root == 'SetRequest':
            return SetRequest(xmlData[root]).toPdu()
        if root == 'SetResponse':
            return SetResponse(xmlData[root]).toPdu()

        if root == 'ActionRequest':
            return ActionRequest(xmlData[root]).toPdu()
        if root == 'ActionResponse':
            return ActionResponse(xmlData[root]).toPdu()

        if root == 'AccessRequest':
            return AccessRequest(xmlData[root]).toPdu()
        if root == 'AccessResponse':
            return AccessResponse(xmlData[root]).toPdu()

        if root == 'GeneralBlockTransfer':
            return GeneralBlockTransfer(xmlData[root]).toPdu()

        if root == 'DataNotification':
            return DataNotification(xmlData[root]).toPdu()

        if root == 'EventNotificationRequest':
            return EventNotificationRequest(xmlData[root]).toPdu()

        if root == 'ExceptionResponse':
            return ExceptionResponse(xmlData[root]).toPdu()

        if root == 'AssociationRequest':
            return AARQ(xmlData[root]).toPdu()
        if root == 'AssociationResponse':
            return AARE(xmlData[root]).toPdu()

        if root == 'InitiateRequest':
            return InitiateRequest(xmlData[root]).toPdu()
        if root == 'InitiateResponse':
            return InitiateResponse(xmlData[root]).toPdu()

        if root == 'RLRQ-apdu':
            return RlrqApdu(xmlData[root]).toPdu()
        if root == 'RLRE-apdu':
            return RlreApdu(xmlData[root]).toPdu()


    def toXml(self):

        pduList = splitWithSpace(self.data)
        if str(pduList[-1]).upper() == '7E' and str(pduList[0]).upper() == '7E':
            [pduList.pop() for _ in range(3)]
            [pduList.pop(0) for _ in range(3)]

            # hdlc address
            [pduList.pop() for _ in range(3)]

            # hdlc control + HCS
            [pduList.pop() for _ in range(3)]

            # (E6 E6 00, E6 E7 00)
            [pduList.pop() for _ in range(3)]

        tag = pduList.pop()

        if tag == '01':
            return InitiateRequest(pduList).toXml()
        if tag == '08':
            return InitiateResponse(pduList).toXml()

        if tag == '0E':
            return ConfirmedServiceError(pduList).toXml()

        if tag == '60':
            return AARQ(pduList).toXml()
        if tag == '61':
            return AARE(pduList).toXml()

        if tag == '62':
            return RlrqApdu(pduList).toXml()
        if tag == '63':
            return RlreApdu(pduList).toXml()

        if tag == 'C0':
            return GetRequest(pduList).toXml()
        if tag == 'C4':
            return GetResponse(pduList).toXml()

        if tag == 'C1':
            return SetRequest(pduList).toXml()
        if tag == 'C5':
            return SetResponse(pduList).toXml()

        if tag == 'C3':
            return ActionRequest(pduList).toXml()
        if tag == 'C7':
            return ActionResponse(pduList).toXml()

        if tag == 'D8':
            return ExceptionResponse(pduList).toXml()

        if tag == 'E0':
            return GeneralBlockTransfer(pduList).toXml()

        if tag == 'C2':
            return EventNotificationRequest(pduList).toXml()


class SelectiveAccessDescriptor(object):

    def __init__(self, data):
        self.data = data
        self.accessSelector = ''
        self.accessParameters = ''

    def toPdu(self):
        self.accessSelector = self.data['AccessSelector']['@Value']
        self.accessParameters = CosemData(path='//AccessSelection/AccessParameters//*').toPdu()
        return '01' + self.accessSelector + self.accessParameters

    def toXml(self, returnList=False):
        xmlBody = list()
        xmlBody.append('<AccessSelection>')

        accessSelector = self.data.pop()
        if accessSelector == '01':
            pass
        if accessSelector == '02':
            xmlBody.append(f'<AccessSelector Value="{accessSelector}"/>')
            xmlBody.append('<AccessParameters>')
            xmlBody.extend(CosemDataReversed(self.data).toXml(returnList=True))
            xmlBody.append('</AccessParameters>')

        xmlBody.append('</AccessSelection>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class CosemAttributeDescriptor(object):

    def __init__(self, data):
        self.data = data
        self.cosemClassId = ''
        self.cosemObjectInstanceId = ''
        self.cosemObjectAttributeId = ''

    def toPdu(self):
        self.cosemClassId = self.data['ClassId']['@Value']
        self.cosemObjectInstanceId = self.data['InstanceId']['@Value']
        self.cosemObjectAttributeId = self.data['AttributeId']['@Value']
        return self.cosemClassId + self.cosemObjectInstanceId + self.cosemObjectAttributeId

    def toXml(self, returnList=False):
        xmlBody = ['<AttributeDescriptor>']

        classId = "".join([self.data.pop() for _ in range(2)])
        instanceId = "".join([self.data.pop() for _ in range(6)])
        methodId = "".join([self.data.pop() for _ in range(1)])

        xmlBody.append(f'<ClassId Value="{classId}" />')
        xmlBody.append(f'<InstanceId Value="{instanceId}" />')
        xmlBody.append(f'<AttributeId Value="{methodId}" />')

        xmlBody.append('</AttributeDescriptor>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class CosemMethodDescriptor(object):

    def __init__(self, data):
        self.data = data
        self.cosemClassId = ''
        self.cosemObjectInstanceId = ''
        self.cosemObjectMethodId = ''

    def toPdu(self):
        self.cosemClassId = self.data['ClassId']['@Value']
        self.cosemObjectInstanceId = self.data['InstanceId']['@Value']
        self.cosemObjectMethodId = self.data['MethodId']['@Value']
        return self.cosemClassId + self.cosemObjectInstanceId + self.cosemObjectMethodId

    def toXml(self, isList=False):
        xmlBody = ['<MethodDescriptor>']

        classId = "".join([self.data.pop() for _ in range(2)])
        instanceId = "".join([self.data.pop() for _ in range(6)])
        methodId = "".join([self.data.pop() for _ in range(1)])

        xmlBody.append(f'<ClassId Value="{classId}" />')
        xmlBody.append(f'<InstanceId Value="{instanceId}" />')
        xmlBody.append(f'<MethodId Value="{methodId}" />')

        xmlBody.append('</MethodDescriptor>')

        if isList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class CosemAttributeDescriptorWithSelection(object):

    def __init__(self, path):
        self.path = path

    def toPdu(self):
        pdu = ""

        rootTag = etree.fromstring(XmlPdu.XmlPduString)
        # _attributeDescriptorWithSelectionList = rootTag.xpath("//GetRequestWithList/AttributeDescriptorList/*")
        _attributeDescriptorWithSelectionList = rootTag.xpath(self.path)

        for index in range(len(_attributeDescriptorWithSelectionList)):
            for subIndex, elem in enumerate(_attributeDescriptorWithSelectionList[index].xpath("*")):
                if subIndex == 0:
                    if elem.tag == 'AttributeDescriptor':
                        pdu += elem.xpath('ClassId')[0].attrib['Value'] + elem.xpath('InstanceId')[0].attrib['Value'] + elem.xpath('AttributeId')[0].attrib['Value']

                # 如果`AttributeDescriptor`没有配套的`AccessSelection`，则用`00`填充
                if len(_attributeDescriptorWithSelectionList[index]) == 1:
                    pdu += '00'

                if subIndex == 1:
                    if elem.tag == 'AccessSelection':
                        pdu += '01' + elem.xpath('AccessSelector')[0].attrib['Value']
                        pdu += CosemData(path=f'//GetRequestWithList/AttributeDescriptorList/_AttributeDescriptorWithSelection[{index+1}]/AccessSelection/AccessParameters//*').toPdu()

        return dec_toHexStr(len(_attributeDescriptorWithSelectionList), 2) + pdu


class CosemData(object):

    def __init__(self, path):
        self.path = path

    @staticmethod
    def DataConvert(element):

        if element.tag == 'NullData':
            return '00'

        if element.attrib.get('Qty'):
            value = element.attrib['Qty'][-2:]
        else:
            value = element.attrib['Value']

        if element.tag in ['OctetString', 'VisibleString']:
            pdu = dec_toHexStr(DataTypeMap[element.tag], 2) + calcDataLength(value) + value
        else:
            pdu = dec_toHexStr(DataTypeMap[element.tag], 2) + value

        if element.tag in ['BitString']:
            pdu = dec_toHexStr(DataTypeMap[element.tag], 2) + dec_toHexStr(len(value), 2) + dec_toHexStr(int(value, 2))

        return pdu


    def toPdu(self):
        pdu = ""
        rootTag = etree.fromstring(XmlPdu.XmlPduString)
        for elem in rootTag.xpath(self.path):
            # print(elem.tag, elem.attrib)
            pdu += self.DataConvert(elem)
        return pdu



class CosemDataReversed(object):

    def __init__(self, pdu):
        self.pdu = pdu


    def toXml(self, returnList=False):
        tagList = list()
        pduList = self.pdu
        while len(pduList) > 0:
            tag = getKeyByValue(DataTypeMap, int(pduList.pop(), 16))[0]
            if tag in ['Array', 'Structure']:
                qty = pduList.pop()
                if qty == '83':
                    qty = ''.join([pduList.pop() for _ in range(3)])
                if qty == '82':
                    qty = ''.join([pduList.pop() for _ in range(2)])
                if qty == '81':
                    qty = ''.join([pduList.pop() for _ in range(1)])
                tagList.append((tag, qty))

            if tag in ['Boolean', 'Bcd', 'Integer', 'Unsigned', 'Enum']:
                length = 1
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['DoubleLong', 'DoubleLongUnsigned', 'Float32']:
                length = 4
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['Long', 'LongUnsigned']:
                length = 2
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['Long64', 'Long64Unsigned', 'Float64']:
                length = 8
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['BitString']:
                length = int(pduList.pop(), 16) // 8
                content = "".join([pduList.pop() for _ in range(length)])
                bitValue = format(int(content, 16), 'b').rjust(int(length)*8, '0')
                tagList.append((tag, bitValue))

            if tag in ['OctetString', 'VisibleString']:
                length = int(pduList.pop(), 16)
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['DateTime']:
                length = 12
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['Date']:
                length = 5
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

            if tag in ['Time']:
                length = 4
                content = "".join([pduList.pop() for _ in range(length)])
                tagList.append((tag, content))

        tagList = tagList[::-1]
        xmlBody = list()

        while len(tagList) > 0:
            if tagList[-1][0] == 'Array':
                arrayList(tagList, xmlBody)
            elif tagList[-1][0] == 'Structure':
                structList(tagList, xmlBody)
            else:
                normalList(tagList, xmlBody)

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class SetRequest(object):

    def __init__(self, data):
        self.data = data
        self.setRequestNormal = ''
        self.setRequestWithFirstDatablock = ''
        self.setRequestWithDatablock = ''
        self.setRequestWithList = ''
        self.setRequestWithListAndFirstDatablock = ''


    def toPdu(self):
        if self.data.get('SetRequestNormal'):
            return 'C101' + SetRequestNormal(self.data['SetRequestNormal']).toPdu()

        if self.data.get('SetRequestWithFirstDataBlock'):
            return 'C102' + SetRequestWithFirstDataBlock(self.data['SetRequestWithFirstDataBlock']).toPdu()

        if self.data.get('SetRequestWithDataBlock'):
            return 'C103' + SetRequestWithDataBlock(self.data['SetRequestWithDataBlock']).toPdu()

        if self.data.get('SetRequestNormalWithList'):
            return 'C104' + SetRequestWithList(self.data['SetRequestNormalWithList']).toPdu()


    def toXml(self):
        tag = self.data.pop()
        if tag == '01':
            return SetRequestNormal(self.data).toXml()

        if tag == '02':
            return SetRequestWithFirstDataBlock(self.data).toXml()



class SetRequestNormal(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemAttributeDescriptor = ''
        self.accessSelection = ''
        self.value = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.cosemAttributeDescriptor = CosemAttributeDescriptor(self.data['AttributeDescriptor']).toPdu()
        self.accessSelection = '00'
        self.value = CosemData(path='//SetRequestNormal/Value//*').toPdu()
        return self.invokeIdAndPriority + self.cosemAttributeDescriptor + self.accessSelection + self.value


    def toXml(self, returnList=False):
        xmlBody = ['<SetRequest>', '<SetRequestNormal>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # cosem-attribute-descriptor
        xmlBody.extend(CosemAttributeDescriptor(self.data).toXml(returnList=True))

        # access-selection
        isAccessSelectionExist = self.data.pop()
        if isAccessSelectionExist == '01':
            pass

        # value
        xmlBody.append('<Value>')
        xmlBody.extend(CosemDataReversed(self.data).toXml(returnList=True))
        xmlBody.append('</Value>')

        xmlBody.append('</SetRequestNormal>')
        xmlBody.append('</SetRequest>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class SetRequestWithFirstDataBlock(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemAttributeDescriptor = ''
        self.accessSelection = ''
        self.lastBlock = ''
        self.blockNumber = ''
        self.rawData = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.cosemAttributeDescriptor = CosemAttributeDescriptor(self.data['AttributeDescriptor']).toPdu()
        self.accessSelection = '00'
        self.lastBlock = self.data['DataBlock']['LastBlock']['@Value']
        self.blockNumber = self.data['DataBlock']['BlockNumber']['@Value']
        rawData = self.data['DataBlock']['RawData']['@Value']
        self.rawData = calcDataLength(rawData) + rawData

        return self.invokeIdAndPriority + self.cosemAttributeDescriptor + self.accessSelection + self.lastBlock + self.blockNumber + self.rawData


    def toXml(self, returnList=False):
        xmlBody = ['<SetRequest>', '<SetRequestWithFirstDataBlock>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # cosem-attribute-descriptor
        xmlBody.extend(CosemAttributeDescriptor(self.data).toXml(returnList=True))

        # access-selection
        isAccessSelectionExist = self.data.pop()
        if isAccessSelectionExist == '01':
            pass

        # data-block
        xmlBody.append('<DataBlock>')
        self.lastBlock = self.data.pop()
        xmlBody.extend(f'<LastBlock Value="{self.lastBlock}" />')

        self.blockNumber = ''.join([self.data.pop() for _ in range(4)])
        xmlBody.extend(f'<BlockNumber Value="{self.blockNumber}" />')

        dataLen = self.data.pop()
        if str(dataLen) == '83':
            [self.data.pop() for _ in range(3)]
        elif str(dataLen) == '82':
            [self.data.pop() for _ in range(2)]
        elif str(dataLen) == '81':
            self.data.pop()

        while len(self.data) > 0:
            self.rawData += self.data.pop()
        xmlBody.extend(f'<RawData Value="{self.rawData}" />')

        xmlBody.append('</DataBlock>')
        xmlBody.append('</SetRequestWithFirstDataBlock>')
        xmlBody.append('</SetRequest>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class SetRequestWithDataBlock(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.lastBlock = ''
        self.blockNumber = ''
        self.rawData = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.lastBlock = self.data['DataBlock']['LastBlock']['@Value']
        self.blockNumber = self.data['DataBlock']['BlockNumber']['@Value']
        rawData = self.data['DataBlock']['RawData']['@Value']
        self.rawData = calcDataLength(rawData) + rawData

        return self.invokeIdAndPriority + self.lastBlock + self.blockNumber + self.rawData


    def toXml(self, returnList=False):
        xmlBody = ['<SetRequest>', '<SetRequestWithDataBlock>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # data-block
        xmlBody.append('<DataBlock>')
        self.lastBlock = self.data.pop()
        xmlBody.extend(f'<LastBlock Value="{self.lastBlock}" />')

        self.blockNumber = ''.join([self.data.pop() for _ in range(4)])
        xmlBody.extend(f'<BlockNumber Value="{self.blockNumber}" />')

        dataLen = self.data.pop()
        if str(dataLen) == '83':
            [self.data.pop() for _ in range(3)]
        elif str(dataLen) == '82':
            [self.data.pop() for _ in range(2)]
        elif str(dataLen) == '81':
            self.data.pop()

        while len(self.data) > 0:
            self.rawData += self.data.pop()
        xmlBody.extend(f'<RawData Value="{self.rawData}" />')

        xmlBody.append('</DataBlock>')
        xmlBody.append('</SetRequestWithDataBlock>')
        xmlBody.append('</SetRequest>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class SetRequestWithList(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemAttributeDescriptorWithSelection = ''
        self.valueList = ''

    def toPdu(self):
        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.cosemAttributeDescriptorWithSelection = CosemAttributeDescriptorWithSelection(path='//SetRequestNormalWithList/AttributeDescriptorList/*').toPdu()
        self.valueList = self.data['ValueList']['@Qty'][-2:] + CosemData(path='//SetRequestNormalWithList/ValueList//*').toPdu()
        return self.invokeIdAndPriority + self.cosemAttributeDescriptorWithSelection + self.valueList



class SetResponse(object):

    def __init__(self, data):
        self.data = data
        # self.setResponseNormal = ''
        # self.setResponseDatablock = ''
        # self.setResponseLastDatablock = ''
        # self.setResponseLastDatablockWithList = ''
        # self.setResponseWithList = ''


    def toPdu(self):
        if self.data.get('SetResponseNormal'):
            return 'C501' + SetResponseNormal(self.data.get('SetResponseNormal')).toPdu()
        if self.data.get('SetResponseForDataBlock'):
            return 'C502' + SetResponseForDataBlock(self.data.get('SetResponseForDataBlock')).toPdu()
        if self.data.get('SetResponseForLastDataBlock'):
            return 'C503' + SetResponseForLastDataBlock(self.data.get('SetResponseForLastDataBlock')).toPdu()


    def toXml(self):
        tag = self.data.pop()
        if tag == '01':
            return SetResponseNormal(self.data).toXml()
        if tag == '02':
            return SetResponseForDataBlock(self.data).toXml()
        if tag == '03':
            return SetResponseForLastDataBlock(self.data).toXml()



class SetResponseNormal(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.result = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.result = dec_toHexStr(DataAccessResultMap[self.data['Result']['@Value'].lower()], 2)
        return self.invokeIdAndPriority + self.result


    def toXml(self, returnList=False):
        xmlBody = ['<SetResponse>', '<SetResponseNormal>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # result
        self.result = getKeyByValue(DataAccessResultMap, int(self.data.pop(), 16))[0].capitalize()
        xmlBody.append(f'<Result Value="{self.result}" />')

        xmlBody.append('</SetResponseNormal>')
        xmlBody.append('</SetResponse>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class SetResponseForDataBlock(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.blockNumber = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.blockNumber = self.data['BlockNumber']['@Value']
        return self.invokeIdAndPriority + self.blockNumber


    def toXml(self, returnList=False):
        xmlBody = ['<SetResponse>', '<SetResponseForDataBlock>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        self.blockNumber = ''.join([self.data.pop() for _ in range(4)])
        xmlBody.append(f'<BlockNumber Value="{self.blockNumber}" />')

        xmlBody.append('</SetResponseForDataBlock>')
        xmlBody.append('</SetResponse>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class SetResponseForLastDataBlock(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.result = ''
        self.blockNumber = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.result = self.data['Result']['@Value']
        self.blockNumber = self.data['BlockNumber']['@Value']
        return self.invokeIdAndPriority + self.result + self.blockNumber


    def toXml(self, returnList=False):
        xmlBody = ['<SetResponse>', '<SetResponseForLastDataBlock>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        self.result = getKeyByValue(DataAccessResultMap, int(self.data.pop(), 16))[0].capitalize()
        xmlBody.append(f'<Result Value="{self.result}"/>')

        self.blockNumber = ''.join([self.data.pop() for _ in range(4)])
        xmlBody.append(f'<BlockNumber Value="{self.blockNumber}" />')

        xmlBody.append('</SetResponseForLastDataBlock>')
        xmlBody.append('</SetResponse>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class GetRequest(object):

    def __init__(self, data):
        self.data = data
        self.getRequestNormal = ''
        self.getRequestNext = ''
        self.getRequestWithList = ''

    def toPdu(self):
        if self.data.get('GetRequestNormal'):
            return 'C001' + GetRequestNormal(self.data['GetRequestNormal']).toPdu()

        if self.data.get('GetRequestForNextDataBlock'):
            return 'C002' + GetRequestNext(self.data['GetRequestForNextDataBlock']).toPdu()

        if self.data.get('GetRequestWithList'):
            return 'C003' + GetRequestWithList(self.data['GetRequestWithList']).toPdu()

    def toXml(self):
        tag = self.data.pop()
        if tag == '01':
            return GetRequestNormal(self.data).toXml()

        if tag == '02':
            return GetRequestNext(self.data).toXml()



class GetRequestNormal(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemAttributeDescriptor = ''
        self.accessSelection = '00'

    def toPdu(self):
        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.cosemAttributeDescriptor = CosemAttributeDescriptor(self.data['AttributeDescriptor']).toPdu()
        if self.data.get('AccessSelection'):
            self.accessSelection = SelectiveAccessDescriptor(self.data['AccessSelection']).toPdu()
        return self.invokeIdAndPriority + self.cosemAttributeDescriptor + self.accessSelection

    def toXml(self, returnList=False):
        xmlBody = ['<GetRequest>', '<GetRequestNormal>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # cosem-attribute-descriptor
        xmlBody.extend(CosemAttributeDescriptor(self.data).toXml(returnList=True))

        # access-selection
        if self.data.pop() == '01':
            xmlBody.extend(SelectiveAccessDescriptor(self.data).toXml(returnList=True))

        xmlBody.append('</GetRequestNormal>')
        xmlBody.append('</GetRequest>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class GetRequestNext(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.blockNumber = ''

    def toPdu(self):
        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.blockNumber = self.data['BlockNumber']['@Value']
        return self.invokeIdAndPriority + self.blockNumber

    def toXml(self, returnList=False):
        xmlBody = ['<GetRequest>', '<GetRequestForNextDataBlock>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        self.blockNumber = "".join([self.data.pop() for _ in range(4)])
        xmlBody.append(f'<BlockNumber Value="{self.blockNumber}"/>')

        xmlBody.append('</GetRequestForNextDataBlock>')
        xmlBody.append('</GetRequest>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class GetRequestWithList(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemAttributeDescriptorWithSelection = ''

    def toPdu(self):
        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.cosemAttributeDescriptorWithSelection = CosemAttributeDescriptorWithSelection(path='//GetRequestWithList/AttributeDescriptorList/*').toPdu()
        return self.invokeIdAndPriority + self.cosemAttributeDescriptorWithSelection


class GetResponse(object):

    def __init__(self, data):
        self.data = data
        self.getResponseNormal = ''
        self.getResponseWithDatablock = ''
        self.getResponseWithList = ''

    def toPdu(self):
        if self.data.get('GetResponseNormal'):
            return 'C401' + GetResponseNormal(self.data.get('GetResponseNormal')).toPdu()
        if self.data.get('GetResponsewithDataBlock'):
            return 'C402' + GetResponsewithDataBlock(self.data.get('GetResponsewithDataBlock')).toPdu()


    def toXml(self):
        tag = self.data.pop()
        if tag == '01':
            return GetResponseNormal(self.data).toXml()
        if tag == '02':
            return GetResponsewithDataBlock(self.data).toXml()


class GetResponseNormal(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.result = ''

    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        if self.data['Result'].get('DataAccessError'):
            self.result = '01' + DataAccessResultMap[self.data['Result']['DataAccessError']['@Value'].lower()]
        else:
            self.result = '00' + CosemData(path='//Result/Data//*').toPdu()
        return self.invokeIdAndPriority + self.result

    def toXml(self, returnList=False):
        xmlBody = ['<GetResponse>', '<GetResponseNormal>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # result
        xmlBody.append('<Result>')
        # result [Get-Data-Result]
        if self.data.pop() == '00':
            xmlBody.append('<Data>')
            xmlBody.extend(CosemDataReversed(self.data).toXml(returnList=True))
            xmlBody.append('</Data>')
        else:
            dataAccessError = getKeyByValue(DataAccessResultMap, int(self.data.pop(), 16))[0]
            xmlBody.append(f'<DataAccessError Value="{str(dataAccessError).capitalize()}" />')

        xmlBody.append('</Result>')
        xmlBody.append('</GetResponseNormal>')
        xmlBody.append('</GetResponse>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class GetResponsewithDataBlock(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.lastBlock = ''
        self.blockNumber = ''
        self.rawData = ''
        self.dataAccessResult = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.lastBlock = self.data['Result']['LastBlock']['@Value']
        self.blockNumber = self.data['Result']['BlockNumber']['@Value']

        if self.data['Result']['Result'].get('RawData'):
            rawData =  self.data['Result']['Result']['RawData']['@Value']
            self.rawData = '00' + calcDataLength(rawData) + rawData

        return self.invokeIdAndPriority + self.lastBlock + self.blockNumber + self.rawData + self.dataAccessResult


    def toXml(self, returnList=False):
        xmlBody = ['<GetResponse>', '<GetResponsewithDataBlock>']

        self.invokeIdAndPriority = self.data.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}"/>')

        # result
        xmlBody.append('<Result>')
        self.lastBlock = self.data.pop()
        xmlBody.append(f'<LastBlock Value="{self.lastBlock}" />')
        self.blockNumber = "".join([self.data.pop() for _ in range(4)])
        xmlBody.append(f'<BlockNumber Value="{self.blockNumber}" />')

        xmlBody.append('<Result>')
        if self.data.pop() == '00':         # raw-data
            dataLen = self.data.pop()
            if str(dataLen) == '83':
                [self.data.pop() for _ in range(3)]
            elif str(dataLen) == '82':
                [self.data.pop() for _ in range(2)]
            elif str(dataLen) == '81':
                self.data.pop()

            self.rawData = "".join([self.data.pop() for _ in range(len(self.data))])
            xmlBody.append(f'<RawData Value="{self.rawData}" />')
        else:                               # data-access-result
            pass
        xmlBody.append('</Result>')

        xmlBody.append('</Result>')
        xmlBody.append('</GetResponsewithDataBlock>')
        xmlBody.append('</GetResponse>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class ActionRequest(object):

    def __init__(self, data):
        self.data = data
        self.actionRequestNormal = ''
        self.actionRequestNextPblock = ''
        self.actionRequestWithList = ''
        self.actionRequestWithFirstPblock = ''
        self.actionRequestWithListAndFirstPblock = ''
        self.actionRequestWithPblock = ''

    def toPdu(self):
        if self.data.get('ActionRequestNormal'):
            return 'C301' + ActionRequestNormal(self.data['ActionRequestNormal']).toPdu()

        if self.data.get('ActionRequestWithList'):
            return 'C303' + ActionRequestWithList(self.data['ActionRequestWithList']).toPdu()

    def toXml(self):
        tag = self.data.pop()
        if tag == '01':
            return ActionRequestNormal(self.data).toXml()


class ActionRequestNormal(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemMethodDescriptor = ''
        self.methodInvocationParameters = ''


    def toPdu(self):
        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.cosemMethodDescriptor = CosemMethodDescriptor(self.data['MethodDescriptor']).toPdu()
        if self.data.get('MethodInvocationParameters'):
            self.methodInvocationParameters = '01' + CosemData(path='//ActionRequestNormal/MethodInvocationParameters//*').toPdu()
        else:
            self.methodInvocationParameters = '00'
        return self.invokeIdAndPriority + self.cosemMethodDescriptor + self.methodInvocationParameters


    def toXml(self, isList=False):
        xmlBody = ['<ActionRequest>', '<ActionRequestNormal>']

        pduList = self.data
        self.invokeIdAndPriority = pduList.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}" />')

        xmlBody.extend(CosemMethodDescriptor(pduList).toXml(isList=True))

        isMethodInvocationParams = pduList.pop()
        if isMethodInvocationParams == '01':
            xmlBody.append('<MethodInvocationParameters>')
            xmlBody.extend(CosemDataReversed(pduList).toXml(returnList=True))
            xmlBody.append('</MethodInvocationParameters>')

        xmlBody.append('</ActionRequestNormal>')
        xmlBody.append('</ActionRequest>')

        if isList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class ActionRequestWithList(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.cosemMethodDescriptor = ''
        self.methodInvocationParameters = ''

    def toPdu(self):
        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']

        # 获取`MethodDescriptorList`长度
        self.cosemMethodDescriptor += self.data['MethodDescriptorList']['@Qty'][-2:]
        rootTag = etree.fromstring(XmlPdu.XmlPduString)
        for elem in rootTag.xpath("//ActionRequestWithList/MethodDescriptorList/*"):
            self.cosemMethodDescriptor += elem.xpath('ClassId')[0].attrib['Value'] + elem.xpath('InstanceId')[0].attrib['Value'] + elem.xpath('MethodId')[0].attrib['Value']

        if self.data.get('MethodInvocationParameters'):
            # 获取`MethodInvocationParameters`长度
            self.methodInvocationParameters += self.data['MethodInvocationParameters']['@Qty'][-2:]
            self.methodInvocationParameters += CosemData(path='//ActionRequestWithList/MethodInvocationParameters//*').toPdu()

        return self.invokeIdAndPriority + self.cosemMethodDescriptor + self.methodInvocationParameters


class ActionResponse(object):

    def __init__(self, data):
        self.data = data
        self.actionResponseNormal = ''
        self.actionResponseWithPblock = ''
        self.actionResponseWithList = ''
        self.actionResponseNextPblock = ''

    def toPdu(self):
        if self.data.get('ActionResponseNormal'):
            return 'C701' + ActionResponseNormal(self.data.get('ActionResponseNormal')).toPdu()

    def toXml(self):
        tag = self.data.pop()
        if tag == '01':
            return ActionResponseNormal(self.data).toXml()


class ActionResponseNormal(object):

    def __init__(self, data):
        self.data = data
        self.invokeIdAndPriority = ''
        self.result = ''
        self.returnParameters = ''

    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        self.invokeIdAndPriority = self.data['InvokeIdAndPriority']['@Value']
        self.result = dec_toHexStr(ActionResultMap[self.data['Result']['@Value'].lower()], 2)
        if self.data.get('ReturnParameters'):
            # '01' -> 代表可选属性`return-parameters`存在;  '00' -> 代表选择了`CHOICE`的第一个属性(Get-Data-Result)
            self.returnParameters = '01' + '00' + CosemData(path='//ActionResponseNormal/ReturnParameters//*').toPdu()
        else:
            self.returnParameters = '00'
        return self.invokeIdAndPriority + self.result + self.returnParameters

    def toXml(self, returnList=False):
        xmlBody = ['<ActionResponse>', '<ActionResponseNormal>']

        pduList = self.data

        self.invokeIdAndPriority = pduList.pop()
        xmlBody.append(f'<InvokeIdAndPriority Value="{self.invokeIdAndPriority}" />')

        self.result = getKeyByValue(ActionResultMap, int(pduList.pop(), 16))[0]
        xmlBody.append(f'<Result Value="{self.result}" />')

        isReturnParametersExist = pduList.pop()
        if isReturnParametersExist == '01':
            xmlBody.append(f'<ReturnParameters>')
            if pduList.pop() == '00':           # Get-Data-Result ::= CHOICE   [data]
                xmlBody.extend(CosemDataReversed(pduList).toXml(returnList=True))
            else:                               # Get-Data-Result ::= CHOICE   [data-access-result]
                pass
            xmlBody.append(f'</ReturnParameters>')

        xmlBody.append('</ActionResponseNormal>')
        xmlBody.append('</ActionResponse>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class AccessRequest(object):

    def __init__(self, data):
        self.data = data
        self.longInvokeIdAndPriority = ''
        self.dateTime = ''
        self.accessRequestBody = ''

    def toPdu(self):
        self.longInvokeIdAndPriority = self.data['LongInvokeIdAndPriority']['@Value']
        self.dateTime = self.data['OctetString']['@Value'].strip()
        if len(self.dateTime) > 0:
            self.dateTime = calcDataLength(self.dateTime) + self.dateTime
        else:
            self.dateTime = '00'
        self.accessRequestBody = AccessRequestBody(self.data['AccessRequestBody']).toPdu()

        return 'D9' + self.longInvokeIdAndPriority + self.dateTime + self.accessRequestBody


class AccessRequestBody(object):

    def __init__(self, data):
        self.data = data
        self.listOfAccessRequestSpecification = ''
        self.listOfData = ''

    def toPdu(self):
        self.listOfAccessRequestSpecification = self.data['ListOfAccessRequestSpecification']['@Qty'][-2:] + AccessRequestSpecification.toPdu()
        self.listOfData =  self.data['ValueList']['@Qty'][-2:] + CosemData(path='//AccessRequestBody/ValueList//*').toPdu()
        return self.listOfAccessRequestSpecification + self.listOfData


class AccessRequestSpecification(object):

    @staticmethod
    def toPdu():
        pdu = ''
        rootTag = etree.fromstring(XmlPdu.XmlPduString)
        for elem in rootTag.xpath('//AccessRequestBody/ListOfAccessRequestSpecification/*'):
            if elem.tag == 'AccessRequestGet':

                pdu += '01' + elem.xpath('AttributeDescriptor/ClassId')[0].attrib['Value'] + \
                              elem.xpath('AttributeDescriptor/InstanceId')[0].attrib['Value'] + \
                              elem.xpath('AttributeDescriptor/AttributeId')[0].attrib['Value']

            if elem.tag == 'AccessRequestSet':
                pdu += '02' + elem.xpath('AttributeDescriptor/ClassId')[0].attrib['Value'] + \
                              elem.xpath('AttributeDescriptor/InstanceId')[0].attrib['Value'] + \
                              elem.xpath('AttributeDescriptor/AttributeId')[0].attrib['Value']

            if elem.tag == 'AccessRequestAction':
                pdu += '03' + elem.xpath('MethodDescriptor/ClassId')[0].attrib['Value'] + \
                              elem.xpath('MethodDescriptor/InstanceId')[0].attrib['Value'] + \
                              elem.xpath('MethodDescriptor/MethodId')[0].attrib['Value']

        return pdu


class AccessResponse(object):

    def __init__(self, data):
        self.data = data
        self.longInvokeIdAndPriority = ''
        self.dateTime = ''
        self.accessResponseBody = ''

    def toPdu(self):
        self.longInvokeIdAndPriority = self.data['LongInvokeIdAndPriority']['@Value']
        self.dateTime = self.data['OctetString']['@Value'].strip()
        if len(self.dateTime) > 0:
            self.dateTime = calcDataLength(self.dateTime) + self.dateTime
        else:
            self.dateTime = '00'
        self.accessResponseBody = AccessResponseBody(self.data['AccessResponseBody']).toPdu()

        return 'DA' + self.longInvokeIdAndPriority + self.dateTime + self.accessResponseBody


class AccessResponseBody(object):

    def __init__(self, data):
        self.data = data
        self.accessRequestSpecification = '00'
        self.accessResponseListOfData = ''
        self.accessResponseSpecification = ''

    def toPdu(self):
        self.accessResponseListOfData =  self.data['ListOfData']['@Qty'][-2:] + CosemData(path='//AccessResponseBody/ListOfData//*').toPdu()
        self.accessResponseSpecification = self.data['ListOfAccessResponseSpecification']['@Qty'][-2:] + AccessResponseSpecification.toPdu()
        return self.accessRequestSpecification + self.accessResponseListOfData + self.accessResponseSpecification


class AccessResponseSpecification(object):

    @staticmethod
    def toPdu():
        pdu = ''
        rootTag = etree.fromstring(XmlPdu.XmlPduString)
        for elem in rootTag.xpath('//AccessResponseBody/ListOfAccessResponseSpecification/AccessResponseSpecification/*'):
            if elem.tag == 'AccessResponseGet':
                pdu += '01' + dec_toHexStr(DataAccessResultMap[elem.xpath('Result')[0].attrib['Value'].lower()], 2)

            if elem.tag == 'AccessResponseSet':
                pdu += '02' + dec_toHexStr(DataAccessResultMap[elem.xpath('Result')[0].attrib['Value'].lower()], 2)

            if elem.tag == 'AccessResponseAction':
                pdu += '03' + dec_toHexStr(DataAccessResultMap[elem.xpath('Result')[0].attrib['Value'].lower()], 2)

        return pdu


class GeneralBlockTransfer(object):

    def __init__(self, data):
        self.data = data
        self.blockControl = ''
        self.blockNumber = ''
        self.blockNumberAck = ''
        self.blockData = ''

    def toPdu(self):
        self.blockControl = self.data['Unsigned']['@Value']
        self.blockNumber = self.data['LongUnsigned'][0]['@Value']
        self.blockNumberAck = self.data['LongUnsigned'][1]['@Value']
        self.blockData = calcDataLength(self.data['OctetString']['@Value']) + self.data['OctetString']['@Value']
        return 'E0' + self.blockControl + self.blockNumber + self.blockNumberAck + self.blockData

    def toXml(self):
        xmlBody = ['<GeneralBlockTransfer>']

        self.blockControl = self.data.pop()
        xmlBody.append(f'<Unsigned Value="{self.blockControl}" />')

        self.blockNumber = "".join([self.data.pop() for _ in range(2)])
        xmlBody.append(f'<LongUnsigned Value="{self.blockNumber}" />')

        self.blockNumberAck = "".join([self.data.pop() for _ in range(2)])
        xmlBody.append(f'<LongUnsigned Value="{self.blockNumberAck}" />')

        dataLen = self.data.pop()
        if dataLen == '83':
            dataLen = "".join([self.data.pop() for _ in range(3)])
        elif dataLen == '82':
            dataLen = "".join([self.data.pop() for _ in range(2)])
        elif dataLen == '81':
            dataLen = "".join([self.data.pop() for _ in range(1)])
        self.blockData = "".join([self.data.pop() for _ in range(int(dataLen, 16))])
        xmlBody.append(f'<OctetString Value="{self.blockData}" />')

        xmlBody.append('</GeneralBlockTransfer>')
        return formatXmlString("".join(xmlBody))


class ExceptionResponse(object):

    def __init__(self, data):
        self.data = data
        self.stateError = ''
        self.serviceError = ''

    def toPdu(self):
        self.stateError = dec_toHexStr(ExceptionStateErrorMap[self.data['StateError']['@Value'].lower()], 2)
        self.serviceError = dec_toHexStr(ExceptionServiceErrorMap[self.data['ServiceError']['@Value'].lower()], 2)
        return 'D8' + self.stateError + self.serviceError

    def toXml(self):
        xmlBody = ['<ExceptionResponse>']

        pduList = self.data

        self.stateError = getKeyByValue(ExceptionStateErrorMap, int(pduList.pop(), 16))[0]
        xmlBody.append(f'<StateError Value="{self.stateError}" />')

        self.serviceError = getKeyByValue(ExceptionServiceErrorMap, int(pduList.pop(), 16))[0]
        xmlBody.append(f'<ServiceError Value="{self.serviceError}" />')

        xmlBody.append('</ExceptionResponse>')

        return formatXmlString("".join(xmlBody))


class DataNotification(object):
    """
    <DataNotification>
        <LongInvokeIdAndPriority Value='00000001' />
        <OctetString Value='0C07E30A1E03050023FFFFC400'/>
        <Data>
            <Structure Qty="0001" >
                <Array Qty="0001" >
                    <Structure Qty="0026" >
                        <OctetString Value="07E30A1E03000000FFFFC400" />
                        <Unsigned Value="84" />
                        <DoubleLongUnsigned Value="00000008" />
                        <DoubleLongUnsigned Value="00000000" />
                        <DoubleLongUnsigned Value="00000000" />
                        <DoubleLongUnsigned Value="00000000" />
                    </Structure>
                </Array>
            </Structure>
        </Data>
    </DataNotification>
    """

    def __init__(self, data):
        self.data = data
        self.longInvokeIdAndPriority = ''
        self.dateTime = ''
        self.notificationBody = ''

    def toPdu(self):
        self.longInvokeIdAndPriority = self.data['LongInvokeIdAndPriority']['@Value']
        self.dateTime = self.data['OctetString']['@Value'].strip()
        if len(self.dateTime) == 0:
            self.dateTime = '00'
        self.notificationBody = CosemData(path='//Data//*').toPdu()

        return '0F' + self.longInvokeIdAndPriority + self.dateTime + self.notificationBody


class AARQ(object):

    def __init__(self, data):
        self.data = data
        self.protocolVersion = ''
        self.applicationContextName = ''            # A1
        self.callingApTitle = ''                    # A6
        self.senderAcseRequirements = ''            # 8A
        self.mechanismName = ''                     # 8B
        self.callingAuthenticationValue = ''        # AC
        self.userInformantion = ''                  # BE


    def toPdu(self):

        if self.data.get('ProtocolVersion'):
            self.protocolVersion = self.data['ProtocolVersion']['@Value']


        if self.data.get('ApplicationContextName'):
            applicationContextName = self.data['ApplicationContextName']['@Value']
            if applicationContextName.strip().upper() == 'LN':
                self.applicationContextName = 'A109060760857405080101'
            elif applicationContextName.strip().upper() == 'LNC':
                self.applicationContextName = 'A109060760857405080103'
            else:
                self.applicationContextName = 'A109060760857405000000'

        if self.data.get('CallingAPTitle'):
            callingApTitle = self.data['CallingAPTitle']['@Value']
            # A6 0A 04 08 4D4D4D0000BC614E
            self.callingApTitle = 'A6' + calcDataLength(callingApTitle + '0000') + '04' + calcDataLength(callingApTitle) + callingApTitle       # 用'0000'代表增加两个字节长度

        if self.data.get('SenderACSERequirements'):
            senderAcseRequirements = self.data['SenderACSERequirements']['@Value']
            if senderAcseRequirements == '0':
                self.senderAcseRequirements = '8A020700'
            elif senderAcseRequirements == '1':
                self.senderAcseRequirements = '8A020780'
            else:
                self.senderAcseRequirements = '8A020000'

        if self.data.get('MechanismName'):
            mechanismName = self.data['MechanismName']['@Value']
            if mechanismName == 'LOW_SECURITY':
                self.mechanismName = '8B07' + '60857405080201'
            elif mechanismName == 'HIGH_SECURITY':
                self.mechanismName = '8B07' + '60857405080202'
            elif mechanismName == 'HIGH_SECURITY_MD5':
                self.mechanismName = '8B07' + '60857405080203'
            elif mechanismName == 'HIGH_SECURITY_SHA1':
                self.mechanismName = '8B07' + '60857405080204'
            elif mechanismName == 'HIGH_SECURITY_GMAC':
                self.mechanismName = '8B07' + '60857405080205'
            elif mechanismName == 'HIGH_SECURITY_SHA256':
                self.mechanismName = '8B07' + '60857405080206'
            elif mechanismName == 'HIGH_SECURITY_ECDSA':
                self.mechanismName = '8B07' + '60857405080207'
            else:
                self.mechanismName = '8B07' + '60857405080000'

        if self.data.get('CallingAuthenticationValue'):
            callingAuthenticationValue = self.data['CallingAuthenticationValue']['@Value']
            self.callingAuthenticationValue = 'AC' + calcDataLength(callingAuthenticationValue + '0000') + '80' + calcDataLength(callingAuthenticationValue) + callingAuthenticationValue

        if self.data.get('CipheredInitiateRequest'):
            userInfo = self.data['CipheredInitiateRequest']['@Value']
            self.userInformantion = 'BE' + calcDataLength(userInfo + '0000') + '04' + calcDataLength(userInfo) + userInfo

        if self.data.get('InitiateRequest'):
            userInfo = InitiateRequest(self.data['InitiateRequest']).toPdu()
            self.userInformantion = 'BE' + calcDataLength(userInfo + '0000') + '04' + calcDataLength(userInfo) + userInfo


        totalLength = calcDataLength(self.applicationContextName + self.callingApTitle + self.senderAcseRequirements \
                                     + self.mechanismName + self.callingAuthenticationValue + self.userInformantion)

        return '60' + totalLength + self.applicationContextName + self.callingApTitle + self.senderAcseRequirements \
                    + self.mechanismName + self.callingAuthenticationValue + self.userInformantion


    def toXml(self):
        """
        PDU 数据结构
        60                                                                          --> Tag of `AARQ`
        5D                                                                          --> length of the AARQ's contents
        A1 09 06 07 60 85 74 05 08 01 03                                            --> Tag of `application-context-name`
        A6 0A 04 08 00 00 00 00 00 00 98 00                                         --> Tag of `calling-AP-title`
        8A 02 07 80                                                                 --> Tag of `acse-requirements`
        8B 07 60 85 74 05 08 02 06                                                  --> Tag of `mechanism-name`
        AC 12 80 10 1D 80 71 79 84 0B BB 7D 38 B3 8D 04 8B DB 90 06                 --> Tag of `calling-authentication-value`
        BE 23 04 21 21 1F 31 00 06 D5 F2 33 AA F1 87 CF 8C 58 C8 E2 74 78 BB B5 83 96 47 05 21 93 3A B5 F0 41 81 E3 B2      --> Tag of `user-information`
        """
        pduList = self.data
        pduList.pop()           # length of AARQ's contents

        while len(pduList) > 0:
            tag = pduList.pop()
            if tag == 'A1':         # application-context-name
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                applicationContextName = "".join([pduList.pop() for _ in range(int(length, 16))])
                if applicationContextName == '60857405080101':
                    self.applicationContextName = 'LN'
                if applicationContextName == '60857405080103':
                    self.applicationContextName = 'LNC'

            if tag == 'A6':         # calling-AP-title
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                self.callingApTitle = "".join([pduList.pop() for _ in range(int(length, 16))])

            if tag == '8A':         # acse-requirements
                pduList.pop() + pduList.pop()
                acseRequirement = pduList.pop()
                if acseRequirement == '00':
                    self.senderAcseRequirements = '0'
                else:
                    self.senderAcseRequirements = '1'

            if tag == '8B':         # mechanism-name
                length = pduList.pop()
                mechanismName = "".join([pduList.pop() for _ in range(int(length, 16))])
                if mechanismName == '60857405080201':
                    self.mechanismName = 'LOW_SECURITY'
                if mechanismName == '60857405080202':
                    self.mechanismName = 'HIGH_SECURITY'
                if mechanismName == '60857405080203':
                    self.mechanismName = 'HIGH_SECURITY_MD5'
                if mechanismName == '60857405080204':
                    self.mechanismName = 'HIGH_SECURITY_SHA1'
                if mechanismName == '60857405080205':
                    self.mechanismName = 'HIGH_SECURITY_GMAC'
                if mechanismName == '60857405080206':
                    self.mechanismName = 'HIGH_SECURITY_SHA256'
                if mechanismName == '60857405080207':
                    self.mechanismName = 'HIGH_SECURITY_ECDSA'

            if tag == 'AC':         # calling-authentication-value
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                self.callingAuthenticationValue = "".join([pduList.pop() for _ in range(int(length, 16))])

            if tag == 'BE':         # user-information
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                self.userInformantion = "".join([pduList.pop() for _ in range(int(length, 16))])

        xmlList = ['<AssociationRequest>']
        if self.applicationContextName:
            xmlList.append(f'<ApplicationContextName Value="{self.applicationContextName}"/>')
        if self.callingApTitle:
            xmlList.append(f'<CallingAPTitle Value="{self.callingApTitle}"/>')
        if self.senderAcseRequirements:
            xmlList.append(f'<SenderACSERequirements Value="{self.senderAcseRequirements}"/>')
        if self.mechanismName:
            xmlList.append(f'<MechanismName Value="{self.mechanismName}"/>')
        if self.callingAuthenticationValue:
            xmlList.append(f'<CallingAuthenticationValue Value="{self.callingAuthenticationValue}"/>')
        if self.userInformantion:
            if self.userInformantion.startswith('10'):       # 明文 InitiateRequest
                xmlList.extend(InitiateRequest(self.userInformantion).toXml(returnList=True))
            else:
                xmlList.append(f'<CipheredInitiateRequest Value="{self.userInformantion}"/>')
        xmlList.append('</AssociationRequest>')

        return formatXmlString("".join(xmlList))


class AARE(object):

    def __init__(self, data):
        self.data = data
        self.applicationContextName = ''            # A1
        self.result = ''                            # A2
        self.resultSourceDiagnostic = ''            # A3
        self.respondingApTitle  = ''                # A4
        self.responderAcseRequirements = ''         # 88
        self.mechanismName = ''                     # 89
        self.respondingAuthenticationValue = ''     # AA
        self.userInformantion = ''                  # BE


    def toPdu(self):

        if self.data.get('ApplicationContextName'):
            applicationContextName = self.data['ApplicationContextName']['@Value']
            if applicationContextName.strip().upper() == 'LN':
                self.applicationContextName = 'A109060760857405080101'
            if applicationContextName.strip().upper() == 'LNC':
                self.applicationContextName = 'A109060760857405080103'

        if self.data.get('AssociationResult'):
            self.result = 'A2030201' + self.data['AssociationResult']['@Value']

        if self.data.get('ResultSourceDiagnostic'):
            self.resultSourceDiagnostic = 'A305A1030201' + self.data['ResultSourceDiagnostic']['AcseServiceUser']['@Value']

        if self.data.get('RespondingAPTitle'):
            respondingApTitle = self.data['RespondingAPTitle']['@Value']
            self.respondingApTitle = 'A4' + calcDataLength(respondingApTitle + '0000') + '04' + calcDataLength(respondingApTitle) + respondingApTitle       # 用'0000'代表增加两个字节长度

        if self.data.get('ResponderACSERequirement'):
            responderAcseRequirements = self.data['ResponderACSERequirement']['@Value']
            if responderAcseRequirements == '0':
                self.responderAcseRequirements = '88020700'
            if responderAcseRequirements == '1':
                self.responderAcseRequirements = '88020780'

        if self.data.get('MechanismName'):
            mechanismName = self.data['MechanismName']['@Value']
            if mechanismName == 'LOW_SECURITY':
                self.mechanismName = '8907' + '60857405080201'
            if mechanismName == 'HIGH_SECURITY':
                self.mechanismName = '8907' + '60857405080202'
            if mechanismName == 'HIGH_SECURITY_MD5':
                self.mechanismName = '8907' + '60857405080203'
            if mechanismName == 'HIGH_SECURITY_SHA1':
                self.mechanismName = '8907' + '60857405080204'
            if mechanismName == 'HIGH_SECURITY_GMAC':
                self.mechanismName = '8907' + '60857405080205'
            if mechanismName == 'HIGH_SECURITY_SHA256':
                self.mechanismName = '8907' + '60857405080206'
            if mechanismName == 'HIGH_SECURITY_ECDSA':
                self.mechanismName = '8907' + '60857405080207'

        if self.data.get('RespondingAuthenticationValue'):
            respondingAuthenticationValue = self.data['RespondingAuthenticationValue']['@Value']
            self.respondingAuthenticationValue = 'AA' + calcDataLength(respondingAuthenticationValue + '0000') + '80' + calcDataLength(respondingAuthenticationValue) + respondingAuthenticationValue

        if self.data.get('CipheredInitiateResponse'):
            userInfo = self.data['CipheredInitiateResponse']['@Value']
            self.userInformantion = 'BE' + calcDataLength(userInfo + '0000') + '04' + calcDataLength(userInfo) + userInfo

        totalLength = calcDataLength(self.applicationContextName + self.result + self.resultSourceDiagnostic \
                                     + self.respondingApTitle + self.responderAcseRequirements + self.mechanismName \
                                     + self.respondingAuthenticationValue + self.userInformantion)

        return '61' + totalLength + self.applicationContextName + self.result + self.resultSourceDiagnostic \
                                     + self.respondingApTitle + self.responderAcseRequirements + self.mechanismName \
                                     + self.respondingAuthenticationValue + self.userInformantion


    def toXml(self):
        """
        PDU 数据结构
        61                                                                  # Tag of `AARE`
        69                                                                  # length of the AARE's content
        A1 09 06 07 60 85 74 05 08 01 03                                    # Tag of `application-context-name`
        A2 03 02 01 00                                                      # Tag of `association-result`
        A3 05 A1 03 02 01 0E                                                # Tag of `result-source-diagnostic`
        A4 0A 04 08 4B 46 4D 10 10 00 00 0D                                 # Tag of `responding-AP-title`
        88 02 07 80                                                         # Tag of `acse-requirements`
        89 07 60 85 74 05 08 02 06                                          # Tag of `mechanism-name`
        AA 12 80 10 1E 2D E7 F1 25 24 57 4F 79 65 E9 0D 02 87 D7 69         # Tag of `responding-authentication-value`
        BE 23 04 21 28 1F 31 00 00 01 BE 89 A4 98 BC 31 1F 28 FF 29 CD D6 93 0E DC AA EC 7B F5 B9 DB C4 52 86 A3 33 77      # Tag of `user-info`
        """
        pduList = self.data
        pduList.pop()           # length of AARE's contents

        while len(pduList) > 0:
            tag = pduList.pop()
            if tag == 'A1':                             # application-context-name
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                applicationContextName = "".join([pduList.pop() for _ in range(int(length, 16))])
                if applicationContextName == '60857405080101':
                    self.applicationContextName = 'LN'
                if applicationContextName == '60857405080103':
                    self.applicationContextName = 'LNC'


            if tag == 'A2':                             # association-result
                pduList.pop() + pduList.pop() + pduList.pop()
                self.result = pduList.pop()

            if tag == 'A3':                             # result-source-diagnostic
                pduList.pop() + pduList.pop() + pduList.pop() + pduList.pop() + pduList.pop()
                self.resultSourceDiagnostic = pduList.pop()

            if tag == 'A4':                             # responding-AP-title
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                self.respondingApTitle = "".join([pduList.pop() for _ in range(int(length, 16))])

            if tag == '88':                             # acse-requirements
                pduList.pop() + pduList.pop()
                acseRequirements = pduList.pop()
                if acseRequirements == '80':
                    self.responderAcseRequirements = '1'
                if acseRequirements == '00':
                    self.responderAcseRequirements = '0'

            if tag == '89':                             # mechanism-name
                length = pduList.pop()
                mechanismName = "".join([pduList.pop() for _ in range(int(length, 16))])
                if mechanismName == '60857405080201':
                    self.mechanismName = 'LOW_SECURITY'
                if mechanismName == '60857405080202':
                    self.mechanismName = 'HIGH_SECURITY'
                if mechanismName == '60857405080203':
                    self.mechanismName = 'HIGH_SECURITY_MD5'
                if mechanismName == '60857405080204':
                    self.mechanismName = 'HIGH_SECURITY_SHA1'
                if mechanismName == '60857405080205':
                    self.mechanismName = 'HIGH_SECURITY_GMAC'
                if mechanismName == '60857405080206':
                    self.mechanismName = 'HIGH_SECURITY_SHA256'
                if mechanismName == '60857405080207':
                    self.mechanismName = 'HIGH_SECURITY_ECDSA'

            if tag == 'AA':                             # responding-authentication-value
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                self.respondingAuthenticationValue = "".join([pduList.pop() for _ in range(int(length, 16))])

            if tag == 'BE':         # user-information
                pduList.pop() + pduList.pop()
                length = pduList.pop()
                self.userInformantion = "".join([pduList.pop() for _ in range(int(length, 16))])

        xmlList = ['<AssociationResponse>']
        if self.applicationContextName:
            xmlList.append(f'<ApplicationContextName Value="{self.applicationContextName}"/>')
        if self.result:
            xmlList.append(f'<AssociationResult Value="{self.result}"/>')
        if self.resultSourceDiagnostic:
            xmlList.append(f'<ResultSourceDiagnostic><AcseServiceUser Value="{self.resultSourceDiagnostic}"/></ResultSourceDiagnostic>')
        if self.respondingApTitle:
            xmlList.append(f'<RespondingAPTitle Value="{self.respondingApTitle}"/>')
        if self.responderAcseRequirements:
            xmlList.append(f'<ResponderAcseRequirements Value="{self.responderAcseRequirements}"/>')
        if self.mechanismName:
            xmlList.append(f'<MechanismName Value="{self.mechanismName}"/>')
        if self.respondingAuthenticationValue:
            xmlList.append(f'<RespondingAuthenticationValue Value="{self.respondingAuthenticationValue}"/>')
        if self.userInformantion:
            if self.userInformantion.startswith('0E'):
                xmlList.extend(ConfirmedServiceError(splitWithSpace(self.userInformantion[2:])).toXml(returnList=True))
            elif self.applicationContextName == 'LN':
                xmlList.extend(InitiateResponse(splitWithSpace(self.userInformantion[2:])).toXml(returnList=True))
            else:
                xmlList.append(f'<CipheredInitiateRequest Value="{self.userInformantion}"/>')
        xmlList.append('</AssociationResponse>')

        return formatXmlString("".join(xmlList))


class InitiateRequest(object):
    # Table 118 – A-XDR encoding of the xDLMS InitiateRequest APDU

    def __init__(self, data):
        self.data = data
        self.dedicatedKey = '00'
        self.responseAllowed = '00'
        self.proposedQualityOfService = '00'                # not used in DLMS/COSEM
        self.proposedDlmsVersionNumber = '06'
        self.proposedConformance = ''
        self.clientMaxReceivePduSize = '04B0'               # client-max-receive-pdu-size: 1200 = 0x04B0

    def toPdu(self):
        if self.data.get('DedicatedKey'):
            dedicatedKey = self.data['DedicatedKey']['@Value']
            self.dedicatedKey = '01' + calcDataLength(dedicatedKey) + dedicatedKey

        if self.data.get('ResponseAllowed'):
            self.responseAllowed = self.data['ResponseAllowed']['@Value']

        if self.data.get('ProposedQualityOfService'):
            self.proposedQualityOfService = self.data['ProposedQualityOfService']['@Value']

        if self.data.get('ProposedDlmsVersionNumber'):
            self.proposedDlmsVersionNumber = self.data['ProposedDlmsVersionNumber']['@Value']

        if self.data.get('ProposedConformance'):
            conformanceList = ['0'] * 24
            conformances = self.data['ProposedConformance']['ConformanceBit']
            for conformance in conformances:
                conformanceList[ConformanceMap[conformance['@Name'].lower()]] = '1'
            self.proposedConformance = '5F1F0400' + format(int("".join(conformanceList), 2), 'x').rjust(6, '0').upper()

        if self.data.get('ProposedMaxPduSize'):
            self.clientMaxReceivePduSize = self.data['ProposedMaxPduSize']['@Value']

        return '01' + self.dedicatedKey + self.responseAllowed + self.proposedQualityOfService + \
               self.proposedDlmsVersionNumber + self.proposedConformance + self.clientMaxReceivePduSize

    def toXml(self, returnList=False):
        """
        PDU 数据结构
        01                                          # Tag of `InitiateRequest`
        00                                          # Tag of `dedicate-key`
        00                                          # Tag of `response-allowed`
        00                                          # Tag of `proposedQualityOfService`
        06                                          # Tag of `proposed-dlms-version-number`
        5F1F04 00601F1                              # Tag of `proposed-conformance`
        FFFFD                                       # Tag of `client-max-receive-pdu-size`
        """
        pduList = self.data

        value = pduList.pop()                               # dedicate-key  -- OCTET STRING OPTIONAL
        if value == '01':
            length = pduList.pop()
            self.dedicatedKey = "".join([pduList.pop() for _ in range(int(length, 16))])
        else:
            self.dedicatedKey = '00'

        self.responseAllowed = pduList.pop()                # response-allowed  -- BOOLEAN DEFAULT TRUE
        self.proposedQualityOfService = pduList.pop()       # proposedQualityOfService  -- Integer8 OPTIONAL
        self.proposedDlmsVersionNumber = pduList.pop()      # proposed-dlms-version-number  -- Unsigned8

        pduList.pop() + pduList.pop() + pduList.pop() + pduList.pop()
        proposedConformance = "".join([pduList.pop() for _ in range(3)])
        proposedConformanceBitString =  format(int(proposedConformance, 16), 'b').rjust(24, '0')
        conformanceList = list()
        for index, value in enumerate(proposedConformanceBitString):
            if value == '1':
                conformanceList.append(ConformanceReversedMap[index])

        self.clientMaxReceivePduSize = "".join([pduList.pop() for _ in range(2)])       # Unsigned16

        xmlList = ['<InitiateRequest>']
        if self.dedicatedKey != '00':
            xmlList.append(f'<DedicatedKey  Value="{self.dedicatedKey}"/>')
        if self.responseAllowed != '00':
            xmlList.append(f'<ResponseAllowed Value="{self.responseAllowed}"/>')
        if self.proposedQualityOfService != '00':
            xmlList.append(f'<ProposedQualityOfService Value="{self.proposedQualityOfService}"/')

        xmlList.append(f'<ProposedDlmsVersionNumber Value="{self.proposedDlmsVersionNumber}"/>')
        xmlList.append('<ProposedConformance>')
        for conformance in conformanceList:
            xmlList.append(f'<ConformanceBit Name="{conformance}" />')
        xmlList.append('</ProposedConformance>')
        xmlList.append(f'<ProposedMaxPduSize Value="{self.clientMaxReceivePduSize}"/>')
        xmlList.append('</InitiateRequest>')

        if returnList:
            return xmlList
        return formatXmlString("".join(xmlList))


class InitiateResponse(object):

    def __init__(self, data):
        self.data = data
        self.negotiatedQualityOfService = ''                # not used in DLMS/COSEM
        self.negotiatedDlmsVersionNumber = ''
        self.negotiatedConformance = ''
        self.serverMaxReceivePduSize = ''
        self.vaaName = ''                                   # In the case of LN referencing, the value of the vaa-name is 0x0007


    def toPdu(self):

        if self.data.get('NegotiatedQualityOfService'):
            self.negotiatedQualityOfService = self.data['NegotiatedQualityOfService']['@Value']
        else:
            self.negotiatedQualityOfService = '00'

        self.negotiatedDlmsVersionNumber = self.data['NegotiatedDlmsVersionNumber']['@Value']

        conformanceList = ['0'] * 24
        conformances = self.data['NegotiatedConformance']['ConformanceBit']
        for conformance in conformances:
            conformanceList[ConformanceMap[conformance['@Name'].lower()]] = '1'
        self.negotiatedConformance = '5F1F0400' + format(int("".join(conformanceList), 2), 'x').rjust(6, '0').upper()

        self.serverMaxReceivePduSize = self.data['NegotiatedMaxPduSize']['@Value']
        self.vaaName = self.data['VaaName']['@Value']

        return '08' + self.negotiatedQualityOfService + self.negotiatedDlmsVersionNumber + self.negotiatedConformance \
                    + self.serverMaxReceivePduSize + self.vaaName


    def toXml(self, returnList=False):
        """
        PDU 数据结构

        08                              # Tag of `InitiateResponse`
        00                              # Tag of `negotiated-quality-of-service`
        06                              # Tag of `negotiated-dlms-version-number`
        5F1F0400 007C1F                 # Tag of `negotiated-conformance`
        0400                            # Tag of `server-max-receive-pdu-size`
        0007                            # Tag of `VAA-Name`
        """
        self.negotiatedQualityOfService = self.data.pop()                 # Integer8 OPTIONAL
        self.negotiatedDlmsVersionNumber = self.data.pop()                # Unsigned8

        self.data.pop() + self.data.pop() + self.data.pop() + self.data.pop()
        proposedConformance = "".join([self.data.pop() for _ in range(3)])
        proposedConformanceBitString =  format(int(proposedConformance, 16), 'b').rjust(24, '0')
        conformanceList = list()
        for index, value in enumerate(proposedConformanceBitString):
            if value == '1':
                conformanceList.append(ConformanceReversedMap[index])

        self.serverMaxReceivePduSize = "".join([self.data.pop() for _ in range(2)])       # Unsigned16

        length = len(self.data)
        self.vaaName = "".join([self.data.pop() for _ in range(length)])

        xmlList = ['<InitiateResponse>']
        if self.negotiatedQualityOfService != '00':
            xmlList.append(f'<NegotiatedQualityOfService  Value="{self.negotiatedQualityOfService}"/>')

        xmlList.append(f'<NegotiatedDlmsVersionNumber Value="{self.negotiatedDlmsVersionNumber}"/>')

        xmlList.append('<ProposedConformance>')
        for conformance in conformanceList:
            xmlList.append(f'<ConformanceBit Name="{conformance}" />')
        xmlList.append('</ProposedConformance>')
        xmlList.append(f'<NegotiatedMaxPduSize Value="{self.serverMaxReceivePduSize}"/>')
        xmlList.append(f'<VaaName Value="{self.vaaName}"/>')
        xmlList.append('</InitiateResponse>')

        if returnList:
            return xmlList
        return formatXmlString("".join(xmlList))


class RlrqApdu(object):

    def __init__(self, data):
        self.data = data
        self.reason = ''
        self.userInfo = ''

    def toPdu(self):
        if self.data.get('reason'):
            self.reason = '8001' + self.data['reason']['@Value']

        if self.data.get('userInformation'):
            userinfo = self.data['userInformation']['@Value']
            userinfo = '04' + calcDataLength(userinfo) + userinfo
            self.userInfo = 'BE' + calcDataLength(userinfo) + userinfo

        return '62' + calcDataLength(self.reason + self.userInfo) + self.reason + self.userInfo


    def toXml(self, returnList=False):

        self.data.pop()                                     # RLRQ length
        while len(self.data) > 0:
            tag = self.data.pop()
            if tag == '80':
                length = self.data.pop()
                self.reason = "".join([self.data.pop() for _ in range(int(length, 16))])

            if tag == 'BE':
                value = self.data.pop()                         # encoding of the length of the tagged component's value field
                if value == '83':
                    [self.data.pop() for _ in range(3)]
                if value == '82':
                    [self.data.pop() for _ in range(2)]
                if value == '81':
                    [self.data.pop() for _ in range(1)]

                self.data.pop()                                 # encoding of the choice for user-information

                userInfoLen = self.data.pop()
                self.userInfo = "".join([self.data.pop() for _ in range(int(userInfoLen, 16))])

        xmlBody = ["<RLRQ-apdu>"]
        if self.reason:
            xmlBody.append(f'<reason Value="{self.reason}" />')
        if self.userInfo:
            xmlBody.append(f'<userInformation Value="{self.userInfo}" />')
        xmlBody.append('</RLRQ-apdu>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class RlreApdu(object):

    def __init__(self, data):
        self.data = data
        self.reason = ''
        self.userInfo = ''

    def toPdu(self):
        if self.data.get('reason'):
            self.reason = '8001' + self.data['reason']['@Value']

        if self.data.get('userInformation'):
            userinfo = self.data['userInformation']['@Value']
            userinfo = '04' + calcDataLength(userinfo) + userinfo
            self.userInfo = 'BE' + calcDataLength(userinfo) + userinfo

        return '63' + calcDataLength(self.reason + self.userInfo) + self.reason + self.userInfo


    def toXml(self, returnList=False):

        self.data.pop()                                     # RLRE length
        while len(self.data) > 0:
            tag = self.data.pop()
            if tag == '80':
                length = self.data.pop()
                self.reason = "".join([self.data.pop() for _ in range(int(length, 16))])

            if tag == 'BE':
                value = self.data.pop()                         # encoding of the length of the tagged component's value field
                if value == '83':
                    [self.data.pop() for _ in range(3)]
                if value == '82':
                    [self.data.pop() for _ in range(2)]
                if value == '81':
                    [self.data.pop() for _ in range(1)]

                self.data.pop()                                 # encoding of the choice for user-information

                userInfoLen = self.data.pop()
                self.userInfo = "".join([self.data.pop() for _ in range(int(userInfoLen, 16))])

        xmlBody = ["<RLRE-apdu>"]
        if self.reason:
            xmlBody.append(f'<reason Value="{self.reason}" />')
        if self.userInfo:
            xmlBody.append(f'<userInformation Value="{self.userInfo}" />')
        xmlBody.append('</RLRE-apdu>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))



class ConfirmedServiceError(object):

    def __init__(self, data):
        self.data = data


    def toXml(self, returnList=False):

        xmlBody = ['<ConfirmedServiceError>']

        confirmedService = ConfirmedServiceErrorMap[int(self.data.pop(), 16)]
        xmlBody.append(f'<{confirmedService}>')

        serviceErrorTag = ServiceErrorMap[int(self.data.pop(), 16)]
        serviceErrorValue = globals()['ServiceError_' + serviceErrorTag][int(self.data.pop(), 16)]
        xmlBody.append(f'<{serviceErrorTag} Value="{serviceErrorValue}" />')

        xmlBody.append(f'</{confirmedService}>')
        xmlBody.append('</ConfirmedServiceError>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


class EventNotificationRequest(object):

    def __init__(self, data):
        self.data = data
        self.time = ''
        self.cosemAttributeDescriptor = ''
        self.attributeValue = ''


    def toPdu(self):
        if self.data is None or len(self.data) == 0:
            return ''

        try:
            self.time = '01' + calcDataLength(self.data['Time']['@Value']) + self.data['Time']['@Value']
        except KeyError:
            self.time = '00'
        self.cosemAttributeDescriptor = CosemAttributeDescriptor(self.data['AttributeDescriptor']).toPdu()
        self.attributeValue = CosemData(path='//EventNotificationRequest/AttributeValue//*').toPdu()

        return 'C2' + self.time + self.cosemAttributeDescriptor + self.attributeValue


    def toXml(self, returnList=False):

        xmlBody = ['<EventNotificationRequest>']

        hasTime = self.data.pop()
        if hasTime == '01':
            timeLen = self.data.pop()
            self.time = "".join(self.data.pop() for _ in range(int(timeLen, 16)))
        # time
        xmlBody.append(f'<Time Value="{self.time}" />')
        # cosem-attribute-descriptor
        xmlBody.extend(CosemAttributeDescriptor(self.data).toXml(returnList=True))
        # attribute-value
        xmlBody.append('<AttributeValue>')
        xmlBody.extend(CosemDataReversed(self.data).toXml(returnList=True))
        xmlBody.append('</AttributeValue>')

        xmlBody.append('</EventNotificationRequest>')

        if returnList:
            return xmlBody
        return formatXmlString("".join(xmlBody))


if __name__ == '__main__':

    # dat = 'C101C1000B00000B0000FF0200018201A402031200001AFFFF0101FF110002031200011AFFFF0A01FF110102031200021AFFFF03FEFF110202031200031AFFFF04FD07110302031200041AFFFF051007110402031200051AFFFFFF02FF110502031200061AFFFFFF03FF110602031200071AFFFF0604FF110702031200081AFFFF021CFF110002031200091AFFFF0701FF1101020312000A1AFFFF071FFF1102020312000B1AFFFF0801FF1103020312000C1AFFFF081FFF1104020312000D1AFFFF09FD011105020312000E1AFFFF0901011106020312000F1AFFFF0A0FFF110702031200101AFFFF0B01FF110002031200111AFFFF0B02FF110102031200121AFFFF0C01FF110202031200131AFFFF0C19FF110302031200141A07E30202FF110402031200151A07E30203FF110502031200161A07E30204FF110602031200171A07E30205FF110702031200181A07E30206FF110002031200191A07E30207FF1101020312001A1A07E30208FF1102020312001B1A07E30209FF1103020312001C1A07E3020AFF1104020312001D1A07E3020BFF1105020312001E1A07E3020CFF1106020312001F1A07E3020DFF110702031200201A07E3020EFF110002031200211A07E3020FFF110102031200221A07E30210FF110202031200231A07E30211FF110302031200241A07E30212FF110402031200251A07E30213FF110502031200261A07E30214FF110602031200271A07E30215FF110702031200281A07E40301FF110002031200291A07E40302FF1101020312002A1A07E40303FF1102020312002B1A07E40304FF1103020312002C1A07E40305FF1104020312002D1A07E40306FF1105020312002E1A07E40307FF1106020312002F1A07E40308FF110702031200301A07E40309FF110002031200311A07E4030AFF110102031200321A07E4030BFF110202031200331A07E4030CFF110302031200341A07E4030DFF110402031200351A07E4030EFF110502031200361A07E4030FFF110602031200371A07E40310FF110702031200381A07E40311FF110002031200391A07E40312FF1101020312003A1A07E40313FF1102020312003B1A07E40314FF1103020312003C1A07E50401FF1104020312003D1A07E50402FF1105020312003E1A07E50403FF1106020312003F1A07E50404FF110702031200401A07E50405FF110002031200411A07E50406FF110102031200421A07E50407FF110202031200431A07E50408FF110302031200441A07E50409FF110402031200451A07E5040AFF110502031200461A07E5040BFF110602031200471A07E5040CFF110702031200481A07E5040DFF110002031200491A07E5040EFF1101020312004A1A07E5040FFF1102020312004B1A07E50410FF1103020312004C1A07E50411FF1104020312004D1A07E50412FF1105020312004E1A07E50413FF1106020312004F1A07E50414FF110702031200501A07E60606FF110002031200511A07E60607FF110102031200521A07E60608FF110202031200531A07E60609FF110302031200541A07E6060AFF110402031200551A07E6060BFF110502031200561A07E6060CFF110602031200571A07E6060DFF110702031200581A07E6060EFF110002031200591A07E6060FFF1101020312005A1A07E60610FF1102020312005B1A07E60611FF1103020312005C1A07E60612FF1104020312005D1A07E60613FF1105020312005E1A07E60614FF1106020312005F1A07E60615FF110702031200601A07E60616FF110002031200611A07E60617FF110102031200621A07E60618FF110202031200631A07E60619FF110302031200641A07E70705FF110402031200651A07E70706FF110502031200661A07E70707FF110602031200671A07E70708FF110702031200681A07E70709FF110002031200691A07E7070AFF1101020312006A1A07E7070BFF1102020312006B1A07E7070CFF1103020312006C1A07E7070DFF1104020312006D1A07E7070EFF1105020312006E1A07E7070FFF1106020312006F1A07E70710FF110702031200701A07E70711FF110002031200711A07E70712FF110102031200721A07E70713FF110202031200731A07E70714FF110302031200741A07E70715FF110402031200751A07E70716FF110502031200761A07E70717FF110602031200771A07E70718FF110702031200781A07E80804FF110002031200791A07E80805FF1101020312007A1A07E80806FF1102020312007B1A07E80807FF1103020312007C1A07E80808FF1104020312007D1A07E80809FF1105020312007E1A07E8080AFF1106020312007F1A07E8080BFF110702031200801A07E8080CFF110002031200811A07E8080DFF110102031200821A07E8080EFF110202031200831A07E8080FFF110302031200841A07E80810FF110402031200851A07E80811FF110502031200861A07E80812FF110602031200871A07E80813FF110702031200881A07E80814FF110002031200891A07E80815FF1101020312008A1A07E80816FF1102020312008B1A07E80817FF1103020312008C1A07E90B05FF1104020312008D1A07E90B06FF1105020312008E1A07E90B07FF1106020312008F1A07E90B08FF110702031200901A07E90B09FF110002031200911A07E90B0AFF110102031200921A07E90B0BFF110202031200931A07E90B0CFF110302031200941A07E90B0DFF110402031200951A07E90B0EFF110502031200961A07E90B0FFF110602031200971A07E90B10FF110702031200981A07E90B11FF110002031200991A07E90B12FF1101020312009A1A07E90B13FF1102020312009B1A07E90B14FF1103020312009C1A07E90B15FF1104020312009D1A07E90B16FF1105020312009E1A07E90B17FF1106020312009F1A07E90B18FF110702031200A01A07EA0607FF110002031200A11A07EA0608FF110102031200A21A07EA0609FF110202031200A31A07EA060AFF110302031200A41A07EA060BFF110402031200A51A07EA060CFF110502031200A61A07EA060DFF110602031200A71A07EA060EFF110702031200A81A07EA060FFF110002031200A91A07EA0610FF110102031200AA1A07EA0611FF110202031200AB1A07EA0612FF110302031200AC1A07EA0613FF110402031200AD1A07EA0614FF110502031200AE1A07EA0615FF110602031200AF1A07EA0616FF110702031200B01A07EA0617FF110002031200B11A07EA0618FF110102031200B21A07EA0619FF110202031200B31A07EA061AFF110302031200B41A07EB0703FF110402031200B51A07EB0704FF110502031200B61A07EB0705FF110602031200B71A07EB0706FF110702031200B81A07EB0707FF110002031200B91A07EB0708FF110102031200BA1A07EB0709FF110202031200BB1A07EB070AFF110302031200BC1A07EB070BFF110402031200BD1A07EB070CFF110502031200BE1A07EB070DFF110602031200BF1A07EB070EFF110702031200C01A07EB070FFF110002031200C11A07EB0710FF110102031200C21A07EB0711FF110202031200C31A07EB0712FF110302031200C41A07EB0713FF110402031200C51A07EB0714FF110502031200C61A07EB0715FF110602031200C71A07EB0716FF110702031200C81A07EC0806FF110002031200C91A07EC0807FF110102031200CA1A07EC0808FF110202031200CB1A07EC0809FF110302031200CC1A07EC080AFF110402031200CD1A07EC080BFF110502031200CE1A07EC080CFF110602031200CF1A07EC080DFF110702031200D01A07EC080EFF110002031200D11A07EC080FFF110102031200D21A07EC0810FF110202031200D31A07EC0811FF110302031200D41A07EC0812FF110402031200D51A07EC0813FF110502031200D61A07EC0814FF110602031200D71A07EC0815FF110702031200D81A07EC0816FF110002031200D91A07EC0817FF110102031200DA1A07EC0818FF110202031200DB1A07EC0819FF110302031200DC1A07ED0B05FF110402031200DD1A07ED0B06FF110502031200DE1A07ED0B07FF110602031200DF1A07ED0B08FF110702031200E01A07ED0B09FF110002031200E11A07ED0B0AFF110102031200E21A07ED0B0BFF110202031200E31A07ED0B0CFF110302031200E41A07ED0B0DFF110402031200E51A07ED0B0EFF110502031200E61A07ED0B0FFF110602031200E71A07ED0B10FF110702031200E81A07ED0B11FF110002031200E91A07ED0B12FF110102031200EA1A07ED0B13FF110202031200EB1A07ED0B14FF110302031200EC1A07ED0B15FF110402031200ED1A07ED0B16FF110502031200EE1A07ED0B17FF110602031200EF1A07ED0B18FF110702031200F01A07EE0606FF110002031200F11A07EE0607FF110102031200F21A07EE0608FF110202031200F31A07EE0609FF110302031200F41A07EE060AFF110402031200F51A07EE060BFF110502031200F61A07EE060CFF110602031200F71A07EE060DFF110702031200F81A07EE060EFF110002031200F91A07EE060FFF110102031200FA1A07EE0610FF110202031200FB1A07EE0611FF110302031200FC1A07EE0612FF110402031200FD1A07EE0613FF110502031200FE1A07EE0614FF110602031200FF1A07EE0615FF110702031201001A07EE0616FF110002031201011A07EE0617FF110102031201021A07EE0618FF110202031201031A07EE0619FF110302031201041A07EF0705FF110402031201051A07EF0706FF110502031201061A07EF0707FF110602031201071A07EF0708FF110702031201081A07EF0709FF110002031201091A07EF070AFF1101020312010A1A07EF070BFF1102020312010B1A07EF070CFF1103020312010C1A07EF070DFF1104020312010D1A07EF070EFF1105020312010E1A07EF070FFF1106020312010F1A07EF0710FF110702031201101A07EF0711FF110002031201111A07EF0712FF110102031201121A07EF0713FF110202031201131A07EF0714FF110302031201141A07EF0715FF110402031201151A07EF0716FF110502031201161A07EF0717FF110602031201171A07EF0718FF110702031201181A07F00805FF110002031201191A07F00806FF1101020312011A1A07F00807FF1102020312011B1A07F00808FF1103020312011C1A07F00809FF1104020312011D1A07F0080AFF1105020312011E1A07F0080BFF1106020312011F1A07F0080CFF110702031201201A07F0080DFF110002031201211A07F0080EFF110102031201221A07F0080FFF110202031201231A07F00810FF110302031201241A07F00811FF110402031201251A07F00812FF110502031201261A07F00813FF110602031201271A07F00814FF110702031201281A07F00815FF110002031201291A07F00816FF1101020312012A1A07F00817FF1102020312012B1A07F00818FF1103020312012C1A07F10B04FF1104020312012D1A07F10B05FF1105020312012E1A07F10B06FF1106020312012F1A07F10B07FF110702031201301A07F10B08FF110002031201311A07F10B09FF110102031201321A07F10B0AFF110202031201331A07F10B0BFF110302031201341A07F10B0CFF110402031201351A07F10B0DFF110502031201361A07F10B0EFF110602031201371A07F10B0FFF110702031201381A07F10B10FF110002031201391A07F10B11FF1101020312013A1A07F10B12FF1102020312013B1A07F10B13FF1103020312013C1A07F10B14FF1104020312013D1A07F10B15FF1105020312013E1A07F10B16FF1106020312013F1A07F10B17FF110702031201401A07F20605FF110002031201411A07F20606FF110102031201421A07F20607FF110202031201431A07F20608FF110302031201441A07F20609FF110402031201451A07F2060AFF110502031201461A07F2060BFF110602031201471A07F2060CFF110702031201481A07F2060DFF110002031201491A07F2060EFF1101020312014A1A07F2060FFF1102020312014B1A07F20610FF1103020312014C1A07F20611FF1104020312014D1A07F20612FF1105020312014E1A07F20613FF1106020312014F1A07F20614FF110702031201501A07F20615FF110002031201511A07F20616FF110102031201521A07F20617FF110202031201531A07F20618FF110302031201541A07F30707FF110402031201551A07F30708FF110502031201561A07F30709FF110602031201571A07F3070AFF110702031201581A07F3070BFF110002031201591A07F3070CFF1101020312015A1A07F3070DFF1102020312015B1A07F3070EFF1103020312015C1A07F3070FFF1104020312015D1A07F30710FF1105020312015E1A07F30711FF1106020312015F1A07F30712FF110702031201601A07F30713FF110002031201611A07F30714FF110102031201621A07F30715FF110202031201631A07F30716FF110302031201641A07F30717FF110402031201651A07F30718FF110502031201661A07F30719FF110602031201671A07F3071AFF110702031201681A07F40808FF110002031201691A07F40809FF1101020312016A1A07F4080AFF1102020312016B1A07F4080BFF1103020312016C1A07F4080CFF1104020312016D1A07F4080DFF1105020312016E1A07F4080EFF1106020312016F1A07F4080FFF110702031201701A07F40810FF110002031201711A07F40811FF110102031201721A07F40812FF110202031201731A07F40813FF110302031201741A07F40814FF110402031201751A07F40815FF110502031201761A07F40816FF110602031201771A07F40817FF110702031201781A07F40818FF110002031201791A07F40819FF1101020312017A1A07F4081AFF1102020312017B1A07F4081BFF1103020312017C1A07F50B05FF1104020312017D1A07F50B06FF1105020312017E1A07F50B07FF1106020312017F1A07F50B08FF110702031201801A07F50B09FF110002031201811A07F50B0AFF110102031201821A07F50B0BFF110202031201831A07F50B0CFF110302031201841A07F50B0DFF110402031201851A07F50B0EFF110502031201861A07F50B0FFF110602031201871A07F50B10FF110702031201881A07F50B11FF110002031201891A07F50B12FF1101020312018A1A07F50B13FF1102020312018B1A07F50B14FF1103020312018C1A07F50B15FF1104020312018D1A07F50B16FF1105020312018E1A07F50B17FF1106020312018F1A07F50B18FF110702031201901A07F60605FF110002031201911A07F60606FF110102031201921A07F60607FF110202031201931A07F60608FF110302031201941A07F60609FF110402031201951A07F6060AFF110502031201961A07F6060BFF110602031201971A07F6060CFF110702031201981A07F6060DFF110002031201991A07F6060EFF1101020312019A1A07F6060FFF1102020312019B1A07F60610FF1103020312019C1A07F60611FF1104020312019D1A07F60612FF1105020312019E1A07F60613FF1106020312019F1A07F60614FF110702031201A01A07F60615FF110002031201A11A07F60616FF110102031201A21A07F60617FF110202031201A31A07F60618FF1103'
    # print(XmlPdu(XmlPduString=dat).toXml())

    # dat = 'C5 03 C1 0C 00 00 00 05'
    # print(XmlPdu(XmlPduString=dat).toXml())


    dat = """
    C1 01 C1 00 01 00 00 15 00 01 FF 02 00 01 05 02 04 12 00 03 09 06 01 00 01 08 00 FF 11 02 09 00 02 04 12 00 03 09 06 01 00 01 08 01 FF 11 02 09 00 02 04 12 00 03 09 06 01 00 01 08 02 FF 11 02 09 00 02 04 12 00 03 09 06 01 00 01 08 03 FF 11 02 09 00 02 04 12 00 03 09 06 01 00 01 08 04 FF 11 02 09 00 
    """
    print(XmlPdu(XmlPduString=dat).toXml())
