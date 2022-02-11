# -*- coding: UTF-8 -*-

import json
import sys
import traceback
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from .DataFormatAPI import *
from .KFLog import *


def formatXmlString(xmlString):
    """
    格式化XML字符串(带缩减和换号)

    :param xmlString:
    :return:               格式化后的字符串
    """
    xmlBody = ET.tostring(ET.fromstring(xmlString), encoding='utf-8', method='xml')
    return parseString(xmlBody).toprettyxml(indent="  ", newl="\n").replace('<?xml version="1.0" ?>', '')


def convertObisToHex(obis):
    """
    将OBIS转换成16进制数

    :param obis:
    :return:               16进制字符串
    """
    if len(obis) == 12 and re.match(r'^[0-9a-fA-F]{10}[fF]{2}$', obis):
        return obis

    lst = re.split("[\\.,\\-,\\:]", obis)
    if len([item for item in lst if int(item) > 255 or int(item) < 0]) == 0:
        return "".join(["{:02x}".format(int(item)) for item in lst])
    raise Exception(f"OBIS '{obis}' is invalid")


def getRequestNormalXml(classId, obis, attr):
    """
    构造NormalRequest对应的XML结构体

    :param classId:     class id（十进制）
    :param obis:        obis
    :param attr:        attr id（十进制）
    :return:            xml字符串
    """
    classIdHex = "{:04x}".format(int(classId))
    obisHex = convertObisToHex(obis)
    attrHex = "{:02x}".format(int(attr))
    return f'<GetRequest><GetRequestNormal><InvokeIdAndPriority Value="C1" /><AttributeDescriptor><ClassId Value="{classIdHex}" /><InstanceId Value="{obisHex}" /><AttributeId Value="{attrHex}" /></AttributeDescriptor></GetRequestNormal></GetRequest>'


def getResponseFromSetWithList(xmlStr):
    if len(xmlStr) == 0:
        return ''
    try:
        retList = list()
        root = ET.fromstring(xmlStr)
        for result in root.iter("_DataAccessResult"):
            retList.append(result.attrib['Value'])
        return retList
    except ET.ParseError as e:
        error(f"Error: '{e}'")
        return


# 从XML响应中提取数据内容
# def getXmlResponseResult(xmlStr):
#     if len(xmlStr) == 0:
#         error("** No response **")
#         return ''
#     root = ET.fromstring(xmlStr)
#     for result in root.iter("Result"):
#         for child in result:
#             if child.tag == "DataAccessError":
#                 return "NA"
#             if child.tag == "Data":
#                 value = child[0].attrib['Value']
#                 return int(str(value), 16)


def getInvokeIdFromGetResp(xmlStr):
    """
    从GetResponse/SetResponse中提取InvokeId

    :param xmlStr:       xml字符串
    :return:             InvokeId
    """
    if len(xmlStr) == 0:
        # error("** No response **")
        return ''
    try:
        root = ET.fromstring(xmlStr)
        for invoke in root.iter("InvokeIdAndPriority"):
            return invoke.attrib['Value']
    except ET.ParseError as e:
        error(f"Error: '{e}'")
        return ''


# # 从ActionResponse中提取只包含单一数据项的内容
# def getSingleDataFromActionResp(xmlStr):
#     if len(xmlStr) == 0:
#         # error("** No response **")
#         return ''
#     try:
#         root = ET.fromstring(xmlStr)
#         for result in root.iter("ReturnParameters"):
#             for child in result:
#                 return child.attrib['Value']
#     except ET.ParseError as e:
#         error(f"Error: '{e}'")
#         return ''


def getDataFromActionResp(xmlStr):
    """
    从ActionResponse中提取数据项内容

    :param xmlStr:        xml字符串
    :return:              value of ReturnParameters tag
    """
    if xmlStr is None or len(xmlStr) == 0:
        # error("** No response **")
        return ''
    try:
        root = ET.fromstring(xmlStr)
        for result in root.iter("ReturnParameters"):
            isArray = False
            for array in result:
                arrayList = list()
                if array.tag in ("Structure", "Array"):
                    # isArray = True
                    for struct in array.iter("Array"):  # for class 91 act_mac_get_neighbour_table_entry
                        subStructList = list()
                        for child in struct:
                            subStructList.append(child.attrib['Value'])
                        arrayList.append(subStructList)
                    return dict(zip(range(len(arrayList)), arrayList))
            if not isArray:
                for child in result:
                    return child.attrib['Value']
    except ET.ParseError as e:
        error(f"Error: '{e}'")
        return ''


def getSingleDataFromSetResp(xmlStr):
    """
    从SetResponse中提取只包含单一数据项的内容

    :param xmlStr:            xml字符串
    :return:                  value of Result Tag
    """
    if xmlStr is None or len(xmlStr) == 0:
        return ''
    try:
        root = ET.fromstring(xmlStr)
        for result in root.iter("Result"):
            return result.attrib['Value']
    except ET.ParseError as e:
        error(f"Error: '{e}'")
        return


# 从GetResponse中提取只包含单一数据项的内容
def getSingleDataFromGetResp(xmlStr):
    """
    从GetResponse中提取只包含单一数据项的内容

    :param xmlStr:
    :return:     返回一个元组（data, tag）
    """
    if xmlStr is None or len(xmlStr) == 0:
        return '', ''
    try:
        root = ET.fromstring(xmlStr)
        for result in root.iter("Data"):
            for child in result:
                if child.tag in ['Array', 'Structure']:
                    index = 0
                    valDict = dict()
                    tagDict = dict()
                    for subChild in child:
                        valDict[index] = subChild.attrib['Value']
                        tagDict[index] = subChild.tag
                        index += 1
                    return valDict, tagDict
                else:
                    return child.attrib['Value'], child.tag
        else:
            # 如果Get失败，返回失败原因
            for result in root.iter("Result"):
                for child in result:
                    return child.attrib['Value'], child.tag

    except ET.ParseError as e:
        print(f"Error: '{e}'")
        return '', ''


def getStrucDataFromGetResp(xmlStr):
    """
    从GetResponse中提取包含structure数据项的内容

    :param xmlStr:
    :return:           返回一个元组（data, tag）
    """
    if len(xmlStr) == 0:
        # error("** No response **")
        return ''
    try:
        root = ET.fromstring(xmlStr)
        # 如果Get失败，返回失败原因
        if root.findall('*//DataAccessError'):
            for result in root.iter("Result"):
                for child in result:
                    return child.attrib['Value'], child.tag
        for array in root.iter("Array"):  # the first array
            arrayList = list()
            tagArrayList = list()
            for struct in array:  # all structures under the first array
                # for class 21 get_thresholds
                if struct.tag != "Structure" and struct.tag != "Array":
                    structList = list()
                    tagStructList = list()
                    structList.append(struct.attrib['Value'])
                    tagStructList.append(struct.tag)
                    arrayList.append(structList)
                    tagArrayList.append(tagStructList)
                else:
                    structList = list()
                    tagStructList = list()
                    for child in struct:
                        if child.tag == "Array":  # array under structure
                            subChildList = list()
                            tagSubChildList = list()
                            for subChild in child:
                                # for class 6 get_mask_list
                                if subChild.tag != "Structure" and subChild.tag != "Array":
                                    subChildList.append(subChild.attrib['Value'])
                                    tagSubChildList.append(subChild.tag)
                                elif subChild.tag == "Structure":
                                    # for camel billing
                                    sub2ChildList = list()
                                    tag2SubChildList = list()
                                    for sub2Child in subChild:
                                        if sub2Child.tag == "Structure":
                                            sub3ChildList = list()
                                            tag3SubChildList = list()
                                            for sub3Child in sub2Child:
                                                if sub3Child.tag == "Structure":
                                                    sub4ChildList = list()
                                                    tag4SubChildList = list()
                                                    for sub4Child in sub3Child:
                                                        sub4ChildList.append(sub4Child.attrib['Value'])
                                                        tag4SubChildList.append(sub4Child.tag)
                                                    sub3ChildList.append(sub4ChildList)
                                                    tag3SubChildList.append(tag4SubChildList)
                                                else:
                                                    sub3ChildList.append(sub3Child.attrib['Value'])
                                                    tag3SubChildList.append(sub3Child.tag)
                                            sub2ChildList.append(sub3ChildList)
                                            tag2SubChildList.append(tag3SubChildList)
                                        else:
                                            if sub2Child.tag == "NullData":
                                                sub2ChildList.append("NullData")
                                                tag2SubChildList.append("NullData")
                                            else:
                                                sub2ChildList.append(sub2Child.attrib['Value'])
                                                tag2SubChildList.append(sub2Child.tag)
                                    subChildList.append(sub2ChildList)
                                    tagSubChildList.append(tag2SubChildList)
                                else:
                                    subStructList = list()
                                    tagSubStructList = list()
                                    for ele in subChild:
                                        if subChild.tag == "NullData":
                                            subStructList.append("NullData")
                                            tagSubStructList.append("NullData")
                                        else:
                                            subStructList.append(ele.attrib['Value'])
                                            tagSubStructList.append(ele.tag)
                                    subChildList.append(subStructList)
                                    tagSubChildList.append(tagSubStructList)
                            structList.append(subChildList)
                            tagStructList.append(tagSubChildList)

                        # Class15 object lists
                        elif child.tag == "Structure":
                            sub2StructList = list()
                            tagSub2StructList = list()
                            for subChild in child:
                                if subChild.tag == "Array":
                                    sub3StructList = list()
                                    tagSub3StructList = list()
                                    for subStruct in subChild.iter("Structure"):
                                        sub4StructList = list()
                                        tagSub4StructList = list()
                                        for sub2Child in subStruct:
                                            if sub2Child.tag == "NullData":
                                                sub4StructList.append("NullData")
                                                tagSub4StructList.append("NullData")
                                            elif sub2Child.tag == "Array":
                                                sub5StructList = list()
                                                tagSub5StructList = list()
                                                for sub3Child in sub2Child:
                                                    if sub3Child.tag == "NullData":
                                                        sub5StructList.append("NullData")
                                                        tagSub5StructList.append("NullData")
                                                    else:
                                                        sub5StructList.append(sub3Child.attrib['Value'])
                                                        tagSub5StructList.append(sub3Child.tag)
                                                sub4StructList.append(sub5StructList)
                                                tagSub4StructList.append(tagSub5StructList)
                                            else:
                                                sub4StructList.append(sub2Child.attrib['Value'])
                                                tagSub4StructList.append(sub2Child.tag)
                                        sub3StructList.append(sub4StructList)
                                        tagSub3StructList.append(tagSub4StructList)
                                    sub2StructList.append(sub3StructList)
                                    tagSub2StructList.append(tagSub3StructList)
                                # for class 7 get_buffer(0-0:94.43.132.255)
                                elif subChild.tag == "Structure":
                                    # sub3StructList = list()
                                    # tagSub3StructList = list()
                                    for subStruct in subChild.iter("Structure"):  # first structure
                                        sub4StructList = list()
                                        tagSub4StructList = list()
                                        for sub2Child in subStruct:
                                            if sub2Child.tag == "NullData":
                                                sub4StructList.append("NullData")
                                                tagSub4StructList.append("NullData")
                                            elif sub2Child.tag == "Structure":
                                                sub5StructList = list()
                                                tagSub5StructList = list()
                                                for sub3Child in sub2Child:
                                                    if sub3Child.tag == "NullData":
                                                        sub5StructList.append("NullData")
                                                        tagSub5StructList.append("NullData")
                                                    else:
                                                        sub5StructList.append(sub3Child.attrib['Value'])
                                                        tagSub5StructList.append(sub3Child.tag)
                                                sub4StructList.append(sub5StructList)
                                                tagSub4StructList.append(tagSub5StructList)
                                            else:
                                                sub4StructList.append(sub2Child.attrib['Value'])
                                                tagSub4StructList.append(sub2Child.tag)
                                        # sub3StructList.append(sub4StructList)
                                        # tagSub3StructList.append(tagSub4StructList)
                                        break  # first structure  for camel billing 1-0:98.1.2.23
                                    sub2StructList.append(sub4StructList)
                                    tagSub2StructList.append(tagSub4StructList)
                                else:
                                    # C7_SecurityEventLog = '0-0:99.98.9.255'
                                    if subChild.tag == "NullData":
                                        sub2StructList.append("NullData")
                                        tagSub2StructList.append("NullData")
                                    else:
                                        sub2StructList.append(subChild.attrib['Value'])
                                        tagSub2StructList.append(subChild.tag)

                            structList.append(sub2StructList)
                            tagStructList.append(tagSub2StructList)
                            # if isStruct:
                            #     structList.append(sub2StructList)
                            #     tagStructList.append(tagSub2StructList)

                            # if not isStruct:
                            #     # For class 21 get_actions
                            #     for subChild in child:
                            #         if subChild.tag == "NullData":
                            #             sub2StructList.append("NullData")
                            #             tagSub2StructList.append("NullData")
                            #         else:
                            #             sub2StructList.append(subChild.attrib['Value'])
                            #             tagSub2StructList.append(subChild.tag)
                            #     structList.append(sub2StructList)
                            #     subStructList.append(tagSub2StructList)
                        else:
                            if child.tag == "NullData":
                                structList.append("NullData")
                                tagStructList.append("NullData")
                            else:
                                structList.append(child.attrib['Value'])
                                tagStructList.append(child.tag)
                    arrayList.append(structList)
                    tagArrayList.append(tagStructList)
            return dict(zip(range(len(arrayList)), arrayList)), dict(zip(range(len(tagArrayList)), tagArrayList))
        else:
            # XML 不包含 Array, 之包含 Structure
            structList = list()
            tagStructList = list()
            isStructure = False
            for struct in root.iter("Structure"):
                for child in struct:
                    # class 71 for get_actions
                    if child.tag == "Structure":
                        isStructure = True
                        subStructList = list()
                        tagSubStructList = list()
                        for subChild in child.iter("Structure"):
                            for ele in subChild:
                                subStructList.append(ele.attrib['Value'])
                                tagSubStructList.append(ele.tag)
                        structList.append(subStructList)
                        tagStructList.append(tagSubStructList)
                if not isStructure:
                    subStructList = list()
                    tagSubStructList = list()
                    for child in struct:
                        subStructList.append(child.attrib['Value'])
                        tagSubStructList.append(child.tag)
                    structList.append(subStructList)
                    tagStructList.append(tagSubStructList)
            return dict(zip(range(len(structList)), structList)), dict(zip(range(len(tagStructList)), tagStructList))

    except ET.ParseError as e:
        error(f"Error: '{e}'")
        return '', ''


def __checkSimpleData(respData, ckSimpleData):
    if isinstance(respData, dict):
        for listValue in respData.values():
            for item in listValue:
                if re.search(str(ckSimpleData), str(item)) is not None:
                    return KFResult(True, '')
        return KFResult(False, f"'ckSimpleData={ckSimpleData}' not in list of 'respData={respData.values()}'")

    else:
        if re.search(str(ckSimpleData), str(respData)) is None:
            return KFResult(False, f"'ckSimpleData={ckSimpleData}' not equal to 'respData={respData}'")
        return KFResult(True, "")


def __checkComplexData(respData, ckComplexData):
    errorList = list()

    def checkValue(respons, ckData, ckDataIndex):
        # CheckBit()
        if re.match('bit\((.*)\)', ckData):
            bitNums = re.match("bit\((.*)\)", ckData).group(1)
            respDataBit = '{:032b}'.format(int(respons))
            for bitInde in bitNums.split("/"):
                if bitInde.strip().startswith('^'):
                    if respDataBit[31 - int(bitInde.strip().replace('^', ''))] != '0':
                        errorList.append(
                            f"'{ckDataIndex} = {ckData}' no equal to 0 at Indxe = {bitInde} of '{respons} [{respDataBit}]'")
                else:
                    if respDataBit[31 - int(bitInde.strip())] != '1':
                        errorList.append(
                            f"'{ckDataIndex} = {ckData}' no equal to 1 at Indxe = {bitInde} of '{respons} [{respDataBit}]'")
        elif str(ckData).find("*") != -1:
            if len(ckData) != len(respons):
                errorList.append(f"'{ckDataIndex} = {ckData}' no equal to '{respons}'")
            else:
                for index, item in enumerate(str(ckData)):
                    if item == "*":
                        continue
                    if respons[index] != ckData[index]:
                        errorList.append(f"'{ckDataIndex} = {ckData}' no equal to '{respons}'")
                        break
        # 正则匹配
        # elif re.search(ckData, str(respons)) is None:
        #     errorList.append(f"'{ckDataIndex} = {ckData}' no equal to '{respons}'")
        elif ckData != str(respons):
            errorList.append(f"'{ckDataIndex} = {ckData}' no equal to '{respons}'")

    dictLen = len(respData)
    try:
        for cKey, cValue in ckComplexData.items():
            # 处理传入的cKey为负值
            cKey = int(cKey)
            if cKey < 0:
                cKey = dictLen + cKey

            if isinstance(cValue, (str, int)):  # for class 92 check_adp_group_table
                checkValue(str(respData[cKey]), str(cValue), "ckData[%s]" % cKey)

            elif isinstance(cValue, dict):
                for subKey, subValue in cValue.items():
                    checkValue(str(respData[cKey][subKey]), str(subValue), "ckData[%s][%s]" % (cKey, subKey))

            else:
                for index, item in enumerate(cValue):
                    if isinstance(item, int):
                        checkValue(str(respData[cKey][index]), str(item), "ckData[%s][%s]" % (cKey, index))

                    if isinstance(item, str):
                        # 忽略 'NA' 或 空值(忽略部分值的检查)
                        if item.strip().lower() == 'na':
                            continue
                        else:
                            checkValue(str(respData[cKey][index]), item, "ckData[%s][%s]" % (cKey, index))

                    if isinstance(item, list):
                        for subIndex, subItem in enumerate(item):
                            if isinstance(subItem, int):
                                checkValue(str(respData[cKey][index][subIndex]), str(subItem),
                                           "ckData[%s][%s][%s]" % (cKey, index, subIndex))

                            if isinstance(subItem, list):
                                for sub2Index, sub2Item in enumerate(subItem):
                                    checkValue(str(respData[cKey][index][subIndex][sub2Index]), str(sub2Item),
                                               "ckData[%s][%s][%s][%s]" % (cKey, index, subIndex, sub2Index))

                            if isinstance(subItem, str):
                                # 忽略 'NA' 或 空值
                                if subItem.strip().lower() == 'na' or len(subItem.strip()) == 0:
                                    continue
                                else:
                                    checkValue(respData[cKey][index][subIndex], subItem,
                                               "ckData[%s][%s][%s]" % (cKey, index, subIndex))

        if len(errorList) == 0:
            return KFResult(True, "")
        else:
            return KFResult(False, "\n".join(errorList))

    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
        return KFResult(False, f'{e}')


def checkResponsValue(respData, ckValue):
    """
    检查返回结果

    :param respData:   DLMS协议返回的结果
    :param ckValue:    期望的检查值
    :return:  返回一个元组 (True/False, Information)

    # ckValue 可以是一个字典 (注: 字典中的每一个字都是字符串形式)
     ckValue = {
        0 : ["07EE020105050000.*800000", "20", "00000AFE", "00000000"],   # 支持正则表达式
        2 : ["NullData", "", "00000AEE"],                                 # 检查数据时忽略空格
       -1 : ["07E3050204120F00FF800080", "88", "00000AFE", "00000001"]    # 支持倒序
     }

    # ckValue 也可以是一个字符串
     ckValue='1-0:99.1.0.254'
     ckValue='1-0:99.1.0.2\d+5'
    """

    # ckValue 是一个字符串/数值
    if isinstance(ckValue, (str, int)):
        return __checkSimpleData(respData, str(ckValue))

    if isinstance(ckValue, dict):
        return __checkComplexData(respData, ckValue)


def readFrameCounter(project, clientId):
    """
    从 config/FrameCounter 目录下的配置文件中读取frameCounter

    :param project:         项目名
    :param clientId:        客户端ID
    :return:                frameCounter
    """
    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "config/FrameCounter/%s.ini" % project.lower())
    if os.path.exists(filename):
        try:
            with open(filename) as jsonFile:
                data = json.load(jsonFile)
                return int(data.get(str(clientId), -1))
        except:
            return -1
    return -1


def writeFrameCounter(project, clientId, frameCounter):
    """
    将 frameCounter 写入到 config/FrameCounter 目录下的配置文件中

    :param project:         项目名
    :param clientId:
    :param frameCounter:
    """
    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "config/FrameCounter/%s.ini" % project.lower())
    data = dict()
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as jsonFile:
                data = json.load(jsonFile)
        except:
            pass
    with open(filename, 'w') as jsonFile:
        data[str(clientId)] = str(frameCounter)
        json.dump(data, jsonFile)
