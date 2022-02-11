# -*- coding: UTF-8 -*-
# @Time     : 2020/08/14
# @Author   : mouyi
# @Version  : v1
# @Updated  : 0000/00/00
from .comm import *


@tag('get_data')
def get_data_010():
    """
    获取OBIS Get Response结果以及数据类型
    """
    conn = None
    try:
        # read excel config
        file_path = os.path.abspath(f"conf/DefaultValue/{Singleton().Project}/user.yaml")
        user_config = read_config(file_path)

        # read target data from excel
        start_time = time.time()
        conn = KaifaDLMS()

        readDataByAdmin(config=user_config, conn=conn)

        end_time = time.time()
        info(f"Total cost {end_time - start_time} seconds")
        return 0
    except (AttributeError, ValueError) as e:
        error(f"** Meet exception ** :\n{e}\n")
        return -1
    finally:
        disconnectDevice(conn)
