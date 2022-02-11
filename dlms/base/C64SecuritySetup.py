# -*- coding: UTF-8 -*-

from libs.DllLoader import *
from libs.Singleton import *

from dlms.DlmsClass import *


class C64SecuritySetup(DlmsClass):
    """
    Security setup (class_id = 64, version = 1)
    """
    attr_index_dict = {
        1: "logical_name",
        2: "security_policy",
        3: "security_suite",
        4: "client_system_title",
        5: "server_system_title",
        6: "certificates"
    }

    action_index_dict = {
        1: "security_activate",
        2: "key_transfer",
        3: "key_agreement",
        4: "generate_key_pair",
        5: "generate_certificate_request",
        6: "import_certificate",
        7: "export_certificate_by_serial",
        8: "remove_certificate"
    }

    def __init__(self, conn, obis=None):
        super().__init__(conn, obis, classId=64)

    # Attribute of logical_name (No.1)
    @formatResponse
    def get_logical_name(self, dataType=False, response=None):
        """
        获取 logical_name 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            点分十进制形式的OBIS值
        """
        if response is None:
            response = self.getRequest(1)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toOBIS(ret[0]), ret[1]
        return hex_toOBIS(ret[0])

    @formatResponse
    def check_logical_name(self, ck_data):
        """
        检查 logical_name 的值

        :param ck_data:         点分十进制形式的OBIS值
        :return:                KFResult对象
        """
        ret = self.get_logical_name()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_logical_name(self, data):
        """
        设置 logical_name 的值

        :param data:         点分十进制形式的OBIS值
        :return:             KFResult对象
        """
        return self.setRequest(1, obis_toHex(data), "OctetString", data)

    # Attribute of security_policy (No.2)
    @formatResponse
    def get_security_policy(self, dataType=False, response=None):
        """
        获取 security_policy 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:    返回一个十进制整数 (整数的每个 bit 对应关系如下)

        Bit     Security policy
        0       unused, shall be set to 0,
        1       unused, shall be set to 0,
        2       authenticated request,
        3       encrypted request,
        4       digitally signed request,
        5       authenticated response,
        6       encrypted response,
        7       digitally signed response
        """
        if response is None:
            response = self.getRequest(2)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_security_policy(self, ck_data):
        """
        检查 security_policy 的值

        :param ck_data:      接收一个十进制整数
        :return:             返回 KFResult 对象
        """
        ret = self.get_security_policy()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_security_policy(self, data):
        """
        设置 security_policy

        :param data:    接收一个十进制整数
        :return:        返回 KFResult 对象
        """
        return self.setRequest(2, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of security_suite (No.3)
    @formatResponse
    def get_security_suite(self, dataType=False, response=None):
        """
        获取 security_suite

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:    返回一个十进制整数

        对应关系:
        0           AES-GCM-128 authenticated encryption and AES-128 key wrap
        1           AES-GCM-128 authenticated encryption, ECDSA P-256 digital signature, ECDH P-256 key agreement, SHA-256 hash, V.44 compression and AES-128 key wrap
        2           AES-GCM-256 authenticated encryption, ECDSA P-384 digital signature, ECDH P-384 key agreement, SHA-384 hash, V.44 compression and AES-256 key wrap
        3...15      reserved
        """
        if response is None:
            response = self.getRequest(3)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_security_suite(self, ck_data):
        """
        检查 security_suite

        :param ck_data:     接收一个十进制整数
        :return:    返回 KFResult 对象
        """
        ret = self.get_security_suite()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_security_suite(self, data):
        """
        设置 security_suite

        :param data:    接收一个十进制整数
        :return:    返回 KFResult 对象
        """
        return self.setRequest(3, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of client_system_title (No.4)
    @formatResponse
    def get_client_system_title(self, dataType=False, response=None):
        """
        获取 client_system_title

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:    返回一个字符串
        """
        if response is None:
            response = self.getRequest(4)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_client_system_title(self, ck_data):
        """
        检查 client_system_title

        :param ck_data:     接收一个字符串
        :return:            返回 KFResult 对象
        """
        ret = self.get_client_system_title()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_client_system_title(self, data):
        """
        设置 client_system_title

        :param data:    接收一个字符串
        :return:        返回 KFResult 对象
        """
        return self.setRequest(4, data, "OctetString", data)

    # Attribute of server_system_title (No.5)
    @formatResponse
    def get_server_system_title(self, dataType=False, response=None):
        """
        获取 server_system_title

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:    返回一个字符串
        """
        if response is None:
            response = self.getRequest(5)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_server_system_title(self, ck_data):
        """
        检查 server_system_title

        :param ck_data:     接收一个字符串
        :return:            返回 KFResult 对象
        """
        ret = self.get_server_system_title()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_server_system_title(self, data):
        """
        设置 server_system_title

        :param data:    接收一个字符串
        :return:        返回 KFResult 对象
        """
        return self.setRequest(5, data, "OctetString", data)

    # Attribute of get_certificates (No.6)
    @formatResponse
    def get_certificates(self, dataType=False, response=None):
        """
        获取 certificates

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:    返回一个字典
        {
            index : [certificate_entity, certificate_type, serial_number, issuer, subject, subject_alt_name]

            0: [0, 0, '008E6910F80B5B75CA', 'KFSubCA', '4B464D101000000C', ''],
            1: [2, 0, '00F46DC68943A8174D', 'KFRootCA', 'KFSubCA', ''],
            2: [2, 0, '0091436F9B5F9ECCC8', 'KFRootCA', 'KFRootCA', '']
        }
        """
        if response is None:
            response = self.getRequest(6)

        response = getStrucDataFromGetResp(response)
        if isinstance(response[0], dict):
            for value in response[0].values():
                for index, item in enumerate(value):
                    if index in [0, 1]:
                        value[index] = hex_toDec(item)
                    if index in [3, 4, 5]:
                        value[index] = hex_toAscii(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_certificates(self, ck_data):
        """
        检查 certificates
        :param ck_data:     接收一个字典 (可参考如下示例)
        :return:    返回 KFResult 对象

        ck_data:
        {
            0: [0, 0, '5B050EAE', '4D65746572732D4341', '4D65746572732D4341', ''],
            1: [2, 0, '5B050B68', '534D2D546573742D526F6F742D4341', '4D65746572732D4341', ''],
            2: [2, 0, '5B050938', '534D2D546573742D526F6F742D4341', '534D2D546573742D526F6F742D4341', '']
        }
        """
        return checkResponsValue(self.get_certificates(), ck_data)

    @formatResponse
    def set_certificates(self, data):
        """
        设置 certificates
        :param data:    接收一个字典参数 (可参考如下示例)
        :return:    返回 KFResult 对象

        data:
        {
            0: [0, 0, '5B050EAE', '4D65746572732D4341', '4D65746572732D4341', ''],
            1: [2, 0, '5B050B68', '534D2D546573742D526F6F742D4341', '4D65746572732D4341', ''],
            2: [2, 0, '5B050938', '534D2D546573742D526F6F742D4341', '534D2D546573742D526F6F742D4341', '']
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex in [0, 1]:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(6, array, "Array", data)

    # Method of security_activate (No.1)
    @formatResponse
    def act_security_activate(self, data=0):
        """
        Activates and strengthens the security policy

        :param data:    接收一个10进制整数 (可参考 'security_policy' 属性的参数设置)
        :return:        返回 KFResult 对象
        """
        return self.actionRequest(1, dec_toHexStr(data, 2), "Enum", data)

    # Method of key_transfer (No.2)
    @formatResponse
    def act_key_transfer(self, masterKey="", data=None, algorithm='AES', isUpdateEkey=True):
        """
        Used to transfer one or more symmetric keys.用于传递对称密钥 (akey, ekey, bkey, key 的修改)

        :param masterKey:     master Key
        :param data:  一个字典, 每一组值是一个list, 由'key_id' 和 'key_wrapped' 组成
                    {
                        index : [key_type, key_value]

                        0 : ['bkey', "000102030405060708090A0B0C0D0E0F"],
                        1 : ['akey', "FEB1FEB1FEB1FEB1FEB1FEB1FEB1FEB1"],
                        2 : ['ekey', "D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF"]
                        3 : ['kek',  "00112233445566778899AABBCCDDEEFF"]
                    }
        :param algorithm: 加密算法, 可选值有: [AES, CRC], 默认为: AES
        :param isUpdateEkey: 是否更新eKey到当前连接对象
        :return:    返回 KFResult 对象
        """
        keyMap = {
            'ekey': 0,
            'bkey': 1,
            'akey': 2,
            'kek': 3
        }
        if data is None:
            data = {}
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for index, item in enumerate(value):
                if index == 0:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(keyMap[item], 2))
                if index == 1:
                    if algorithm == 'AES':
                        etree.SubElement(struct, "OctetString").set("Value", encryptDataUseAES(masterKey, item))
                    else:
                        etree.SubElement(struct, "OctetString").set("Value", encryptDataUseCRC(masterKey, item))
        result = self.actionRequest(2, array, "Array", data)

        # 如果ekey修改成功, 则立即用新的ekey进行后续通信 (需要同时修改 ekey 和 dedicatedkey)
        if isUpdateEkey:
            if result.status:
                for value in data.values():
                    if 'ekey' in value:
                        self.conn.classDlms.CommunicationParam.SecInfo.UsingEncryptionKey = value[1]
                        self.conn.classDlms.CommunicationParam.AARQParam.DedicatedKey = value[1]
                        Singleton().EKey = value[1]
                    if 'akey' in value:
                        self.conn.classDlms.CommunicationParam.SecInfo.UsingAuthenticationKey = value[1]
                        Singleton().AKey = value[1]
                    if 'kek' in value:
                        self.conn.classDlms.CommunicationParam.SecInfo.UsingMasterKey = value[1]
                        Singleton().MasterKey = value[1]
        return result

    # Method of key_agreement (No.3)
    @formatResponse
    def act_key_agreement(self, data=None):
        """
        Used to agree on one or more symmetric keys using the key agreement algorithm as specified by the security
         suite. In the case of suites 1 and 2 the ECDH key agreement algorithm is used with the Ephemeral Unified
         Model C(2e, 0s, ECC CDH) scheme.

        :param data:    字典
        :return:        返回 KFResult 对象

        data ::= array key_agreement_data
        key_agreement_data ::= structure
        {
            key_id: enum:
            (0) global unicast encryption key,
            (1) global broadcast encryption key,
            (2) authentication key,
            (3) master key (KEK)
            key_data: octet-string
        }
        """
        if data is None:
            data = {}
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "Enum").set("Value", dec_toHexStr(subItem, 2))
                else:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.actionRequest(3, array, "Array", data)

    # Method of generate_key_pair (No.4)
    @formatResponse
    def act_generate_key_pair(self, data=0):
        """
        Generates an asymmetric key pair as required by the security suite. The data parameter
        identifies the usage of the key pair to be generated.

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.actionRequest(4, dec_toHexStr(data, 2), "Enum", data)

    # Method of generate_certificate_request (No.5)
    @formatResponse
    def act_generate_certificate_request(self, data=0):
        """
        When this method is invoked, the server sends the Certificate Signing Request (CSR) data
        that is necessary for a CA to generate a certificate for a server public key. The data
        parameter identifies the key pair for which the certificate will be requested.

        :param data:        十进制数
        :return:            KFResult 对象
        """
        return self.actionRequest(5, dec_toHexStr(data, 2), "Enum", data)

    # Method of import_certificate (No.6)
    @formatResponse
    def act_import_certificate(self, data=""):
        """
        Imports an X.509 v3 certificate of a public key.

        :param data:          字符串
        :return:              KFResult 对象
        """
        return self.actionRequest(6, data, "OctetString", data)

    # Method of export_certificate (No.7)
    @formatResponse
    def act_export_certificate_by_serial(self, serialNumber="", issuer=""):
        """
        基于 certificate_identification_serial 导出证书

        :param serialNumber:    序列号
        :param issuer:          发布机构
        :return:                KFResult 对象

        <ActionRequest>
          <ActionRequestNormal>
            <InvokeIdAndPriority Value="C1" />
            <MethodDescriptor>
              <ClassId Value="0040" />
              <InstanceId Value="00002B0000FF" />
              <MethodId Value="07" />
            </MethodDescriptor>
            <MethodInvocationParameters>
              <Structure Qty="0002" >
                <Enum Value="01" />
                <Structure Qty="0002" >
                  <OctetString Value="5B050EAE" />
                  <OctetString Value="4D65746572732D4341" />
                </Structure>
              </Structure>
            </MethodInvocationParameters>
          </ActionRequestNormal>
        </ActionRequest>
        """
        struct = etree.Element("Structure")
        struct.set("Qty", "0002")
        etree.SubElement(struct, "Enum").set("Value", "01")
        subStruct = etree.SubElement(struct, "Structure")
        subStruct.set("Qty", "0002")
        etree.SubElement(subStruct, "OctetString").set("Value", serialNumber)
        etree.SubElement(subStruct, "OctetString").set("Value", ascii_toHex(issuer))
        return self.actionRequest(7, struct, "structure", {'serialNumber': serialNumber, 'issuer': issuer})

    # Method of remove_certificate (No.8)
    @formatResponse
    def act_remove_certificate_by_serial(self, serialNumber="", issuer=""):
        """
        Removes X.509 v3 certificate in the server.

        :param serialNumber:    序列号
        :param issuer:          发布机构
        :return:                KFResult 对象
        """

        struct = etree.Element("Structure")
        struct.set("Qty", "0002")
        etree.SubElement(struct, "Enum").set("Value", "01")
        subStruct = etree.SubElement(struct, "Structure")
        subStruct.set("Qty", "0002")
        etree.SubElement(subStruct, "OctetString").set("Value", serialNumber)
        etree.SubElement(subStruct, "OctetString").set("Value", ascii_toHex(issuer))
        return self.actionRequest(8, struct, "structure", {'serialNumber': serialNumber, 'issuer': issuer})
