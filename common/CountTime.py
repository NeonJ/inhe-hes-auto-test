import datetime

def count_time(func):
    def took_up_time(*args, **kwargs):
        start_time = datetime.datetime.now()
        ret = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        took_up_time = (end_time - start_time).total_seconds()
        print(f"{func.__name__} execution took up time:{took_up_time}")
        return ret
    return took_up_time