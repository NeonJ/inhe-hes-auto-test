# -*- coding:utf-8 -*-
# @Time     :2020/12/8
# @Author   :yimou
# @Version  :v1
# @Updated  :0000/00/00
# @RunTime  :

__all__ = [
    "ValueCheck",
    "readDataByAdmin",
    "defaultValueCheck",
    "accessRightsCheck",
    "dataTypeCheck",
    "getAttrType",
]


class ValueCheck(object):
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

    supported_objects = ["", "nan", 'NA']

    # 客户端对应关系
    clientDict = dict()

    # 电表类型对应列，用于筛选不支持的OBIS
    meterTypeDict = dict()

    simple_data_type = ["null_data", "boolean", "bit_string", "double_long",
                        "double_long_unsigned", "octet_string", "visible_string",
                        "utf8_string", "bcd", "integer", "long", "unsigned",
                        "long_unsigned", "long64", "long64_unsigned", "enum",
                        "float32", "float64", "date_time", "date", "time"]

    def getAttrType(self, **kwargs):
        """
        获取指定属性


        :param config:         yaml配置文件
        :param conn            连接对象
        :return:               从Excel文件中提取到的目标数据
        """

        conn = kwargs.get("conn")
        excel_path = os.path.abspath(f"projects/{Singleton().Project}/MeterIntegrationCase/data.xlsx")
        # 从 data model 中读取数据
        read_result = pd.read_excel(excel_path, header=1, sheet_name=1,
                                    usecols=[0, 6, 7, 10])  # attr id/数据类型/class id/Obis
        read_result = read_result.to_dict()
        # Read data from excel file
        attr_name_index_list = list(list(read_result.values())[0].values())
        data_type_list = list(list(read_result.values())[1].values())
        class_list = list(list(read_result.values())[2].values())
        default_value_list = list(list(read_result.values())[3].values())

        is_start = False
        class_id = None
        obis_id = None

        for i in range(len(class_list)):
            if str(class_list[i]) != "nan" and str(class_list[i]).strip() != "":
                class_id = int(class_list[i])
                obis_id = default_value_list[i]

                is_start = True
                continue

            if is_start:

                if str(attr_name_index_list[i]).strip() in ["", "nan"]:
                    continue
                attr_name_index_list[i] = str(attr_name_index_list[i]).split(".")[0]
                if class_id == 3 and int(attr_name_index_list[i]) == 2:
                    if data_type_list[i].strip() == "double_long_unsigned":
                        print("[" + obis_id.replace("-", ".").replace(":", ".") + "]")
                        print("dataType = DoubleLongUnsigned % dlu")
                    elif data_type_list[i].strip() == "long_unsigned":
                        print("[" + obis_id.replace("-", ".").replace(":", ".") + "]")
                        print("dataType = LongUnsigned % lu")
                    elif data_type_list[i].strip() == "unsigned":
                        print("[" + obis_id.replace("-", ".").replace(":", ".") + "]")
                        print("dataType = Unsigned % u")
                    elif data_type_list[i].strip() == "enum":
                        print("[" + obis_id.replace("-", ".").replace(":", ".") + "]")
                        print("dataType = Enum % e")
                    else:
                        print((f"=========================={obis_id}  {data_type_list[i]}"))

    def read_data_by_admin(self, **kwargs):
        """
        使用权限最大的客户端获取所有OBIS Get属性返回方法并解析对应的数据类型


        :param config:         yaml配置文件
        :param conn            连接对象
        :return:               从Excel文件中提取到的目标数据
        """
        config = kwargs.get("config")
        conn = kwargs.get("conn")

        not_run_action_dict = {}
        not_run_class = [12544, 8192]
        not_run_attr_dict = {}

        # 获取配置文件中的参数(主要包含excel路径和excel相关sheet和列的索引)
        if not config:
            assert False, "config file not exist!"
        object_model_sheet_index = config['Config']['object_model_sheet']
        excel_path = os.path.abspath(f"projects/{Singleton().Project}/MeterIntegrationCase/data.xlsx")
        ret = self.getColumnData(self.clientDict, config, excel_path, self.meterTypeDict, object_model_sheet_index)
        device_type_list = ret["deviceType"]
        attr_name_index_list = ret["attrNameIndex"]
        attr_name_list = ret["attrName"]
        data_type_list = ret["dataType"]
        class_list = ret["class"]
        default_value_list = ret["defaultValue"]
        client_access_rights_list = ret["clientAccessRights"]

        # 复制一个新的Excel文件， 用于将执行结果输入到里面
        result_excel_name = os.path.abspath(f"projects/{Singleton().Project}/MeterIntegrationCase/admin_result.xlsx")
        shutil.copyfile(excel_path, result_excel_name)

        # 在excel最后面插入两列用于填写执行结果
        writer = pd.ExcelWriter(result_excel_name, engine='openpyxl')
        writer.book = load_workbook(result_excel_name)
        ws = writer.book.worksheets[object_model_sheet_index]
        col_max_length = ws.max_column
        ws.insert_cols(col_max_length)
        ws.insert_cols(col_max_length)
        rows = ws.rows

        class_id = None
        obis_id = None
        is_start = False
        is_action = False
        action_index = 0

        # 设置列标题
        row = next(rows)
        row[col_max_length - 1].value = "ResponseData"
        row[col_max_length].value = "DataType"
        row = next(rows)
        row[col_max_length - 1].value = "ResponseData"
        row[col_max_length].value = "DataType"
        for i in range(len(class_list)):
            row = next(rows)
            attr_name_index_list[i] = str(attr_name_index_list[i]).encode('utf-8').decode('utf-8-sig')
            if str(class_list[i]) != "nan" and str(class_list[i]).strip() != "":
                class_id = int(class_list[i])
                obis_id = default_value_list[i]
                action_index = 0

                is_action = False
                is_start = True
                continue

            if is_start:
                if str(attr_name_index_list[i]).strip() in ["", "nan"]:
                    continue
                attr_name_index_list[i] = str(attr_name_index_list[i]).split(".")[0]

                # 以下私有类暂时没有检测
                if class_id in not_run_class:
                    row[col_max_length - 1].value = "Not Run"
                    row[col_max_length].value = "Not Run"
                    continue

                if int(attr_name_index_list[i]) < action_index:
                    is_action = True
                    is_not_run = False
                    for key, value in not_run_action_dict.items():
                        if key == class_id and int(attr_name_index_list[i]) in value:
                            is_not_run = True
                            break
                    if is_not_run:
                        row[col_max_length - 1].value = "Not Run"
                        row[col_max_length].value = "Not Run"
                        continue
                else:
                    is_not_run = False
                    for key, value in not_run_attr_dict.items():
                        if key == class_id and int(attr_name_index_list[i]) in value:
                            is_not_run = True
                            break
                    if is_not_run:
                        row[col_max_length - 1].value = "Not Run"
                        row[col_max_length].value = "Not Run"
                        continue

                action_index += 1

                # 默认
                result = ""
                data_type = ""
                if not is_action:
                    if str(client_access_rights_list[i]).find("Get") != -1:
                        classId = f'{class_id:04x}'.upper()
                        obis = obis_toHex(obis_id)
                        attributeId = f'{int(attr_name_index_list[i]):02x}'.upper()
                        if class_id == 7 and int(attr_name_index_list[i]) == 2:
                            result = """<Data>
                            <Array Qty="0000" >
                            </Array>
                            </Data>"""

                        if class_id == 15 and int(attr_name_index_list[i]) == 2:
                            result = """<Data>
                            <Array Qty="0000" >
                            </Array>
                            </Data>"""

                        else:

                            xmlStr = """<GetRequest>
                               <GetRequestNormal>
                                 <InvokeIdAndPriority Value="C1"/>
                                 <AttributeDescriptor>
                                   <ClassId Value="0007"/>
                                   <InstanceId Value="0100630100FF"/>
                                   <AttributeId Value="02"/>
                                 </AttributeDescriptor>
                                </GetRequestNormal>
                             </GetRequest>"""

                            xmlStr = re.sub(r'(\<ClassId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{classId}\g<2>', xmlStr)
                            xmlStr = re.sub(r'(\<AttributeId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{attributeId}\g<2>',
                                            xmlStr)
                            xmlStr = re.sub(r'(\<InstanceId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{obis}\g<2>', xmlStr)

                            try:
                                response = conn.receiveXmlOrPdu(xmlStr)
                            except:
                                response = None

                            if response is None:
                                result = "Get method no response"

                            elif response.find("<Data>") != -1:
                                result = response[response.find("<Data"):response.rfind("Data>") + 5]

                            elif response.find("<DataAccessError") != -1:
                                match = re.search(r'<DataAccessError Value=(.*)/>?', response)
                                if match:
                                    result = match.group(1)
                    else:
                        result = "No get access rights, need provide set param by user"

                    result = ValueCheck.ILLEGAL_CHARACTERS_RE.sub(r'', result)

                    # 数据类型转换
                    current_data_type = str(data_type_list[i]).replace("-", "_").strip()
                    if current_data_type.split("[")[0] in self.simple_data_type:
                        match_1 = re.search("(.*)\[(.*)\]", current_data_type)
                        data_type = current_data_type
                        if match_1:
                            data_type = "".join(
                                [e.capitalize() for e in match_1.group(1).split("_")]) + "_" + match_1.group(2)

                    else:
                        if result.find("<Data>") != -1:
                            data_type = self.getDataTypeByResponseData(result)
                        else:
                            data_type = result

                row[col_max_length - 1].value = result
                row[col_max_length].value = data_type

        writer.save()
        writer.close()

    def default_value_check(self, **kwargs):
        """
        默认值检查


        :param config:         yaml配置文件
        :param conn            连接对象
        :return:               从Excel文件中提取到的目标数据
        """
        config = kwargs.get("config")
        conn = kwargs.get("conn")

        # 获取配置文件中的参数(主要包含excel路径和excel相关sheet和列的索引)
        if not config:
            assert False, "config file not exist!"
        object_model_sheet_index = config['Config']['object_model_sheet']
        excel_path = os.path.abspath(f"projects/{Singleton().Project}/MeterIntegrationCase/data.xlsx")
        ret = self.getColumnData(self.clientDict, config, excel_path, self.meterTypeDict, object_model_sheet_index)
        device_type_list = ret["deviceType"]
        attr_name_index_list = ret["attrNameIndex"]
        attr_name_list = ret["attrName"]
        data_type_list = ret["dataType"]
        class_list = ret["class"]
        default_value_list = ret["defaultValue"]
        client_access_rights_list = ret["clientAccessRights"]

        # 复制一个新的Excel文件， 用于将执行结果输入到里面
        current_time_str = datetime.datetime.strftime(datetime.datetime.now(), "%m%d_%H%M%S")
        result_excel_name = os.path.abspath(
            f"projects/{Singleton().Project}/MeterIntegrationCase/{Singleton().Project}_{Singleton().Client}_{current_time_str}.xlsx")
        shutil.copyfile(excel_path, result_excel_name)

        # 在excel最后面插入两列用于填写执行结果
        writer = pd.ExcelWriter(result_excel_name, engine='openpyxl')
        writer.book = load_workbook(result_excel_name)
        ws = writer.book.worksheets[object_model_sheet_index]
        col_max_length = ws.max_column
        ws.insert_cols(col_max_length)
        ws.insert_cols(col_max_length)
        rows = ws.rows

        class_id = None
        obis_id = None
        obis_name = None
        is_start = False
        is_action = False
        action_index = 0

        # 设置列标题
        row = next(rows)

        row[col_max_length - 1].value = "Result"
        row[col_max_length].value = "Notes"
        row = next(rows)
        row[col_max_length - 1].value = "Result"
        row[col_max_length].value = "Notes"
        for i in range(len(class_list)):
            row = next(rows)
            attr_name_index_list[i] = str(attr_name_index_list[i]).encode('utf-8').decode('utf-8-sig')
            if str(class_list[i]) != "nan" and str(class_list[i]).strip() != "":
                class_id = int(class_list[i])
                obis_id = default_value_list[i]
                obis_name = attr_name_list[i]
                action_index = 0

                is_action = False
                is_start = True
                continue

            if is_start:

                if str(attr_name_index_list[i]).strip() in ["", "nan"]:
                    continue
                attr_name_index_list[i] = attr_name_index_list[i].split(".")[0]

                if int(attr_name_index_list[i]) < action_index:
                    is_action = True
                action_index += 1

                if str(default_value_list[i]) != "nan":
                    default_value = default_value_list[i]
                else:
                    continue

                # 将数据转为obis格式方便做对比
                convert_result = self.convert_data(default_value)

                if isinstance(convert_result, str):
                    if len(convert_result) == 12:
                        convert_result = hex_toOBIS(convert_result)

                # 将数据转为WildcardTimeString格式方便做对比
                if attr_name_list[i].strip().lower() in ["daylights_savings_begin", "daylights_savings_end"]:
                    convert_result = hex_toWildcardTimeString(convert_result)

                # if str(convert_result).replace("-", "").isdigit():
                #     convert_result = int(convert_result)

                try:
                    if is_action:
                        continue
                    else:
                        start_info = f"Start exec {obis_name}  attr index:{int(attr_name_index_list[i])}:"
                        info(start_info)
                        access_right = str(client_access_rights_list[i]).strip()

                        if access_right.find("Get") != -1:
                            if str(class_id) not in ClassInterfaceMap.keys():
                                result = start_info
                                row[col_max_length - 1].value = "Fail"
                                row[col_max_length].value = "Class not exist"
                                continue

                            result = conn.getMethod(class_id, obis_id, int(attr_name_index_list[i]))
                            info(str(convert_result))
                            if callable(convert_result):
                                def getRet():
                                    try:
                                        ret = convert_result(result)
                                    except:
                                        ret = False

                                    return ret

                                if getRet():
                                    row[col_max_length - 1].value = "Pass"
                                else:
                                    result = start_info + "\n" + str(result)
                                    row[col_max_length - 1].value = "Fail"
                                    row[col_max_length].value = result
                            elif str(result) == str(convert_result):
                                row[col_max_length - 1].value = "Pass"
                            else:
                                result = start_info + "\n" + str(result)
                                row[col_max_length - 1].value = "Fail"
                                row[col_max_length].value = result

                except UnicodeEncodeError:
                    pass

        writer.save()
        writer.close()

    def access_rights_check(self, **kwargs):
        """
        :param config:         yaml配置文件
        :param conn            连接对象
        :return:               从Excel文件中提取到的目标数据
        """
        config = kwargs.get("config")
        conn = kwargs.get("conn")

        pass_count = 0
        fail_count = 0
        total_count = 0
        not_run_count = 0

        # 指定不需要运行的类，属性和Action
        not_run_action_dict = {15: [1],
                               64: [1],
                               }
        not_run_class = [12544, 8192]

        # not_run_attr_dict = {15: [2],
        #                      70: [2, 3]}
        not_run_attr_dict = {}

        # 获取配置文件中的参数(主要包含excel路径和excel相关sheet和列的索引)
        if not config:
            assert False, "config file not exist!"
        object_model_sheet_index = config['Config']['object_model_sheet']
        excel_path = os.path.abspath(f"projects/{Singleton().Project}/MeterIntegrationCase/admin_result.xlsx")
        ret = self.getColumnDataForResponse(self.clientDict, config, excel_path, self.meterTypeDict,
                                            object_model_sheet_index)
        device_type_list = ret["deviceType"]
        attr_name_index_list = ret["attrNameIndex"]
        attr_name_list = ret["attrName"]
        data_type_list = ret["dataType"]
        class_list = ret["class"]
        default_value_list = ret["defaultValue"]
        client_access_rights_list = ret["clientAccessRights"]
        get_value_list = ret["responseValue"]

        # 复制一个新的Excel文件， 用于将执行结果输入到里面
        current_time_str = datetime.datetime.strftime(datetime.datetime.now(), "%m%d_%H%M%S")
        result_excel_name = os.path.abspath(
            f"projects/{Singleton().Project}/MeterIntegrationCase/{Singleton().Project}_{Singleton().Client}_{current_time_str}.xlsx")
        result_txt_name = result_excel_name.replace(".xlsx", ".txt")
        shutil.copyfile(excel_path, result_excel_name)

        # 在excel最后面插入两列用于填写执行结果
        writer = pd.ExcelWriter(result_excel_name, engine='openpyxl')
        writer.book = load_workbook(result_excel_name)
        ws = writer.book.worksheets[object_model_sheet_index]
        col_max_length = ws.max_column
        ws.insert_cols(col_max_length)
        # ws.insert_cols(col_max_length)
        rows = ws.rows

        class_id = None
        obis_id = None
        obis_name = None
        is_start = False
        is_action = False
        action_index = 0

        # 设置列标题
        row = next(rows)
        row[col_max_length - 1].value = "Result"
        row[col_max_length].value = "Notes"
        row = next(rows)
        row[col_max_length - 1].value = "Result"
        row[col_max_length].value = "Notes"
        for i in range(len(class_list)):
            reason_key = None
            row = next(rows)
            attr_name_index_list[i] = str(attr_name_index_list[i]).encode('utf-8').decode('utf-8-sig')
            if str(class_list[i]) != "nan" and str(class_list[i]).strip() != "":
                class_id = int(class_list[i])
                obis_id = default_value_list[i]
                obis_name = attr_name_list[i]
                action_index = 0

                is_action = False
                is_start = True
                continue

            # if class_id not in [17]:
            #     continue

            if is_start:
                if str(attr_name_index_list[i]).strip() in ["", "nan"]:
                    continue
                attr_name_index_list[i] = str(attr_name_index_list[i]).split(".")[0]

                # 以下私有类暂时没有检测
                if class_id in not_run_class:
                    row[col_max_length - 1].value = "Not Run"
                    row[col_max_length].value = "Not Run"
                    continue

                if int(attr_name_index_list[i]) < action_index:
                    is_action = True
                    is_not_run = False
                    for key, value in not_run_action_dict.items():
                        if key == class_id and int(attr_name_index_list[i]) in value:
                            is_not_run = True
                            break
                    if is_not_run:
                        row[col_max_length - 1].value = "Not Run"
                        row[col_max_length].value = "Not Run"
                        continue
                else:
                    is_not_run = False
                    for key, value in not_run_attr_dict.items():
                        if key == class_id and int(attr_name_index_list[i]) in value:
                            is_not_run = True
                            break
                    if is_not_run:
                        row[col_max_length - 1].value = "Not Run"
                        row[col_max_length].value = "Not Run"
                        continue

                action_index += 1

                # 默认
                convert_result = ""
                result = ""
                start_info = ""
                is_failed = False

                if str(get_value_list[i]) != "nan":
                    convert_result = str(get_value_list[i])

                # if not (class_id == 15 and int(attr_name_index_list[i]) == 2):
                #     continue

                classId = f'{class_id:04x}'.upper()
                obis = obis_toHex(obis_id)
                attributeId = f'{int(attr_name_index_list[i]):02x}'.upper()
                try:
                    access_right = str(client_access_rights_list[i]).strip()
                    total_count += 1
                    if is_action:
                        if str(default_value_list[i]) != "nan":
                            convert_result = str(default_value_list[i])

                        if Singleton().isCheckAction == "True":

                            # 标记为--的Action不执行
                            if str(access_right).find("--") != -1:
                                not_run_count += 1
                                row[col_max_length - 1].value = "Not Run"
                                continue

                            start_info = f"Log: Start exec {obis_name}  action index:{int(attr_name_index_list[i])}:"
                            info(start_info)
                            if convert_result != "":
                                ret = conn.actMethod(class_id, obis_id, int(attr_name_index_list[i]), convert_result)
                            else:
                                ret = conn.actMethod(class_id, obis_id, int(attr_name_index_list[i]))

                            if str(access_right).find("Action") != -1:
                                # 支持 action
                                if isinstance(ret, str):
                                    if re.search(r"missing .* argument", ret):
                                        is_failed = True
                                        result = "missing argument"
                                    else:
                                        result = ret
                                elif isinstance(ret, KFResult):
                                    if not ret.status:
                                        is_failed = True
                                        try:
                                            result = f"execute Action failed: {ret.result}"
                                        except AttributeError:
                                            result = "execute Action failed"
                            else:
                                # 不支持action
                                if isinstance(ret, str):
                                    if re.search(r"missing .* argument", ret):
                                        is_failed = True
                                        result = "missing argument"
                                    else:
                                        result = ret
                                elif isinstance(ret, KFResult):
                                    if not (ret and ret.result == "ReadWriteDenied"):
                                        is_failed = True
                                        try:
                                            result = f"execute Action failed: {ret.result}"
                                        except AttributeError:
                                            result = "execute Action failed"
                        else:
                            not_run_count += 1
                            row[col_max_length - 1].value = "Not Run"
                            continue

                    else:

                        # 所有客户端都没有Get权限是否检查
                        if convert_result.find("No get access rights") != -1:
                            not_run_count += 1
                            row[col_max_length - 1].value = "Not Run"
                            continue

                        start_info = f"Log: Start exec {obis_name}  attr index:{int(attr_name_index_list[i])}:"
                        info(start_info)

                        xmlStr = """<GetRequest>
                           <GetRequestNormal>
                             <InvokeIdAndPriority Value="C1"/>
                             <AttributeDescriptor>
                               <ClassId Value="0007"/>
                               <InstanceId Value="0100630100FF"/>
                               <AttributeId Value="02"/>
                             </AttributeDescriptor>
                            </GetRequestNormal>
                         </GetRequest>"""

                        xmlStr = re.sub(r'(\<ClassId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{classId}\g<2>', xmlStr)
                        xmlStr = re.sub(r'(\<AttributeId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{attributeId}\g<2>',
                                        xmlStr)
                        xmlStr = re.sub(r'(\<InstanceId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{obis}\g<2>', xmlStr)
                        response = conn.receiveXmlOrPdu(xmlStr)

                        result = "Get value failed: "
                        if response is not None:
                            if access_right.find("Get") != -1:
                                if response.find("<Data>") == -1:
                                    is_failed = True
                                    match = re.search(r'<DataAccessError Value=(.*)/>?', response)
                                    if match:
                                        result += match.group(1)
                            else:
                                if response.find("ReadWriteDenied") == -1:
                                    is_failed = True
                                    result += "not return ReadWriteDenied"
                        else:
                            is_failed = True
                            result += "no response from meter"

                        if is_failed:
                            result += "\n"
                        else:
                            result = ""

                        # Set check

                        if convert_result.find("<Data>") != -1:
                            convert_result = convert_result.replace("<Data>", "").replace("</Data>", "").replace("\n",
                                                                                                                 "")
                            xmlStrSet = """<SetRequest>
                                <SetRequestNormal>
                                    <InvokeIdAndPriority Value="C1" />
                                <AttributeDescriptor>
                                    <ClassId Value="0001"/>
                                    <InstanceId Value="000060030AFF"/>
                                    <AttributeId Value="02"/>
                                </AttributeDescriptor>
                                <Value>
                                #data#
                                </Value>
                                </SetRequestNormal>
                            </SetRequest>"""
                            xmlStrSet = re.sub(r'(\<ClassId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{classId}\g<2>',
                                               xmlStrSet)
                            xmlStrSet = re.sub(r'(\<AttributeId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{attributeId}\g<2>',
                                               xmlStrSet)
                            xmlStrSet = re.sub(r'(\<InstanceId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{obis}\g<2>',
                                               xmlStrSet)
                            convert_result = xmlStrSet.replace("#data#", f'{convert_result}')

                            response = conn.receiveXmlOrPdu(convert_result)
                            if access_right.find("Set") != -1:
                                if response.find("Success") == -1:
                                    is_failed = True
                                    result += f"Set value Failed: "
                                    match = re.search(r'<Result Value=(.*)/>?', response)
                                    if match:
                                        result += match.group(1)
                            else:
                                for key in data_access_result:
                                    if response.find(key) != -1:
                                        reason_key = key
                                        break

                                    if key == data_access_result[-1]:
                                        is_failed = True
                                        result += f"Set value Failed: "
                                        result += "not return ReadWriteDenied"


                        else:
                            result += f"Set value Failed: "
                            is_failed = True
                            result += f"{convert_result}"
                except Exception as e:
                    error(e)
                    is_failed = True
                    result += f"Exception: {e.__str__()}"
                    pass

                result = self.ILLEGAL_CHARACTERS_RE.sub(r'', result)

                if is_failed:
                    fail_count += 1

                    result = start_info + "\n" + result
                    row[col_max_length - 1].value = "Fail"
                    row[col_max_length].value = result
                else:
                    pass_count += 1
                    row[col_max_length - 1].value = "Pass"
                    if reason_key:
                        row[col_max_length].value = reason_key

        with open(result_txt_name, "w") as f:
            f.writelines("***********\n")
            f.writelines("* Summary *\n")
            f.writelines("***********\n\n")
            f.writelines(f"PASSED {pass_count:>20}\n")
            f.writelines(f"FAILED {fail_count:>20}\n")
            f.writelines(f"NOT RUN {not_run_count:>20}\n")
            f.writelines(f"TOTAL {total_count:>20}\n")

        writer.save()
        writer.close()

    def data_type_check(self, **kwargs):
        """
        数据类型检查

        :param config:         yaml配置文件
        :param conn            连接对象
        :return:               从Excel文件中提取到的目标数据
        """
        config = kwargs.get("config")
        conn = kwargs.get("conn")

        pass_count = 0
        fail_count = 0
        total_count = 0
        not_run_count = 0

        not_run_action_dict = {15: [1],
                               64: [1],
                               }
        not_run_class = [12544, 8192]
        not_run_attr_dict = {}

        # 获取配置文件中的参数(主要包含excel路径和excel相关sheet和列的索引)
        if not config:
            assert False, "config file not exist!"
        object_model_sheet_index = config['Config']['object_model_sheet']
        excel_path = os.path.abspath(f"projects/{Singleton().Project}/MeterIntegrationCase/admin_result.xlsx")
        ret = self.getColumnDataForResponse(self.clientDict, config, excel_path, self.meterTypeDict,
                                            object_model_sheet_index)
        device_type_list = ret["deviceType"]
        attr_name_index_list = ret["attrNameIndex"]
        attr_name_list = ret["attrName"]
        data_type_list = ret["dataType"]
        class_list = ret["class"]
        default_value_list = ret["defaultValue"]
        client_access_rights_list = ret["clientAccessRights"]
        get_value_list = ret["responseValue"]

        # 复制一个新的Excel文件， 用于将执行结果输入到里面
        current_time_str = datetime.datetime.strftime(datetime.datetime.now(), "%m%d_%H%M%S")
        result_excel_name = os.path.dirname(
            __file__) + os.sep + f"result_{Singleton().Project}_{Singleton().Client}_{current_time_str}.xlsx"
        result_txt_name = result_excel_name.replace(".xlsx", ".txt")
        shutil.copyfile(excel_path, result_excel_name)

        # 在excel最后面插入两列用于填写执行结果
        writer = pd.ExcelWriter(result_excel_name, engine='openpyxl')
        writer.book = load_workbook(result_excel_name)
        ws = writer.book.worksheets[object_model_sheet_index]
        col_max_length = ws.max_column
        ws.insert_cols(col_max_length)
        # ws.insert_cols(col_max_length)
        rows = ws.rows

        # 获取每个OBIS属性的数据类型
        data_type_dict = dict()
        obis_id = None
        is_start = False
        action_index = 0
        for i in range(len(class_list)):
            attr_name_index_list[i] = str(attr_name_index_list[i]).encode('utf-8').decode('utf-8-sig')
            if str(class_list[i]) != "nan" and str(class_list[i]).strip() != "":
                obis_id = default_value_list[i]
                action_index = 0
                is_start = True
                continue

            if is_start:
                if str(attr_name_index_list[i]).strip() in ["", "nan"]:
                    continue

                if int(attr_name_index_list[i]) < action_index:
                    pass
                else:
                    if data_type_dict.get(obis_id) is None:
                        data_type_dict[obis_id] = dict()
                    data_type_dict[obis_id][int(attr_name_index_list[i])] = data_type_list[i]

                action_index += 1

        class_id = None
        obis_id = None
        obis_name = None
        is_start = False
        is_action = False
        action_index = 0

        # 设置列标题
        row = next(rows)
        row[col_max_length - 1].value = "Result"
        row[col_max_length].value = "Notes"
        row = next(rows)
        row[col_max_length - 1].value = "Result"
        row[col_max_length].value = "Notes"
        for i in range(len(class_list)):
            row = next(rows)
            attr_name_index_list[i] = str(attr_name_index_list[i]).encode('utf-8').decode('utf-8-sig')
            if str(class_list[i]) != "nan" and str(class_list[i]).strip() != "":
                class_id = int(class_list[i])
                obis_id = default_value_list[i]
                obis_name = attr_name_list[i]
                action_index = 0

                is_start = True
                is_action = False
                continue

            if is_start:

                if i != 127:
                    continue

                if str(attr_name_index_list[i]).strip() in ["", "nan"]:
                    continue

                # 以下私有类暂时没有检测
                if class_id in not_run_class:
                    row[col_max_length - 1].value = "Not Run"
                    row[col_max_length].value = "Not Run"
                    continue

                if int(attr_name_index_list[i]) < action_index:
                    is_action = True
                    is_not_run = False
                    for key, value in not_run_action_dict.items():
                        if key == class_id and int(attr_name_index_list[i]) in value:
                            is_not_run = True
                            break
                    if is_not_run:
                        row[col_max_length - 1].value = "Not Run"
                        row[col_max_length].value = "Not Run"
                        continue
                else:
                    is_not_run = False
                    for key, value in not_run_attr_dict.items():
                        if key == class_id and int(attr_name_index_list[i]) in value:
                            is_not_run = True
                            break
                    if is_not_run:
                        row[col_max_length - 1].value = "Not Run"
                        row[col_max_length].value = "Not Run"
                        continue

                action_index += 1

                # 默认
                convert_result = ""
                result = ""
                start_info = ""
                is_failed = False

                # if not (class_id == 15 and int(attr_name_index_list[i]) == 2):
                #     continue

                classId = f'{class_id:04x}'.upper()
                obis = obis_toHex(obis_id)
                attributeId = f'{int(attr_name_index_list[i]):02x}'.upper()
                try:
                    access_right = str(client_access_rights_list[i]).strip()
                    total_count += 1
                    if is_action:
                        continue

                    else:
                        if access_right.find("Get") != -1:

                            start_info = f"Log: Start exec {obis_name}  attr index:{int(attr_name_index_list[i])}:"
                            info(start_info)

                            if class_id == 7 and int(attr_name_index_list[i]) == 2:
                                xmlStr = """<GetRequest>
                                      <GetRequestNormal>
                                        <InvokeIdAndPriority Value="C1"/>
                                        <AttributeDescriptor>
                                          <ClassId Value="0007"/>
                                          <InstanceId Value="0100630100FF"/>
                                          <AttributeId Value="02"/>
                                        </AttributeDescriptor>
                                        <AccessSelection>
                                          <AccessSelector Value="02"/>
                                          <AccessParameters>
                                            <Structure Qty="04">
                                              <DoubleLongUnsigned Value="00000001"/>
                                              <DoubleLongUnsigned Value="00000001"/>
                                              <LongUnsigned Value="0001"/>
                                              <LongUnsigned Value="0000"/>
                                            </Structure>
                                          </AccessParameters>
                                        </AccessSelection>
                                      </GetRequestNormal>
                                    </GetRequest>"""
                                xmlStr = re.sub(r'(\<InstanceId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{obis}\g<2>',
                                                xmlStr)
                                response = conn.receiveXmlOrPdu(xmlStr)

                                object_list = list(C7Profile(conn, obis_id).get_capture_objects().values())
                                ret = self.checkBufferType(response,
                                                           self.getC7BufferByCaptureObjects(conn, data_type_dict,
                                                                                            object_list))
                                if not ret.status:
                                    is_failed = True
                                    result += str(ret.result)
                            else:
                                if str(data_type_list[i]) == "nan":
                                    fail_count += 1
                                    row[col_max_length - 1].value = "Fail"
                                    row[col_max_length].value = "Need provide expect xml type!"
                                    continue

                                expect_data_type = self.convertXMLtoDict(data_type_list[i])

                                xmlStr = """<GetRequest>
                                   <GetRequestNormal>
                                     <InvokeIdAndPriority Value="C1"/>
                                     <AttributeDescriptor>
                                       <ClassId Value="0007"/>
                                       <InstanceId Value="0100630100FF"/>
                                       <AttributeId Value="02"/>
                                     </AttributeDescriptor>
                                    </GetRequestNormal>
                                 </GetRequest>"""

                                xmlStr = re.sub(r'(\<ClassId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{classId}\g<2>',
                                                xmlStr)
                                xmlStr = re.sub(r'(\<AttributeId Value\=\")[A-F\d]+(\"\/\>)',
                                                f'\g<1>{attributeId}\g<2>', xmlStr)
                                xmlStr = re.sub(r'(\<InstanceId Value\=\")[A-F\d]+(\"\/\>)', f'\g<1>{obis}\g<2>',
                                                xmlStr)
                                response = conn.receiveXmlOrPdu(xmlStr)

                                if response is not None:
                                    if access_right.find("Get") != -1:
                                        if response.find("<Data>") == -1:
                                            is_failed = True
                                            match = re.search(r'<DataAccessError Value=(.*)/>?', response)
                                            if match:
                                                result += match.group(1)
                                        else:
                                            root = ET.fromstring(response)
                                            ret = self.checkDataType(root, expect_data_type)
                                            if not ret.status:
                                                is_failed = True
                                                result += ret.result
                                else:
                                    is_failed = True
                                    result += "no response from meter"
                except Exception as e:
                    error(e)
                    is_failed = True
                    result += f"Exception: {e.__str__()}"
                    pass

                result = self.ILLEGAL_CHARACTERS_RE.sub(r'', result)

                if is_failed:
                    fail_count += 1

                    result = start_info + "\n" + result
                    row[col_max_length - 1].value = "Fail"
                    row[col_max_length].value = result
                else:
                    pass_count += 1
                    row[col_max_length - 1].value = "Pass"

        with open(result_txt_name, "w") as f:
            f.writelines("***********\n")
            f.writelines("* Summary *\n")
            f.writelines("***********\n\n")
            f.writelines(f"PASSED {pass_count:>20}\n")
            f.writelines(f"FAILED {fail_count:>20}\n")
            f.writelines(f"NOT RUN {not_run_count:>20}\n")
            f.writelines(f"TOTAL {total_count:>20}\n")

        writer.save()
        writer.close()

    def getColumnData(self, clientDict, config, excel_path, meterTypeDict, object_model_sheet_index):
        pass

    def getColumnDataForResponse(self, clientDict, config, excel_path, meterTypeDict, object_model_sheet_index):
        pass

    def getDataTypeByResponseData(self, xmlStr):
        """
        从GetResponse中提取包含structure数据项的内容

        :param xmlStr:
        :return:           返回结构体中一个元素的结构

        <GetResponse>
          <GetResponseNormal>
            <InvokeIdAndPriority Value="C1" />
            <Result>
              <Data>
                <Array Qty="0002">
                  <Structure Qty="0002">
                    <Unsigned Value="01" />
                    <Array Qty="0007">
                      <Structure Qty="0003">
                        <OctetString Value="00000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0001" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="08000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0003" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="0A1E0000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0002" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="0D000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0003" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="131E0000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0002" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="15000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0003" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="16000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0001" />
                      </Structure>
                    </Array>
                  </Structure>
                  <Structure Qty="0002">
                    <Unsigned Value="02" />
                    <Array Qty="0007">
                      <Structure Qty="0003">
                        <OctetString Value="00000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0001" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="08000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0003" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="09000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0002" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="0A1E0000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0003" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="12000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0002" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="141E0000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0003" />
                      </Structure>
                      <Structure Qty="0003">
                        <OctetString Value="16000000" />
                        <OctetString Value="FFFFFFFFFFFF" />
                        <LongUnsigned Value="0001" />
                      </Structure>
                    </Array>
                  </Structure>
                </Array>
              </Data>
            </Result>
          </GetResponseNormal>
        </GetResponse>

    如上面个结构体，对于Array和Structure，都只取一个元素内容，返回如下内容

        <Array>
        <Structure>
        <Unsigned/>
        <Array>
        <Structure>
        <OctetString/>
        <OctetString/>
        <LongUnsigned/>
        </Structure>
        </Array>
        </Structure>
        </Array>
        """
        taglist = list()

        def _analysisArray(node, length):

            taglist.append("<Array>")
            for index, item in enumerate(node):

                if item.tag == 'Array':
                    _analysisArray(item, item.attrib['Qty'])
                    break

                elif item.tag == 'Structure':
                    _analysisStruct(item, item.attrib['Qty'])
                    break
                else:
                    _tag = _analysisPlain(item)
                    taglist.append(_tag)
            taglist.append("</Array>")

        def _analysisStruct(node, length):

            taglist.append("<Structure>")
            for index, item in enumerate(node):

                if item.tag == 'Array':
                    _analysisArray(item, item.attrib['Qty'])
                    break
                elif item.tag == 'Structure':
                    _analysisStruct(item, item.attrib['Qty'])
                    break
                else:
                    _tag = _analysisPlain(item)
                    taglist.append(_tag)
            taglist.append("</Structure>")

        def _analysisPlain(node):
            return "<" + node.tag + "/>"

        if xmlStr is None or len(xmlStr) == 0:
            # error("** No response **")
            return ''

        try:
            root = ET.fromstring(xmlStr)
            # 如果Get失败，返回失败原因
            if root.findall('*//DataAccessError'):
                for result in root.iter("Result"):
                    for child in result:
                        return child.attrib['Value']

            # 处理端结构体不从Array开始情况
            if next(root.iter("Data")).find("Array") is not None:
                for item in root.iter("Array"):
                    if item.tag == 'Array':
                        _analysisArray(item, item.attrib['Qty'])
                        break
                    elif item.tag == 'Structure':
                        _analysisStruct(item, item.attrib['Qty'])
                        break
                    else:
                        _tag = _analysisPlain(item)
                        taglist.append(_tag)

                return "\n".join(taglist)
            elif next(root.iter("Data")).find("Structure") is not None:
                for item in root.iter("Structure"):
                    if item.tag == 'Array':
                        _analysisArray(item, item.attrib['Qty'])
                        break
                    elif item.tag == 'Structure':
                        _analysisStruct(item, item.attrib['Qty'])
                        break
                    else:
                        _tag = _analysisPlain(item)
                        taglist.append(_tag)
                return "\n".join(taglist)
            else:
                for result in root.iter("Data"):
                    for child in result:
                        return child.tag

        except ET.ParseError as e:
            error(f"Error: '{e}'")
            return ''

    def convert_data(self, target_str):
        """
        对于提供的data数据格式进行转换，方便和OBIS返回结果做对比。（能转换大部分数据）

        :param target_str:         目标字符串
        :return:                   转换后的结果（字符串，数字或者字典）
        """
        try:
            target_str = str(target_str)
            # 匹配时间格式字符串
            if re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", target_str) and target_str.find("{") == -1:
                return target_str

            if re.search("^\[.*\]$", target_str):
                match1 = re.search("^\[(\d+)\.\.\*\]$", target_str)
                if match1:
                    return lambda x: x >= int(match1.group(1))

                match2 = re.search("^\[(\d+)\.\.(\d+)\]$", target_str)
                if match2:
                    start = int(match2.group(1))
                    end = int(match2.group(2))
                    return lambda x: start <= x <= end

            if target_str.find("...") != -1:
                return "Parse Error!"

            if target_str.lower().find("false") != -1:
                return 0
            if target_str.lower().find("true") != -1:
                return 1
            if target_str == "nan":
                return ""
            if target_str.replace(" ", "").strip() == "{}":
                return dict()

            if target_str.find("//") != -1:
                target_str = re.sub("//.*", "", target_str)

            if target_str.startswith("\""):
                target_str = target_str.replace("\"", "")

            if not re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", target_str):
                target_str = target_str.replace(" ", "").replace("\n", "")

            target_str = target_str.replace("},}", "}}")

            # 去掉多余的引号
            target_str = re.sub("\"([[a-zA-Z\d]{12})\"", "\g<1>", target_str)
            target_str = re.sub("\"([[a-zA-Z\d]{24})\"", "\g<1>", target_str)
            target_str = re.sub("\"(\d+)\"", "\g<1>", target_str)

            if target_str.find("choice") != -1:  # for class 72 mbus_port_reference
                target_str = target_str.replace("choice", "").replace("(", "[").replace(")", "]")
                target_str = re.sub("(\d+\-\d+:\d+\.\d+\.\d+\.\d+)", "\'\g<1>\'", target_str)
                result_list = eval(target_str)
                return dict(zip(range(len(result_list)), result_list))

            if target_str.find("*") != -1:
                target_str = target_str.replace("{", "").replace("}", "")
                result_list = list()
                result_list.append(target_str.split(","))
                return dict(zip(range(len(result_list)), result_list))

            if target_str.startswith("0x"):
                return int(target_str, 16)

            if target_str.find("{") == -1 and target_str.find(",") != -1:
                return target_str.split(",")

            if target_str.find("{") != -1:
                target_str = target_str.replace(";", ",")

                # 对obis格式（1-0:1.8.2.255）数据加上引号，方便后面用eval函数做处理
                target_str = re.sub("(\d+\-\d+:\d+\.\d+\.\d+\.\d+)", "\'\g<1>\'", target_str)
                target_str = target_str.replace("{", "[").replace("}", "]")

                if target_str.count("[") == 1:
                    result_list = list()
                    result_list.append(eval(target_str))
                else:
                    result_list = eval(target_str)
                return dict(zip(range(len(result_list)), result_list))
            else:
                return target_str
        except (TypeError, SyntaxError, NameError, ValueError) as e:
            return f"Parse Error: {e}"

    def convertXMLtoDict(self, xml):

        result = {}
        key_list = list()

        type_list = [e for e in xml.splitlines() if e != ""]
        for value in type_list:
            value = value.strip()

            if value.startswith("</"):
                continue
            if value.lower() == '<array>':
                if key_list:
                    tmp = result
                    for key in key_list:
                        tmp = tmp[key]
                    tmp["Array"] = {}
                else:
                    result["Array"] = {}

                key_list.append("Array")
            elif value.lower() == '<structure>':
                if key_list:
                    tmp = result
                    for key in key_list:
                        tmp = tmp[key]
                    tmp["Structure"] = {}
                else:
                    result["Structure"] = {}

                key_list.append("Structure")
            else:
                data_length = None
                value = value.replace("<", "").replace(">", "").replace("/", "")
                match = re.search(r'\((\d+)\)', value)
                if re.search("[-_]", value):
                    value = "".join([e.capitalize() for e in re.split("-_")])
                if match:
                    data_length = int(match.group(1))
                    value = value.split("(")[0]

                if key_list:
                    tmp = result
                    for key in key_list:
                        tmp = tmp[key]

                    if tmp.get(value) is not None:
                        count = 0
                        for e in list(tmp.keys()):
                            if value in e:
                                count += 1
                        tmp[f"{value}_{count}"] = data_length if data_length is not None else ""
                    else:
                        tmp[value] = data_length if data_length is not None else ""
                else:
                    result[value] = data_length if data_length is not None else ""
        return result

    def checkDataType(self, xml, d):
        """
        判断xml对象数据类型是否正确

        :param xml:
        :param d:
        :return:
        """
        if 'Array' in d.keys():
            if str(ET.tostring(xml)).find('Array') == -1:
                return KFResult(False, f"Not found Array tag")

            for array in xml.iter("Array"):
                if str(ET.tostring(xml)).find('Structure') == -1:
                    return KFResult(False, f"Not found Structure tag")

                for struct in array:
                    data_type = list(d["Array"]["Structure"].keys())
                    for index, value in enumerate(struct):
                        if data_type[index] in ["Array", "Structure"]:
                            return self.checkDataType(value,
                                                      {data_type[index]: d["Array"]["Structure"][data_type[index]]})
                        else:
                            if value.tag not in data_type[index]:
                                return KFResult(False, f"{value.tag} not equal to {data_type[index]}")
                            else:
                                if d["Array"]["Structure"][data_type[index]] != "":
                                    if d["Array"]["Structure"][data_type[index]] != len(value.attrib['Value']) // 2:
                                        return KFResult(False, f"{value.tag} length is incorrect")
                break
        elif 'Structure' in d.keys():
            if str(ET.tostring(xml)).find('Structure') == -1:
                return KFResult(False, f"Not found Structure tag")

            for struct in xml.iter("Structure"):
                data_type = list(d["Structure"].keys())
                for index, value in enumerate(struct):
                    if data_type[index] in ["Array", "Structure"]:
                        return self.checkDataType(value, {data_type[index]: d["Structure"][data_type[index]]})
                    else:
                        if value.tag not in data_type[index]:
                            return KFResult(False, f"{value.tag} not equal to {data_type[index]}")
                        else:
                            if d["Structure"][data_type[index]] != "":
                                if d["Structure"][data_type[index]] != len(value.attrib['Value']) // 2:
                                    return KFResult(False, f"{value.tag} length is incorrect")
        else:
            data_type = list(d.keys())[0]
            real_tag = ""
            if str(ET.tostring(xml)).find(data_type) == -1:
                is_start = False
                for line in bytes.decode(ET.tostring(xml)).splitlines():
                    if line.find("<Data>") != -1:
                        is_start = True

                    if is_start:
                        match = re.search(r"<(.*) Value=.*", line)
                        if match:
                            real_tag = match.group(1)
                            break

                return KFResult(False, f"{real_tag} not equal to {data_type}")

            for value in xml.iter(data_type):
                if value.tag not in data_type:
                    return KFResult(False, f"{value.tag} not equal to {data_type}")
                else:
                    if d[data_type] != "":
                        if d[data_type] != len(value.attrib['Value']) // 2:
                            return KFResult(False, f"{value.tag} length is incorrect")

        return KFResult(True, "")

    def getC7BufferByCaptureObjects(self, conn, dataTypeDict, object_list):
        expect_list = list()
        expect_list.extend(['<array>', '<structure>'])
        for index, value in enumerate(object_list):
            if value[0] == 7:
                tmp_list = list(C7Profile(conn, value[1]).get_capture_objects().values())
                expect_list.extend(['<array>', '<structure>'])
                for e in tmp_list:
                    if e[2] == 0:
                        expect_list.append('<structure>')
                        expect_list.append(e)
                        expect_list.append('</structure>')
                    else:
                        expect_list.append(e)
                expect_list.extend(['</structure>', '</array>'])
            else:
                if value[2] == 0:
                    expect_list.append('<structure>')
                    expect_list.append(value)
                    expect_list.append('</structure>')
                else:
                    expect_list.append(value)
        expect_list.extend(['</structure>', '</array>'])

        data_type = list()
        for value in expect_list:
            if re.search("array|structure", str(value)) is None:
                if dataTypeDict.get(value[1]):
                    if value[2] == 0:
                        for ele in dataTypeDict.get(value[1]).values():
                            if ele.find("<") != -1:
                                tmp = [e.strip() for e in ele.splitlines() if e.strip() != ""]
                                for e in tmp:
                                    data_type.append(e)
                            else:
                                data_type.append(ele)
                    else:
                        ele = dataTypeDict.get(value[1])[value[2]]
                        if ele.find("<") != -1:
                            tmp = [e.strip() for e in ele.splitlines() if e.strip() != ""]
                            for e in tmp:
                                data_type.append(e)
                        else:
                            data_type.append(ele)
                else:
                    raise Exception(f"{value[1]} not in data model!")
            else:
                data_type.append(value)

        for index, value in enumerate(data_type):
            value = "".join(
                [e.capitalize() for e in value.replace("</", "").replace("<", "").replace(">", "").split("-")])
            data_length = None
            match = re.search(r'\((\d+)\)', value)
            if match:
                data_length = int(match.group(1))
                value = value.split("(")[0]

            if data_length is not None:
                value = f"{value}_{data_length}"

            data_type[index] = value

        return data_type

    def checkBufferType(self, xml, lst):
        """
        判断xml对象数据类型是否正确

        :param xml:
        :param lst:
        :return:
        """
        xml = ET.fromstring(xml)
        xml = next(xml.iter("Array"))
        xml = ET.tostring(xml)
        xml = xml.splitlines()
        xml = [bytes.decode(value).strip() for value in xml if bytes.decode(value).strip() != ""]

        lst = [value.strip() for value in lst if value.strip() != ""]
        response = list()
        for index, value in enumerate(xml):
            item = lst.pop(0)

            match = re.search(r"</(?P<tag1>.*)>|<(?P<tag2>.*) Value=.*|<(?P<tag3>.*) Qty=.*", value)
            tag = match.group("tag1") or match.group("tag2") or match.group("tag3")
            if re.search("Array", str(value)):
                if item.find("Array") == -1 or tag != "Array":
                    response.append(f"Line:{index}, Real Value: {value},  Expect Value: {item}")
            elif re.search("Structure", str(value)):
                if item.find("Structure") == -1 or tag != "Structure":
                    response.append(f"Line:{index}, Real Value: {value},  Expect Value: {item}")
            else:
                if item.find("_") != -1:
                    real_tag, length = item.split("_")
                    length = int(length)
                    match = re.search(r".*Value=\"(.*)\"", value)
                    attr_value = match.group(1)
                    if real_tag != tag or length * 2 != len(attr_value):
                        response.append(f"Line:{index}, Real Value: {value},  Expect Value: {item}")
                else:
                    if tag != item:
                        response.append(f"Line:{index}, Real Value: {value},  Expect Value: {item}")
        if len(response) > 0:
            return KFResult(False, response)

        return KFResult(True, "")


readDataByAdmin = ValueCheck().read_data_by_admin
defaultValueCheck = ValueCheck().default_value_check
accessRightsCheck = ValueCheck().access_rights_check
dataTypeCheck = ValueCheck().data_type_check
getAttrType = ValueCheck().getAttrType
