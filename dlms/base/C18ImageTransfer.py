# -*- coding: UTF-8 -*-

import random

from dlms.DlmsClass import *


class C18ImageTransfer(DlmsClass):
    attr_index_dict = {
        1: "logical_name",
        2: "image_block_size",
        3: "image_transferred_blocks_status",
        4: "image_first_not_transferred_block_number",
        5: "image_transfer_enabled",
        6: "image_transfer_status",
        7: "image_to_activate_info"
    }

    action_index_dict = {
        1: "image_transfer_initiate",
        2: "image_block_transfer",
        3: "image_verify",
        4: "image_activate"
    }

    ImageTransferStatusMap = {
        0: "Image transfer not initiated",
        1: "Image transfer initiated",
        2: "Image verification initiated",
        3: "Image verification successful",
        4: "Image verification failed",
        5: "Image activation initiated",
        6: "Image activation successful",
        7: "Image activation failed",
    }

    def __init__(self, conn, obis):
        super().__init__(conn, obis, classId=18)

    # Attribute of logical_name
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

        :param ck_data:     期望值 (非16进制的各种形式的OBIS)
        :return:            KFResult 对象
        """
        ret = self.get_logical_name()
        if ret.lower() == ck_data.strip().lower():
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_logical_name(self, data):
        """
        设置 logical_name 的值

        :param data:        期望值 (非16进制的各种形式的OBIS)
        :return:            返回一个KFResult对象
        """
        return self.setRequest(1, obis_toHex(data), "OctetString", data)

    # Attribute of image_block_size
    @formatResponse
    def get_image_block_size(self, dataType=False, response=None):
        """
        获取 image_block_size 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            double-long-unsigned
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
    def check_image_block_size(self, ck_data):
        """
        检查 image_block_size 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        ret = self.get_image_block_size()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_image_block_size(self, data):
        """
        设置 image_block_size 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(2, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of image_transferred_blocks_status
    @formatResponse
    def get_image_transferred_blocks_status(self, dataType=False, response=None):
        """
        获取 image_transferred_blocks_status 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字符串
        """
        if response is None:
            response = self.getRequest(3)

        ret = getSingleDataFromGetResp(response)
        if dataType:
            return ret
        return ret[0]

    @formatResponse
    def check_image_transferred_blocks_status(self, ck_data):
        """
        检查 image_transferred_blocks_status 的值

        :param ck_data:     字符串
        :return:            KFResult对象
        """
        ret = self.get_image_transferred_blocks_status()
        if ret == ck_data:
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_image_transferred_blocks_status(self, data):
        """
        设置 image_transferred_blocks_status 的值

        :param data:        字符串
        :return:            KFResult对象
        """
        return self.setRequest(3, data, "BitString", data)

    # Attribute of image_first_not_transferred_block_number
    @formatResponse
    def get_image_first_not_transferred_block_number(self, dataType=False, response=None):
        """
        获取 image_first_not_transferred_block_number 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(4)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]
        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_image_first_not_transferred_block_number(self, ck_data):
        """
        检查 image_first_not_transferred_block_number 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        ret = self.get_image_first_not_transferred_block_number()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_image_first_not_transferred_block_number(self, data):
        """
        设置 image_first_not_transferred_block_number 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(4, dec_toHexStr(data, 8), "DoubleLongUnsigned", data)

    # Attribute of image_transfer_enabled
    @formatResponse
    def get_image_transfer_enabled(self, dataType=False, response=None):
        """
        获取 image_transfer_enabled 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(5)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]
        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_image_transfer_enabled(self, ck_data):
        """
        检查 image_transfer_enabled 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        ret = self.get_image_transfer_enabled()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_image_transfer_enabled(self, data):
        """
        设置 image_transfer_enabled 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(5, dec_toHexStr(data, 2), "Bool", data)

    # Attribute of image_transfer_status
    @formatResponse
    def get_image_transfer_status(self, dataType=False, response=None):
        """
        获取 image_transfer_status 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            十进制数
        """
        if response is None:
            response = self.getRequest(6)

        ret = getSingleDataFromGetResp(response)
        if ret[0] in data_access_result:
            if dataType:
                return ret
            return ret[0]

        if dataType:
            return hex_toDec(ret[0]), ret[1]
        return hex_toDec(ret[0])

    @formatResponse
    def check_image_transfer_status(self, ck_data):
        """
        检查 image_transfer_status 的值

        :param ck_data:     十进制数
        :return:            KFResult对象
        """
        ret = self.get_image_transfer_status()
        if int(ret) == int(ck_data):
            return KFResult(True, "")
        return KFResult(False, f"{ret} not equal to {ck_data}")

    @formatResponse
    def set_image_transfer_status(self, data):
        """
        设置 image_transfer_status 的值

        :param data:        十进制数
        :return:            KFResult对象
        """
        return self.setRequest(6, dec_toHexStr(data, 2), "Enum", data)

    # Attribute of image_to_activate_info
    @formatResponse
    def get_image_to_activate_info(self, dataType=False, response=None):
        """
        获取 image_to_activate_info 的值

        :param dataType:    是否返回数据类型， 默认False不返回
        :param response:    如果给定response, 则直接用response转换格式并返回； 如果未给定response，则从电表获取
        :return:            字典
        """
        if response is None:
            response = self.getRequest(7)

        response = getStrucDataFromGetResp(response)
        if response[0] in data_access_result:
            if dataType:
                return response
            return response[0]
        for value in response[0].values():  # list: level2
            for index, item in enumerate(value):
                if index == 0:
                    value[index] = hex_toDec(item)
        if dataType:
            return response
        return response[0]

    @formatResponse
    def check_image_to_activate_info(self, ck_data):
        """
        检查 image_to_activate_info 的值

        :param ck_data:     期望值 (字典)
        :return:            KFResult 对象

        ck_data ::= structure
        {
            image_to_activate_size: double-long-unsigned,
            image_to_activate_identification: octet-string,
            image_to_activate_signature: octet-string
        }
        """
        return checkResponsValue(self.get_image_to_activate_info(), ck_data)

    @formatResponse
    def set_image_to_activate_info(self, data):
        """
        设置 image_to_activate_info 的值

        :param data:        期望值 (字典)
        :return:            KFResult 对象

        data ::= structure
        {
            image_to_activate_size: double-long-unsigned,
            image_to_activate_identification: octet-string,
            image_to_activate_signature: octet-string
        }
        """
        array = etree.Element("Array")
        array.set("Qty", dec_toHexStr(len(data), 4))
        for value in data.values():
            struct = etree.SubElement(array, "Structure")
            struct.set("Qty", dec_toHexStr(len(value), 4))
            for subIndex, subItem in enumerate(value):
                if subIndex == 0:
                    etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(subItem, 8))
                if subIndex == 1 or subIndex == 2:
                    etree.SubElement(struct, "OctetString").set("Value", subItem)
        return self.setRequest(7, array, "Array", data)

    # Method of image_transfer_initiate
    @formatResponse
    def act_image_transfer_initiate(self, imageIdentifier="", imageSize=0, imgPath=""):
        """
        Initializes the Image transfer process.

        data ::= structure
        {
            image_identifier: octet-string,
            image_size: double-long-unsigned
        }
        :param imageIdentifier:
        :param imageSize:
        :param imgPath:
        :return:                KFResult对象
        """
        # Get FileSize
        if os.path.exists(imgPath):
            imageSize = os.path.getsize(imgPath)

        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(2, length=4))
        etree.SubElement(struct, "OctetString").set("Value", ascii_toHex(imageIdentifier))
        etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(imageSize, length=8))
        return self.actionRequest(1, struct, "structure",
                                  {'imageIdentifier': imageIdentifier, 'imageSize': imageSize, 'imgPath': imgPath})

    # Method of image_block_transfer
    @formatResponse
    def act_image_block_transfer(self, imageBlockNumber=0, imageBlockValue=""):
        """
        Transfers one block of the Image to the server.

        data ::= structure
        {
            image_block_number: double-long-unsigned,
            image_block_value: octet-string
        }
        :param imageBlockNumber:       十进制数
        :param imageBlockValue:        字符串
        :return:                       KFResult对象
        """

        # 通过 threading.Event 实现线程间通信
        from libs.Singleton import Singleton
        for i in range(60):
            if Singleton().Pause.is_set():
                time.sleep(1)

        struct = etree.Element("Structure")
        struct.set("Qty", dec_toHexStr(2, length=4))
        etree.SubElement(struct, "DoubleLongUnsigned").set("Value", dec_toHexStr(imageBlockNumber, length=8))
        etree.SubElement(struct, "OctetString").set("Value", binascii.b2a_hex(imageBlockValue))
        # return self.actionRequest(2, struct, "structure", {'imageBlockNumber' : imageBlockNumber, 'imageBlockValue' : imageBlockValue})
        return self.actionRequest(2, struct, "structure")

    # Method of image_verify
    @formatResponse
    def act_image_verify(self, data=0):
        """
        Verifies the integrity of the Image before activation.

        :param data:   十进制数
        :return:       KFResult对象
        """
        return self.actionRequest(3, dec_toHexStr(data, 2), "Integer", data)

    # Method of image_activate
    @formatResponse
    def act_image_activate(self, data=0):
        """
        Activates the Image.

        :param data:    十进制数
        :return:        KFResult对象
        """
        return self.actionRequest(4, dec_toHexStr(data, 2), "Integer", data)

    # ==================================================================================================#

    # Business
    @staticmethod
    def __calcBlockNum(fileSize, blockSize):
        mod = fileSize % blockSize
        return int(fileSize / blockSize) if mod == 0 else int(fileSize / blockSize) + 1

    def __act_image_block_transfer(self, imageBlockNumber, imageBlockValue):
        try:
            return self.act_image_block_transfer(imageBlockNumber, imageBlockValue)
        except Exception as ex:
            return KFResult(False, f'{ex}')

    # Business
    def imageTransfer(self, **argv):
        """
        The Image transfer usually takes place in several steps:

        • Step 1: (Optional): Get ImageBlockSize
        • Step 2: Client initiates Image transfer
        • Step 3: Client transfers ImageBlocks
        • Step 4: Client checks completeness of the Image
        • Step 5: Server verifies the Image (Initiated by the client or on its own)
        • Step 6 (Optional): Client checks the information on the images to activate
        • Step 7: Server activates the Image(s) (Initiated by the client or on its own)

        :param imgPath:                     image stored path
        :param imgId:                       image identifier
        :param blocksize:                   block size, default value: current block size that set in device
        :param stopBlockIndex:              block index, stop image transfer when reached the specified number of packages
        :param randomRepeatedBlock:         transfer one of block repeatedly, default value: FAlse
        :param randomLostBlock:             lost one block of images randomly, default value: False
        :param retransmission:              1) - image_first_not_transferred; 2) - image_transferred_blocks_status; default value: 1
        :param retransloop:                 retransmission loop, default value: 10
        :param transferEnabled:             enable image transfer, defalt value: True, options: True, False
        :param reTransferEnabled:           enable image reTransfer, defalt value: True, options: True, False
        :param verify:                      verify image, default value: True
        :param activate:                    active image immediately, default value: True
        :return:                            KFResult对象
        """
        imgPath = dealWithLongerPath(argv['imgPath'])
        imgId = argv.get('imgId', '')
        blockSize = argv.get("blocksize", None)
        stopBlockIndex = argv.get("stopBlockIndex", None)
        randomRepeatedBlock = argv.get('randomRepeatedBlock', False)
        randomLostBlock = argv.get('randomLostBlock', False)
        retransmission = argv.get('retransmission', 1)
        retransloop = argv.get('retransloop', 10)
        # 控制开关
        transferEnabled = argv.get('transferEnabled', True)
        reTransferEnabled = argv.get('reTransferEnabled', True)
        verify = argv.get('verify', True)
        activate = argv.get('activate', True)

        # Get FileSize
        fileSize = os.path.getsize(imgPath)

        # 如果没有指定blockSize, 则使用当前系统设置的blockSize
        if not blockSize:
            blockSize = self.get_image_block_size()

        # set_image_transfer_enabled
        if transferEnabled:
            result = self.set_image_transfer_enabled(1)
            if not result.status:
                return KFResult(False, "image_transfer_enabled = False")

        # initiate_transfer
        result = self.act_image_transfer_initiate(imgId, fileSize)
        if not result.status:
            return KFResult(False, f"image_transfer_init failed, reason: {result.result}")

        # get_image_transfer_status
        result = self.get_image_transfer_status()
        if int(result) != 1:  # 1 -> Image transfer initiated
            return KFResult(False,
                            f"image_transfer_status error: {C18ImageTransfer.ImageTransferStatusMap[int(result)]}")

        # calculate total block numbers
        blockNum = self.__calcBlockNum(fileSize, blockSize)

        # randomly transmit one block repeatedly
        randomRepeatedBlockIndex = -1
        if randomRepeatedBlock:
            randomRepeatedBlockIndex = random.randint(1, blockNum)

        # randomly lost one block
        randomLostBlockIndex = -1
        if randomLostBlock:
            randomLostBlockIndex = random.randint(1, blockNum)

        # transfer_image  (blockIndex 从 0 开始)
        with open(imgPath, "rb") as fp:
            for blockIndex in range(blockNum):
                # 达到条件后, 停止升级
                if stopBlockIndex is not None and blockIndex == int(stopBlockIndex):
                    return KFResult(True, f'stop image transfer successfully')

                # 丢弃任意一个block (用于构造随机一个block传送失败的场景)
                if blockIndex == randomLostBlockIndex:
                    continue

                # 传送 firmware block
                info(f"transfer {blockIndex} of {blockNum - 1} ...")
                fp.seek(blockIndex * blockSize)
                blockData = fp.read(blockSize)
                result = self.__act_image_block_transfer(blockIndex, blockData)
                if not result.status:
                    RetryFlag = False
                    for i in range(3):
                        result = self.__act_image_block_transfer(blockIndex, blockData)
                        if result.status:
                            RetryFlag = True
                            break
                    if not RetryFlag:
                        return KFResult(False, f"transfer_image failed, blockIndex: {blockIndex}")

                # 重传任意一个block (用于构造同一个block重复传送多次的场景)
                if blockIndex == randomRepeatedBlockIndex:
                    info(f"**repeatedly** transfer {blockIndex} of {blockNum - 1} ...")
                    result = self.__act_image_block_transfer(blockIndex, blockData)
                    if not result.status:
                        RetryFlag = False
                        for i in range(3):
                            result = self.__act_image_block_transfer(blockIndex, blockData)
                            if result.status:
                                RetryFlag = True
                                break
                        if not RetryFlag:
                            return KFResult(False, f"**repeatedly** transfer_image failed, blockIndex: {blockIndex}")

        # 重传丢失的block
        if reTransferEnabled:
            # Retransmission: image_first_not_transferred
            # 对每个一个block尝试重传'retransloop'次, 如果某一个block仍然传送失败, 则直接退出(其余丢失的block也不再重传)
            if int(retransmission) == 1:
                firstNotTransferredIndex = self.get_image_first_not_transferred_block_number()
                while firstNotTransferredIndex < blockNum - 1:  # firstNotTransferredIndex 从 0 开始
                    retransResult = None
                    with open(imgPath, "rb") as fp:
                        fp.seek(firstNotTransferredIndex * blockSize)
                        blockData = fp.read(blockSize)
                        # 最多重传'retransloop'次
                        for loop in range(int(retransloop)):
                            info(f"retransfer {firstNotTransferredIndex} of {blockNum - 1} ...")
                            retransResult = self.__act_image_block_transfer(firstNotTransferredIndex, blockData)
                            if retransResult.status:
                                break
                        if not retransResult.status:
                            return KFResult(False,
                                            f"transfer_missing_blocks failed, blockIndex: {firstNotTransferredIndex}")
                    # 获取下一个重传block number
                    firstNotTransferredIndex = self.get_image_first_not_transferred_block_number()

                # 经过retransloop次重传后, 仍有部分block传输失败
                if firstNotTransferredIndex < blockNum - 1:
                    return KFResult(False, f"transfer_missing_blocks failed, blockIndex: {firstNotTransferredIndex}")

            # Retransmission: image_transferred_blocks_status
            if int(retransmission) == 2:
                transferredBlocksStatus = self.get_image_transferred_blocks_status()
                if len(transferredBlocksStatus) < blockNum:
                    return KFResult(False, "Server received image blocks less than transferred blocks")

                # transfer_missing_blocks
                for loop in range(int(retransloop)):
                    if transferredBlocksStatus.find("0") > -1:
                        with open(imgPath, "rb") as fp:
                            for blockIndex in range(blockNum + 1):
                                if int(transferredBlocksStatus[blockIndex]) == 0:
                                    fp.seek((blockIndex - 1) * blockSize)
                                    info(f"retransfer {blockIndex} of {blockNum} ...")
                                    self.__act_image_block_transfer(blockIndex, fp.read(blockSize))
                    else:
                        break
                    # 获取下一次重传的所有block number
                    transferredBlocksStatus = self.get_image_transferred_blocks_status()

                # 经过retransloop次重传后, 仍有部分block传输失败
                if transferredBlocksStatus.find("0") > -1:
                    return KFResult(False, f"transfer_missing_blocks failed, blockStatus: {transferredBlocksStatus}")

        # verify_image
        if verify:
            self.act_image_verify(0)
            # get_image_transfer_status
            image_transfer_status = -1
            for i in range(19):  # 尝试10轮, 每轮间隔15s
                time.sleep(8)
                image_transfer_status = self.get_image_transfer_status()
                if image_transfer_status == 3:  # 3 -> Image verification successful
                    break
                if image_transfer_status == 4:
                    return KFResult(False,
                                    f"image_transfer_status failed, image_transfer_status: {C18ImageTransfer.ImageTransferStatusMap[4]}")

            if image_transfer_status != 3:
                return KFResult(False,
                                f"image_transfer_status failed, image_transfer_status: {C18ImageTransfer.ImageTransferStatusMap[image_transfer_status]}")

        # active_image
        if activate:
            self.act_image_activate(0)

        return KFResult(True, '')

    def imageTransferResume(self, **argv):
        """
        续传image

        :param imgPath:                     image stored path
        :param retransmission:              1) - image_first_not_transferred; 2) - image_transferred_blocks_status; default value: 1
        :param retransloop:                 retransmission loop, default value: 10
        :param verify:                      verify image, default value: True
        :param activate:                    active image immediately, default value: True
        :return:
        """
        imgPath = dealWithLongerPath(argv['imgPath'])
        retransmission = argv.get('retransmission', 1)
        retransloop = argv.get('retransloop', 10)
        verify = argv.get('verify', True)
        activate = argv.get('activate', True)

        # Get FileSize
        fileSize = os.path.getsize(imgPath)

        # Get blockSize
        blockSize = self.get_image_block_size()

        # calculate total block numbers
        blockNum = self.__calcBlockNum(fileSize, blockSize)

        # Retransmission: image_first_not_transferred
        # 对每个一个block尝试重传'retransloop'次, 如果某一个block仍然传送失败, 则直接退出(其余丢失的block也不再重传)
        if int(retransmission) == 1:
            firstNotTransferredIndex = self.get_image_first_not_transferred_block_number()
            while firstNotTransferredIndex < blockNum:  # firstNotTransferredIndex 从 0 开始
                retransResult = None
                with open(imgPath, "rb") as fp:
                    fp.seek(firstNotTransferredIndex * blockSize)
                    blockData = fp.read(blockSize)
                    # 最多重传'retransloop'次
                    for loop in range(int(retransloop)):
                        info(f"retransfer {firstNotTransferredIndex} of {blockNum - 1} ...")
                        retransResult = self.__act_image_block_transfer(firstNotTransferredIndex, blockData)
                        if retransResult.status:
                            break
                    if not retransResult.status:
                        return KFResult(False,
                                        f"transfer_missing_blocks failed, blockIndex: {firstNotTransferredIndex}")
                # 获取下一个重传block number
                firstNotTransferredIndex = self.get_image_first_not_transferred_block_number()

            # 经过retransloop次重传后, 仍有部分block传输失败
            if firstNotTransferredIndex < blockNum - 1:
                return KFResult(False, f"transfer_missing_blocks failed, blockIndex: {firstNotTransferredIndex}")

        # Retransmission: image_transferred_blocks_status
        if int(retransmission) == 2:
            transferredBlocksStatus = self.get_image_transferred_blocks_status()
            if len(transferredBlocksStatus) < blockNum:
                return KFResult(False, "Server received image blocks less than transferred blocks")

            # transfer_missing_blocks
            for loop in range(int(retransloop)):
                if transferredBlocksStatus.find("0") > -1:
                    with open(imgPath, "rb") as fp:
                        for blockIndex in range(blockNum + 1):
                            if int(transferredBlocksStatus[blockIndex]) == 0:
                                fp.seek((blockIndex - 1) * blockSize)
                                info(f"retransfer {blockIndex} of {blockNum} ...")
                                self.__act_image_block_transfer(blockIndex, fp.read(blockSize))
                else:
                    break
                # 获取下一次重传的所有block number
                transferredBlocksStatus = self.get_image_transferred_blocks_status()

            # 经过retransloop次重传后, 仍有部分block传输失败
            if transferredBlocksStatus.find("0") > -1:
                return KFResult(False, f"transfer_missing_blocks failed, blockStatus: {transferredBlocksStatus}")

        # verify_image
        if verify:
            self.act_image_verify(0)
            # get_image_transfer_status
            image_transfer_status = -1
            for i in range(19):  # 尝试10轮, 每轮间隔15s
                time.sleep(8)
                image_transfer_status = self.get_image_transfer_status()
                if image_transfer_status == 3:  # 3 -> Image verification successful
                    break
                if image_transfer_status == 4:
                    return KFResult(False,
                                    f"image_transfer_status failed, image_transfer_status: {C18ImageTransfer.ImageTransferStatusMap[4]}")

            if image_transfer_status != 3:
                return KFResult(False,
                                f"image_transfer_status failed, image_transfer_status: {C18ImageTransfer.ImageTransferStatusMap[image_transfer_status]}")

        # active_image
        if activate:
            self.act_image_activate(0)

        return KFResult(True, '')

    def transferSpecifiedBlocks(self, imgPath, imgId, blockList):
        """
        传输指定的几个包

        :param self:    传输对象
        :param imgPath:        升级包路径
        :param imgId:          image identifier
        :param blockList:      需要传输包的序号
        :return:               KFResult对象
        """
        # Get FileSize
        fileSize = os.path.getsize(imgPath)

        # 如果没有指定blockSize, 则使用当前系统设置的blockSize
        blockSize = self.get_image_block_size()

        # set_image_transfer_enabled
        result = self.set_image_transfer_enabled(1)
        if not result.status:
            return KFResult(False, "image_transfer_enabled = False")

        # initiate_transfer
        result = self.act_image_transfer_initiate(imgId, fileSize)
        if not result.status:
            return KFResult(False, f"image_transfer_init failed, reason: {result.result}")

        # get_image_transfer_status
        result = self.get_image_transfer_status()
        if int(result) != 1:  # 1 -> Image transfer initiated
            return KFResult(False,
                            f"image_transfer_status error: {C18ImageTransfer.ImageTransferStatusMap[int(result)]}")

        # calculate total block numbers
        blockNum = self.__calcBlockNum(fileSize, blockSize)

        # transfer_image  (blockIndex 从 0 开始)
        with open(imgPath, "rb") as fp:
            for blockIndex in blockList:
                # 传送 firmware block
                info(f"transfer {blockIndex} of {blockNum - 1} ...")
                fp.seek(blockIndex * blockSize)
                blockData = fp.read(blockSize)
                result = self.__act_image_block_transfer(blockIndex, blockData)
                if not result.status:
                    RetryFlag = False
                    for i in range(3):
                        result = self.__act_image_block_transfer(blockIndex, blockData)
                        if result.status:
                            RetryFlag = True
                            break
                    if not RetryFlag:
                        return KFResult(False, f"transfer_image failed, blockIndex: {blockIndex}")
        return KFResult(True, '')
