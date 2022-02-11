# -*- coding: UTF-8 -*-

import functools
import sys
import traceback

from .DataFormatAPI import KFResult
from .KFLog import *


def formatDict(data, isInputData=False):
    """
    Format data

    :param data:            需要格式化的数据
    :param isInputData:     用于区分data是输入的参数，还是电表的相应数据
    :return:                格式化之后的字典
    """
    leftAlign = ' ' * LogConstant.LOG_REPORT_PLACEHOLDER

    result = data
    if isinstance(data, dict):
        if len(data) > 0:
            result = "\n{0}{{\n".format(leftAlign)
            for key, value in data.items():
                result += f"{leftAlign}    {key} : {value}\n"
            result += "{0}}}".format(leftAlign)
        else:
            result = data

    if isinstance(data, list):
        if len(data) > 0:
            result = "\n{0}[\n".format(leftAlign)
            for item in data:
                result += f"{leftAlign}    {item}\n"
            result += "{0}]".format(leftAlign)
        else:
            result = data

    if isinstance(data, KFResult):
        if data.status:
            result = 'Succeeded'
        else:
            result = data.result

    if isInputData:
        return result

    # Check方法默认会返回两次 ## Response ##
    ### Check 成功的时候直接返回空
    if len(str(result).strip()) == 0:
        return ''

    ### Check 失败的时候返回 ## Failed Reason ##
    if 'not equal to' in str(result):
        return "## Failed Reason ## : " + f'(Acutal Value) {result} (Expected Value)'

    return "## Response ## : " + str(result)


def formatResponse(func):
    """
    格式化目标函数返回结果

    :param func:         目标函数
    :return:             执行目标函数并格式化返回数据
    """

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        # debug(f'** {func.__code__.co_filename} -- "{func.__name__}" **')
        #
        # # 判断第一个参数是否为self对象 # getattr(args[0].__class__, func.__name__)
        # try:
        #     import inspect
        #     inspect.isclass(args[0])
        #     arglist = args[1:]
        # except AttributeError:
        #     arglist = args
        #
        # # 打印参数
        # if len(arglist) > 0:
        #     if func.__name__ not in ['act_image_block_transfer']:
        #         debug(f'** Arguments: {arglist}**')

        try:
            response = func(*args, **kwargs)
            if isinstance(response, KFResult):
                # info(formatDict(str(response.result)))
                info(formatDict(response))
            else:
                # 处理 respoonse 中包含`数据内容` 和 `数据类型` 的情况
                if isinstance(response, (tuple, list)):
                    info(formatDict(response[0]))
                else:
                    info(formatDict(response))
            return response

        except Exception as ex:
            error(f'** Exception: {ex} **')
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
            return "".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj))

    return wrap


# def loggerFuncName(func):
#     """
#     打印目标函数名字以及参数
#
#     :param func:
#     :return:              执行目标函数并打印函数名称以及参数
#     """
#     @functools.wraps(func)
#     def wrap(*args, **kwargs):
#         info(f'** {func.__code__.co_filename} -- "{func.__name__}" **')
#
#         # className = str(func.__module__).split(".")[-1]
#         # funcName = str(func.__code__.co_name)
#         # method, attr = funcName.split('_', maxsplit=1)
#         # info(f'## Method Info ##: Method: "{str(method).capitalize()}", Object: "{className, obis, attr}"')
#
#         # 判断第一个参数是否为self对象 # getattr(args[0].__class__, func.__name__)
#         try:
#             import inspect
#             inspect.isclass(args[0])
#             arglist = args[1:]
#         except AttributeError:
#             arglist = args
#
#         # 打印参数
#         if len(arglist) > 0:
#             if func.__name__ not in ['act_image_block_transfer']:
#                 info(f'** Arguments: {arglist}**')
#
#         try:
#             return func(*args, **kwargs)
#         except Exception as ex:
#             error(f'** Exception: {ex} **')
#             exc_type, exc_value, exc_traceback_obj = sys.exc_info()
#             error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj, limit=3)))
#
#     return wrap


def tag(*decorators):
    """
    给目标函数添加标签

    :param decorators:        标签名
    """

    def wrap(func):
        func.__decorators = decorators
        return func

    return wrap
