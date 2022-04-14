# -*- coding: UTF-8 -*-
# @Time     : 2020/08/26
# @Author   : mouyi
# @Version  : v1
# @Updated  : 2019/11/19
from datetime import date, timedelta

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')


@tag('default_value_check')
def default_value_check_010():
    """
    根据Object Model 进行默认值和权限检查
    """
    conn = None
    try:
        conn = KaifaDLMS()
        d = date(2020, 1, 1)
        t = datetime.time(0, 0, 0)
        dt = datetime.datetime.combine(d, t)
        day_interval = timedelta(1)
        min_interval = timedelta(0, 0, 0, 0, 15)
        for interval in range(1):
            dt = dt + day_interval
            C8Clock(conn=conn, obis=OBIS.C8_Clock).set_time(dt.__str__())
            # print(C8Clock(conn=conn, obis=OBIS.C8_Clock).get_time())
            # timeDiff(C8Clock(conn=conn, obis=OBIS.C8_Clock).get_time(),dt,1)
            # timedWait(5)
            deviceTime = C8Clock(conn=conn, obis=OBIS.C8_Clock).get_time()
            print(dt)
            print(deviceTime)
            print("----",interval)
            print(timeDiff(deviceTime, dt.__str__(), 1))
            timedWait(1)
            # if C7Profile(conn=conn, obis=OBIS.C7_LoadProfileWithPeriod2).get_buffer_by_range(dt.__str__(), dt.__str__()) == {}:
            #     print("Profile data is empty")
            # else:
            #     pass
            if C7Profile(conn=conn, obis=OBIS.C7_LoadProfileWithPeriod2).get_buffer_by_entry_with_list() == {}:
                print("Profile data is empty")
            else:
                pass
        return

        # C8Clock(conn=conn, obis=OBIS.C8_Clock).get_time()
        # C8Clock(conn=conn, obis=OBIS.C8_Clock).set_time()
        # return

        # read excel config
        # file_path = os.path.abspath(f"config/DefaultValue/{Singleton().Project}/user.yaml")
        # user_config = read_config(file_path)

        # read target data from excel
        # start_time = time.time()
        # defaultValueCheck(config=user_config, conn=conn)
        # end_time = time.time()
        # info(f"Total cost {end_time - start_time} seconds")
        # return 0
    except AttributeError as e:
        error(f"** Meet exception ** :\n{e}\n")
        return -1
    finally:
        disconnectDevice(conn)
