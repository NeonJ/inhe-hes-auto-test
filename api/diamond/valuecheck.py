# -*- coding:utf-8 -*-
# @Time     :2020/12/8
# @Author   :yimou
# @Version  :v1
# @Updated  :0000/00/00
# @RunTime  :

__all__ = [
    "readDataByAdmin",
    "defaultValueCheck",
    "accessRightsCheck",
    "dataTypeCheck",
]


class DiamondValueCheck(ValueCheck):
    # 客户端对应关系
    clientDict = {
        1: 9,
    }

    # 电表类型对应列，用于筛选不支持的OBIS
    meterTypeDict = {
        "SP": 10,
        "PP": 11,
    }

    def getColumnData(self, clientDict, config, excel_path, meterTypeDict, object_model_sheet_index):
        attr_name = config['Config']['attr_name']
        attr_name_index = config['Config']['index']
        class_index = config['Config']['class']
        client_index = clientDict[Singleton().Client]
        default_value_index = config['Config']['default_value']
        device_type_index = meterTypeDict[Singleton().MeterType]
        data_type_index = config['Config']['data_type']
        set_xml_index = config['Config']['set_xml_index']
        # 从 data model 中读取数据
        read_result = pd.read_excel(excel_path, header=1, sheet_name=object_model_sheet_index, usecols=[attr_name,
                                                                                                        class_index,
                                                                                                        default_value_index,
                                                                                                        client_index,
                                                                                                        attr_name_index,
                                                                                                        device_type_index,
                                                                                                        data_type_index,
                                                                                                        set_xml_index])
        read_result = read_result.to_dict()
        # Read data from excel file
        device_type_list = list(list(read_result.values())[6].values())
        attr_name_index_list = list(list(read_result.values())[0].values())
        attr_name_list = list(list(read_result.values())[1].values())
        data_type_list = list(list(read_result.values())[2].values())
        class_list = list(list(read_result.values())[3].values())
        default_value_list = list(list(read_result.values())[4].values())
        client_access_rights_list = list(list(read_result.values())[5].values())
        return {
            "deviceType": device_type_list,
            "attrNameIndex": attr_name_index_list,
            "attrName": attr_name_list,
            "dataType": data_type_list,
            "class": class_list,
            "defaultValue": default_value_list,
            "clientAccessRights": client_access_rights_list,
        }

    def getColumnDataForResponse(self, clientDict, config, excel_path, meterTypeDict, object_model_sheet_index):
        attr_name = config['Config']['attr_name']
        attr_name_index = config['Config']['index']
        class_index = config['Config']['class']
        client_index = clientDict[Singleton().Client]
        default_value_index = config['Config']['default_value']
        device_type_index = meterTypeDict[Singleton().MeterType]
        data_type_index = config['Config']['data_type']
        set_xml_index = config['Config']['set_xml_index']
        # 从 data model 中读取数据
        read_result = pd.read_excel(excel_path, header=1, sheet_name=object_model_sheet_index, usecols=[attr_name,
                                                                                                        class_index,
                                                                                                        default_value_index,
                                                                                                        client_index,
                                                                                                        attr_name_index,
                                                                                                        device_type_index,
                                                                                                        data_type_index,
                                                                                                        set_xml_index])
        read_result = read_result.to_dict()
        # Read data from excel file
        device_type_list = list(list(read_result.values())[5].values())
        attr_name_index_list = list(list(read_result.values())[0].values())
        attr_name_list = list(list(read_result.values())[1].values())
        data_type_list = list(list(read_result.values())[7].values())
        get_value_list = list(list(read_result.values())[6].values())  # Response data
        class_list = list(list(read_result.values())[2].values())
        default_value_list = list(list(read_result.values())[3].values())
        client_access_rights_list = list(list(read_result.values())[4].values())
        return {
            "deviceType": device_type_list,
            "attrNameIndex": attr_name_index_list,
            "attrName": attr_name_list,
            "dataType": data_type_list,
            "class": class_list,
            "defaultValue": default_value_list,
            "clientAccessRights": client_access_rights_list,
            "responseValue": get_value_list,
        }


readDataByAdmin = DiamondValueCheck().read_data_by_admin
defaultValueCheck = DiamondValueCheck().default_value_check
accessRightsCheck = DiamondValueCheck().access_rights_check
dataTypeCheck = DiamondValueCheck().data_type_check
