# -*- coding:utf-8 -*-


def log(msg, color="green"):
    if color == 'green':
        print("\033[1;32;46m" + str(msg) + "\033[0m")
    else:
        print("\033[1;31;40m" + str(msg) + "\033[0m")


def logerror(msg, color="red"):
    log(msg, color)


if __name__ == '__main__':
    log("hello")
    logerror("error")
