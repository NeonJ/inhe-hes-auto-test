# -*- coding: UTF-8 -*-
# @Time     : 2020/08/26
# @Author   : jiannancao
# @Version  : v1
# @Updated  : 2021/08/25
from datetime import date, time, timedelta

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')


@tag('lp_capacity')
def lp_capacity_010():
    """
    根据Object Model 进行默认值和权限检查
    """
    conn = None
    try:
        conn = KaifaDLMS()

        start_time = time.time()

        d = date(2020, 8, 24)
        t = datetime.time(0, 0, 0)
        dt = datetime.datetime.combine(d, t)
        # day_interval = timedelta(1)
        min_interval = timedelta(0, 0, 0, 0, 15)
        for interval in range(1):
            dt = dt + min_interval
            C8Clock(conn=conn, obis=OBIS.C8_Clock).get_time()
            print(dt)

        # C8Clock(conn=conn, obis=OBIS.C8_Clock).get_time()
        # C8Clock(conn=conn, obis=OBIS.C8_Clock).set_time()
        # return

        # read excel config
        # file_path = os.path.abspath(f"config/DefaultValue/{Singleton().Project}/user.yaml")

        # read target data from excel

        end_time = time.time()
        info(f"Total cost {end_time - start_time} seconds")
        return 0
    except AttributeError as e:
        error(f"** Meet exception ** :\n{e}\n")
        return -1
    finally:
        disconnectDevice(conn)
