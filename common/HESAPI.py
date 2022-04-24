import os

import yaml



class HESAPI(object):

    def __init__(self, **argv):
        self.HESAPIAddress = argv['Address']
        self.HESRequestMessage = argv.get('RequestMessage', '/api/v1/Request/RequestMessage')
        self.HESCreateTask = argv.get('CreateTask', '/Mdm/CreateTas')
        self.HESMeterStatus = argv.get('MeterStatus', '/Mdm/GetMeterStatus?MeterNo=')
        self.SmartPark = argv.get('Install','/hes/api/device')
        # self.HESDLMS = argv.get('', '')
        # OBIS、升级、时间、费率、结算、需量、负荷曲线、质量曲线、状态字、时间、负控、预付费

    def requestAddress(self):
        return self.HESAPIAddress + self.HESRequestMessage

    def taskAddress(self):
        return self.HESAPIAddress + self.HESCreateTask

    def installAddress(self):
        return self.HESAPIAddress + self.SmartPark

class RequestMessage(object):

    def __init__(self, **argv):
        """
        :param correlationId           Unique identifier用于关联请求消息与回复消息
        :param messageId               Unique identifier作为消息的唯一编号
        :param createTime              任务请求时间，格式yyMMddHHmmss
        :param serviceType
            --HES服务类型，可填入以下其中一个参数：
            1. SET_COMMON
            2. GET_COMMON
            3. GET_PROFILE
            4. RELAY_CONTROL
            5. GET_TARIFF
            6. SET_TARIFF_BY_TARIFF_ID
            7. SET_TARIFF_BY_TARIFF_CONTENT
            8. FIRMWARE_UPGRADE
            9. NOTIFY_FTP_PATH
            10. CHANGE_KEY
            11. GET_DEVICE_NETWORK_STATUS
            12. QUERY_HES_TASK
        :param businessType            请求的业务类型,参数的详细说明详见附录3-Business Type
        :param source                  固定值：MDM
        :param replyType               不使用
        :param replyAddress            不使用
        :param messageType             固定值：REQUEST
        :param asyncReplyFlag          固定值：false
        :param deviceNo                设备编号
        :param deviceType              设备类型，参数的详细说明详见附录4-Device Type
        :param retryCount              不使用
        :param priority                不使用
        :param startTime               不使用
        :param endTime                 不使用
        :param transactionId           Unique identifier用于关联请求消息与回复消息中对单个设备的任务
        :param registerId              通过registerId可查询到OBIS，Attribute等配置，参数的详细说明详见附录2-Register ID, serviceType=GET_COMMON,SET_COMMON,GET_PROFILE时，直接作用于registerId，该参数必填。
        :param featurePoint            服务实现方式，通过featurePoint以及设备的model_code可以从H_PTL_REGISTER表中查询到OBIS，Attribute等配置。serviceType=RELAY_CONTROL,DCU相关业务类型时，直接作用于featurePoint（featurePoint可配置针对不同项目的register），该参数必填。
        :param parameter               处理serviceType对应的业务所需要的参数，不同的serviceType对应的data格式不同参数的详细说明详见3- Data参数结构说明
        :param jobUniqueFlag           标记是否需要保证任务类型在H_TASK_RUNNING表中唯一，true-要保证唯一，false-不限制。默认取值为false。
        """
        self.correlationId = argv['correlationId']
        self.messageId = argv['messageId']
        self.createTime = argv.get('createTime', 'null')
        self.serviceType = argv['serviceType']
        self.businessType = argv['businessType']
        self.source = argv['source']
        self.replyType = argv.get('replyType', 'null')
        self.replyAddress = argv.get('replyAddress', 'null')
        self.messageType = argv.get('messageType', 'REQUEST')
        self.asyncReplyFlag = argv['asyncReplyFlag']
        self.deviceNo = argv['deviceNo']
        self.deviceType = argv['deviceType']
        self.retryCount = argv.get('retryCount', 2)
        self.priority = argv.get('priority', 0)
        self.startTime = argv.get('startTime', 'null')
        self.endTime = argv.get('endTime', 'null')
        self.transactionId = argv['transactionId']
        self.registerId = argv['registerId']
        self.featurePoint = argv.get('featurePoint', '')
        self.parameter = argv['parameter']
        self.jobUniqueFlag = argv['jobUniqueFlag']
        self.accessSelector = argv['accessSelector']
        self.clientId = argv.get('clientId', 1)
        self.jobType = argv['jobType']

    def request_json(self):
        request_json = {
            "header": {
                "correlationId": self.correlationId,
                "messageId": self.messageId,
                "serviceType": self.serviceType,
                "businessType": self.businessType,
                "source": self.source,
                "createTime": self.createTime,
                "replyAddress": self.replyAddress,
                "replyType": self.replyType,
                "messageType": self.messageType,
                "asyncReplyFlag": self.asyncReplyFlag
            },
            "payload": [
                {
                    "deviceNo": self.deviceNo,
                    "deviceType": self.deviceType,
                    "retryCount": self.retryCount,
                    "retryInterval": 0,
                    "priority": self.priority,
                    "endTime": self.endTime,
                    "startTime": self.startTime,
                    "transactionId": self.transactionId,
                    "jobUniqueFlag": self.jobUniqueFlag,
                    "data": [
                        {
                            "clientId": self.clientId,
                            "registerId": self.registerId,
                            "accessSelector": self.accessSelector,
                            "parameter": self.parameter,
                            "featurePoint": self.featurePoint
                        }
                    ]
                }
            ]
        }
        return request_json

    def create_task_json(self):
        request_json = {
            "header": {
                "correlationId": self.correlationId,
                "messageId": self.messageId,
                "createTime": self.createTime,
                "serviceType": "CMD_COMMON",
                "businessType": self.businessType,
                "source": "REG",
                "replyAddress": self.replyAddress,
                "replyType": "MQ",
                "messageType": "REQUEST",
                "asyncReplyFlag": "true"
            },
            "payload": [
                {
                    "deviceNo": self.deviceNo,
                    "deviceType": self.deviceType,
                    "retryCount": self.retryCount,
                    "priority": 2,
                    "retryInterval": 2,
                    "startTime": self.startTime,
                    "endTime": self.endTime,
                    "transactionId": self.transactionId,
                    "jobUniqueFlag": "false",
                    "exePolicy": "",
                    "data": self.parameter
                }
            ]
        }

        return request_json

    def createTask(self):
        request_json = [
            {
                "deviceType": self.deviceType,
                "deviceNo": self.deviceNo,
                "transactionId": self.transactionId,
                "jobType": self.jobType,
                "taskStartTime": self.startTime,
                "taskOvertime": self.endTime,
                "readFromTime": self.startTime,
                "readEndTime": self.startTime,
                "retryTime": 1,
                "retryInterval": 1,
                "priority": 0,
                "responseType": 0,
                "jsonParam": None,
                "exParam": None,
                "isCheckJobtype": "true"
            }
        ]


def read_config(file_path):
    """读取配置文件内容"""
    with open(file_path, encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config


# if __name__ == '__main__':
#     file_path = os.path.abspath(f"conf/DefaultValue/tulip/user.yaml")
#     user_config = read_config(file_path)
#     db_queue = DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
#                   database=user_config['Database']['database'], username=user_config['Database']['username'],
#                   passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
#                   sid=user_config['Database']['sid']).fetchall_dict(
#         "select register_id,class_id,attribute_id,register_desc,is_method,data_type,rw from H_PTL_REGISTER where PTL_TYPE = (select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no='1KFM5600000003'))and register_id='0.0.1.0.0.255830'")
#     for queue in db_queue:
#         print(
#             "Register_ID:{register_id}, Class_ID:{class_id}, Attribute_id:{attribute_id}, Is_method:{is_method}, RW:{rw}, Desc:{register_desc}".format(
#                 **queue))
#         if queue.get('rw') == 'r':
#             RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
#                                           messageId=user_config['Request']['messageId'],
#                                           source=user_config['Request']['source'],
#                                           serviceType='GET_COMMON',
#                                           messageType=user_config['Request']['messageType'],
#                                           asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
#                                           deviceNo=user_config['Request']['deviceNo'],
#                                           deviceType=user_config['Request']['deviceType'],
#                                           registerId=queue.get('register_id'),
#                                           transactionId=user_config['Request']['transactionId'],
#                                           jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
#                                           parameter=user_config['Request']['parameter'],
#                                           accessSelector=user_config['Request']['accessSelector']).request_json()
#             # print(json.dumps(RequestQueue, indent=4))
#             response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
#                                      headers={"Content-Type": "application/json-patch+json"},
#                                      data=json.dumps(RequestQueue, indent=4))
#             # print( for payload in response.get('payload'): return payload )
#             for payload in response.get('payload'):
#                 for data in payload.get('data'):
#                     print('Read Result: ', data.get('resultDesc'))
#             for payload in response.get('payload'):
#                 for data in payload.get('data'):
#                     print(data.get('resultValue'))
#         elif queue.get('rw') == 'w':
#             RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
#                                           messageId=user_config['Request']['messageId'],
#                                           source=user_config['Request']['source'],
#                                           serviceType='SET_COMMON',
#                                           messageType=user_config['Request']['messageType'],
#                                           asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
#                                           deviceNo=user_config['Request']['deviceNo'],
#                                           deviceType=user_config['Request']['deviceType'],
#                                           registerId=queue.get('register_id'),
#                                           transactionId=user_config['Request']['transactionId'],
#                                           jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
#                                           parameter=user_config['Request']['parameter'],
#                                           accessSelector=user_config['Request']['accessSelector']).request_json()
#             print(json.dumps(RequestQueue, indent=4))
#             response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
#                                      headers={"Content-Type": "application/json-patch+json"},
#                                      data=json.dumps(RequestQueue, indent=4))
#             print(response.json())
#         elif queue.get('rw') == 'rw':
#             RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
#                                           messageId=user_config['Request']['messageId'],
#                                           source=user_config['Request']['source'],
#                                           serviceType='GET_COMMON',
#                                           messageType=user_config['Request']['messageType'],
#                                           asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
#                                           deviceNo=user_config['Request']['deviceNo'],
#                                           deviceType=user_config['Request']['deviceType'],
#                                           registerId=queue.get('register_id'),
#                                           transactionId=user_config['Request']['transactionId'],
#                                           jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
#                                           parameter=user_config['Request']['parameter'],
#                                           accessSelector=user_config['Request']['accessSelector']).request_json()
#             # print(json.dumps(RequestQueue, indent=4))
#             response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
#                                      headers={"Content-Type": "application/json-patch+json"},
#                                      data=json.dumps(RequestQueue, indent=4))
#             # print( for payload in response.get('payload'): return payload )
#             for payload in response.get('payload'):
#                 for data in payload.get('data'):
#                     print('Read Result: ', data.get('resultDesc'))
#             for payload in response.get('payload'):
#                 for data in payload.get('data'):
#                     print(data.get('resultValue'))
#                     parameter = data.get('resultValue')
#                     DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
#                        database=user_config['Database']['database'], username=user_config['Database']['username'],
#                        passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
#                        sid=user_config['Database']['sid']).save_result('get_result', parameter,
#                                                                        queue.get('register_id'))
#
#             RequestQueue = RequestMessage(correlationId=user_config['Request']['correlationId'],
#                                           messageId=user_config['Request']['messageId'],
#                                           source=user_config['Request']['source'],
#                                           serviceType='SET_COMMON',
#                                           messageType=user_config['Request']['messageType'],
#                                           asyncReplyFlag=user_config['Request']['asyncReplyFlag'],
#                                           deviceNo=user_config['Request']['deviceNo'],
#                                           deviceType=user_config['Request']['deviceType'],
#                                           registerId=queue.get('register_id'),
#                                           transactionId=user_config['Request']['transactionId'],
#                                           jobUniqueFlag=user_config['Request']['jobUniqueFlag'],
#                                           parameter=parameter,
#                                           accessSelector=user_config['Request']['accessSelector']).request_json()
#             # print(json.dumps(RequestQueue, indent=4))
#             response = requests.post(url=HESAPI(Address=user_config['HESAPI']['url']).requestAddress(),
#                                      headers={"Content-Type": "application/json-patch+json"},
#                                      data=json.dumps(RequestQueue, indent=4))
#             # print( for payload in response.get('payload'): return payload )
#             for payload in response.get('payload'):
#                 for data in payload.get('data'):
#                     print('Set Result: ', data.get('resultDesc'))
#                     DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
#                        database=user_config['Database']['database'], username=user_config['Database']['username'],
#                        passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
#                        sid=user_config['Database']['sid']).save_result('set_result', data.get('resultDesc'),
#                                                                        queue.get('register_id'))
#             for payload in response.get('payload'):
#                 for data in payload.get('data'):
#                     print(data.get('resultValue'))


class ResponseMessage(object):

    def __init__(self, **argv):
        """
        :param correlationId           与SyncRequestMessage/Header中一致
        :param messageId               Unique identifier作为消息的唯一编号
        :param createTime              与SyncRequestMessage/Header中一致
        :param serviceType             与SyncRequestMessage/Header中一致
            --HES服务类型，可填入以下其中一个参数：
            1. SET_COMMON
            2. GET_COMMON
            3. GET_PROFILE
            4. RELAY_CONTROL
            5. GET_TARIFF
            6. SET_TARIFF_BY_TARIFF_ID
            7. SET_TARIFF_BY_TARIFF_CONTENT
            8. FIRMWARE_UPGRADE
            9. NOTIFY_FTP_PATH
            10. CHANGE_KEY
            11. GET_DEVICE_NETWORK_STATUS
            12. QUERY_HES_TASK
        :param businessType            请求的业务类型,参数的详细说明详见附录3-Business Type
        :param source                  固定值：HES
        :param messageType             固定值：RESPONSE
        :param code                    单个设备任务执行结果的错误码, 参数的详细说明详见附录5-Error Code
        :param desc                    单个设备任务执行结果的描述
        :param deviceNo                设备编号
        :param deviceType              设备类型，参数的详细说明详见附录4-Device Type
        :param totalRetryCount         不使用
        :param remainRetryCount        不使用
        :param priority                不使用
        :param executeStartTime        与电表通信的开始时间
        :param executeEndTime          与电表通信的结束时间
        :param transactionId           Unique identifier用于关联请求消息与回复消息中对单个设备的任务
        :param data                    serviceType对应的业务处理完后返回的参数，不同的serviceType对应的data格式不同,参数的详细说明详见3- Data参数返回结构说明
        :param replyDesc               异步任务同步返回结果的描述
        :param replyCode               异步任务同步返回结果错误码参数的详细说明详见附录6-Reply Code
        """
        self.correlationId = argv['correlationId']
        self.messageId = argv['messageId']
        self.createTime = argv['createTime']
        self.serviceType = argv['serviceType']
        self.businessType = argv['businessType']
        self.source = argv['source']
        self.replyType = argv['replyType']
        self.replyAddress = argv['replyAddress']
        self.messageType = argv['messageType']
        self.asyncReplyFlag = argv['asyncReplyFlag']
        self.deviceNo = argv['deviceNo']
        self.deviceType = argv['deviceType']
        self.retryCount = argv['retryCount']
        self.priority = argv['priority']
        self.startTime = argv['startTime']
        self.endTime = argv['endTime']
        self.transactionId = argv['transactionId']
        self.registerId = argv['registerId']
        self.featurePoint = argv['featurePoint']
        self.parameter = argv['parameter']
