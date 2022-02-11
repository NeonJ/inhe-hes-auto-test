# -*- coding:utf-8 -*-

import datetime
import logging
import logging.handlers
import os

__all__ = [
    'kfLog',
    'debug',
    'info',
    'warn',
    'error',
    'LogConstant'
]


class LogConstant:
    """日志模块常量"""
    LOG_DIR = 'logs'  # 日志路径
    LOG_DETAIL_NAME = 'detail.log'  # 用例执行日志
    LOG_REPORT_NAME = 'report.log'  # 用例执行日志
    MAX_LOG_SIZE_BYTES = 1024 * 1024 * 40  # 日志文件大小(20M)
    MAX_LOG_NUM = 10  # 日志文件保存数量

    # 写入report文件的日志格式
    # LOG_DETAIL_FORMAT = '%(asctime)s [%(filename)-20s lineno:%(lineno)-4d] %(levelname)5s : %(message)s'
    # LOG_REPORT_FORMAT = '%(asctime)s [%(filename)-20s lineno:%(lineno)-4d] %(levelname)5s : %(message)s'
    LOG_REPORT_FORMAT = '%(asctime)s : %(message)s'
    LOG_REPORT_PLACEHOLDER = 26


def create_stream_handler(level):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(LogConstant.LOG_REPORT_FORMAT)
    handler.setFormatter(formatter)
    return handler


# def create_detail_rotating_handler(path, level):
#     mkdirs(path)
#     handler = logging.handlers.RotatingFileHandler(path,
#                                                    maxBytes=LogConstant.MAX_LOG_SIZE_BYTES,
#                                                    backupCount=LogConstant.MAX_LOG_NUM)
#     handler.setLevel(level)
#     formatter = logging.Formatter(LogConstant.LOG_DETAIL_FORMAT)
#     handler.setFormatter(formatter)
#     return handler


def create_report_rotating_handler(path, level):
    mkdirs(path)
    handler = logging.handlers.RotatingFileHandler(path,
                                                   maxBytes=LogConstant.MAX_LOG_SIZE_BYTES,
                                                   backupCount=LogConstant.MAX_LOG_NUM)
    handler.setLevel(level)
    formatter = logging.Formatter(LogConstant.LOG_REPORT_FORMAT)
    handler.setFormatter(formatter)
    return handler


def mkdirs(path):
    path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)


# from PyQt5.QtCore import QObject, pyqtSignal
# class PyQtHandler(QObject):
#     msg = pyqtSignal(str)


class KFLog(object):

    def __init__(self):
        # self.level = logging.INFO
        self.level = logging.DEBUG
        self.datetime = datetime.datetime.now().strftime("%m%d_%H%M%S")
        self.log_detail_path = os.path.join(LogConstant.LOG_DIR, self.datetime, LogConstant.LOG_DETAIL_NAME)
        self.log_report_path = os.path.join(LogConstant.LOG_DIR, self.datetime, LogConstant.LOG_REPORT_NAME)
        self._reportLogger = None
        self._dlmsLogger = None

        # GUI日志句柄
        # self.pyqtHandler = PyQtHandler()

    @property
    def kfLog(self):
        if self._reportLogger:
            return self._reportLogger
        self._reportLogger = logging.getLogger("kfLog")
        self._reportLogger.addHandler(create_stream_handler(self.level))
        # self._reportLogger.addHandler(create_detail_rotating_handler(self.log_detail_path, self.level))
        self._reportLogger.addHandler(create_report_rotating_handler(self.log_report_path, self.level))
        self._reportLogger.setLevel(self.level)
        return self._reportLogger


kfLog = KFLog()


# debug = kfLog.kfLog.debug
# info = kfLog.kfLog.info
# warn = kfLog.kfLog.warning
# error = kfLog.kfLog.error


def sendSignal(msg):
    try:
        kfLog.pyqtHandler.msg.emit(str(msg))
    except RuntimeError:
        pass


def debug(msg, *args, **kwargs):
    sendSignal(msg)
    return kfLog.kfLog.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    msg = msg.replace(r"\u", "")
    sendSignal(msg)
    try:
        return kfLog.kfLog.info(msg, *args, **kwargs)
    except:
        pass


def warn(msg, *args, **kwargs):
    sendSignal(msg)
    return kfLog.kfLog.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    sendSignal(msg)
    return kfLog.kfLog.error(msg, *args, **kwargs)
