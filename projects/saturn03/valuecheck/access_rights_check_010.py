# -*- coding: UTF-8 -*-
# @Time     : 2019/07/30
# @Author   : mouyi
# @Version  : v1
# @Updated  : 0000/00/00
from .comm import *

@tag('access_rights_check')
def access_rights_check_010():
    """
    根据Object Model 进行默认值和权限检查
    """
    conn = None
    try:
        # read excel config
        file_path = os.path.abspath(f"conf/DefaultValue/{Singleton().Project}/user.yaml")
        user_config = read_config(file_path)

        # read target data from excel
        start_time = time.time()
        conn = KaifaDLMS()
        accessRightsCheck(config=user_config, conn=conn)
        end_time = time.time()
        info(f"Total cost {end_time - start_time} seconds")
        return 0
    except AttributeError as e:
        error(f"** Meet exception ** :\n{e}\n")
        return -1
    finally:
        disconnectDevice(conn)
