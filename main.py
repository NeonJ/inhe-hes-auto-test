# -*- coding: UTF-8 -*-

import sys
import traceback

import re
import os
import argparse
from libs.Singleton import Singleton
from comms.KFLog import info, error, kfLog
from comms.UsefulAPI import getTimeStamp
from comms.HtmlFormater import logToHtml


def writeTestResultToFile(content):
    """
    创建一个 result.txt 文件, 并向文件中追加用例执行结果
    :param content:
    :return:
    """
    filename = os.path.join("logs", kfLog.datetime, 'result.txt')
    with open(filename, 'a+') as fp:
        fp.write(f'[{getTimeStamp()}] - {content}\n')


def addSpecialTag(tagList):
    """
    将特殊 tag 添加到集合中并返回 (每一个子模块以'000'结尾的文件是特殊文件, 用于执行初始化操作)
    :param tagList:     接收一个list
    :return:            返回一个字符串
    """
    for tag in tagList:
        initialTag = re.sub(r'_(\d{3})', '_000', tag)
        if initialTag not in tagList:
            tagList.append(initialTag)
    return ",".join(set(tagList))


def loadFile(filename):
    """
    通过文件名加载对应的函数
    :param filename:    从'project'路径开始的文件名 (projects/cetus02/loadprofile/lp1_handing_cdi/lp1_handling_cdi_080.py)
    :return:            返回函数对象
    """
    subdirs = filename.replace('.py', '').split(os.sep)[:]
    modules = ''
    for sub in subdirs:
        modules += sub.lower() + '.'
    obj = __import__(modules[:-1], fromlist=['all'])
    func = getattr(obj, subdirs[-1].lower())
    return func


def isContainTags(filename, tags, untags):
    """
    判断指定的文件是否包含特定的tag
    :param filename:    文件路径
    :param tags:
    :param untags:
    :return:            返回一个元组, 成功时返回(True, Func), 失败时返回(False, '')
    """
    # testcasefilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    testcasefilepath = filename
    if not os.path.exists(testcasefilepath):
        error(f"`isContainTags` Not found TestCase: '{testcasefilepath}'")
        return False, ''

    # 通过文件加载对应的函数
    func = loadFile(filename)

    # 提取每个用例中的 tag list
    taglist = list()
    try:
        taglist = [item.lower() for item in list(func.__decorators)]
    except AttributeError:
        pass

    # 如果 taglist 中包含了任意一个 untag, 则返回False
    if untags is not None:
        for untag in untags.split(","):
            if untag.lower() in taglist:
                return False, ''

    # 如果 taglist 中包含任意一个 tag, 则返回True
    if tags is not None:
        for tag in tags.split(","):
            if tag.lower() in taglist:
                return True, func

    return False, ''


def searchFilesByDirectory(projectPath):

    data = dict()
    for root, _, _ in os.walk(projectPath):
        if not root.endswith(Singleton().Project):
            if os.path.basename(os.path.dirname(root)) == Singleton().Project:
                dirname = os.path.basename(root)
                data[dirname] = list()
                for subroot, _, filename in os.walk(root):
                    for file in filename:
                        if re.search('_\d{2,4}.py', file):
                            data[dirname].append(os.path.join(subroot, file))
                if len(data[dirname]) == 0:
                    del data[dirname]
    return data


def execTestcase(func):
    """
    执行函数
    :param func:    函数对象
    :return:        返回一个元组
    """
    Singleton().TestCase = func.__name__
    try:
        return func, func()
        # return func, -1
    except:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
        return func, -1



def setupTearDown(project, feature, isSetup=True):
    """
    执行模块级的setup 和 teardown 操作
    :param project:         项目名
    :param feature:         模块名
    :param isSetup:         是否执行setup操作  (True -> setup,  False -> teardown)
    :return:
    """
    if len(feature) == 0:
        mode = 'Project'
    else:
        mode = 'Module'

    if isSetup:
        filename = 'setup'
    else:
        filename = 'teardown'

    setupTeardownFile = os.path.join("projects", project, feature, filename + ".py")
    if not os.path.exists(setupTeardownFile):
        return 0
    else:
        info('')
        info(f"-------------------------- {mode.capitalize()} {filename.capitalize()} Start --------------------------")
        module = (os.path.dirname(setupTeardownFile) + "." + filename).replace(os.sep, ".")         # projects.cetus02.loadprofile.setup
        obj = __import__(module, fromlist=['all'])
        func = getattr(obj, filename)
        Singleton().TestCase = func.__name__        # Delegate.CommunicationDelegate 需要用到
        response = func()
        # if response != 0:
        #     error(f'{mode} "{project} {feature}" {filename.capitalize()} failed !!!\n')
        if response == 0:
            content = f'{func.__doc__.strip()} *** succeeded! ***'
            info(content)
        else:
            content = f'{func.__doc__.strip()} *** failed! ***'
            error(content)
        return response



def parserArguments():
    """
    解析从命令行接收的参数

    :return:
    """
    parser = argparse.ArgumentParser(description="Exec testcase")

    # 用例选择相关参数
    parser.add_argument("-p", "--project", type=str, help="project name: such as amber51, cetuso2...")
    # parser.add_argument("-f", "--feature", type=str, help="modules in one of project")
    parser.add_argument("--tag", type=str, help="tag list, separate with comma(',')")
    parser.add_argument("--tagfile", type=str, help="tag list from file")
    parser.add_argument("--untag", type=str, help="untag list, separate with comma(',')")
    parser.add_argument("--rerun", type=int, default=0, help="rerun failed testcase [rerun] times")

    # DLMS配置相关参数
    parser.add_argument("-m", "--communication", type=str, default='HDLC', choices=['HDLC', 'GPRS', 'DCU', 'IP'], help="communication mode, default 'HDLC'")
    parser.add_argument("--comPort", type=int, help='comPort for HDLC connection')
    parser.add_argument("--client", type=int, help='client id to login meter')
    parser.add_argument("--serverIpAddr", type=str, help='IP address for DCU/GRPS')
    parser.add_argument("--meterSapId", type=int, help='Sap Id for Meter in DCU Archive Management')
    parser.add_argument("--useIEC", type=str, help='Use IEC or not')

    # 环境变量参数
    parser.add_argument("--ctrlHost", type=str, help="PowerControl Host, ipv4 address")
    parser.add_argument("--ctrlIndex", type=str, default="1,2,3", help="PowerControl Circuit IndexList")
    parser.add_argument("--fwUrl", type=str, help="URL for Firmware upgrade (Jenkins/Release)")

    parser.add_argument("--isCheckAction", type=str, default='False', help="whether check action")

    parser.add_argument("--MeterType", type=str, default='SP', help="meter type: SP/PP")
    parser.add_argument("--SupportedObjects", type=str, default='', help="Supported Objects")
    parser.add_argument("-meter", "--meter", type=str, help="hes check meter no.")

    # 解析数据
    args = parser.parse_args()

    # 更新项目名称
    if args.project is None:
        parser.error("'project' argument is needed!")
    if args.tag is None:
        parser.error("'tag' argument is needed")

    return args



def saveToGlobalVariables(args):
    """
    将部分参数保存到全局变量中

    :param args:
    :return:
    """
    # 保存项目名称
    Singleton().Project = args.project.lower()
    # 保存电表通信模式
    Singleton().Communication = args.communication
    # 保存串口ID
    Singleton().ComPort = args.comPort
    # 保存连接电表客户端的ID
    Singleton().Client = args.client
    # 保存DCU/GPRS的IP地址
    Singleton().ServerIpAddress = args.serverIpAddr
    # 保存DCU上Meter的shortAddr (Sap Id)
    Singleton().MeterSapId = args.meterSapId
    # 保存继电器IP地址
    Singleton().PowerControlHost = args.ctrlHost
    # 保存继电器开关回路
    Singleton().PowerControlCircuitIndexList = args.ctrlIndex.split(",")
    # 保存firmware在Jenkins服务器上的存储路径
    Singleton().FwUrl = args.fwUrl
    # 保存untag
    Singleton().UnTag = args.untag
    # 保存IEC
    Singleton().useIEC = args.useIEC

    Singleton().isCheckAction = args.isCheckAction

    Singleton().MeterType = args.MeterType.upper()

    Singleton().SupportedObjects = args.SupportedObjects.split(",")


class Run(object):

    def __init__(self, parserArgs=None):
        if parserArgs:
            self.args = parserArgs
        else:
            self.args = parserArguments()
        saveToGlobalVariables(self.args)

        self.testCaseStatus = dict()
        self.main()

    def searchAndRunTestCase(self):
        """
        根据 tag 和 untag 提取用例并执行
        :return:
        """
        # 将特殊 tag 添加到集合中
        self.args.tag = addSpecialTag(self.args.tag.split(","))

        # 遍历模块下所有以".py"结尾的文件
        # testcasedir = "projects" + os.sep + self.args.project.lower() + os.sep + self.args.feature.lower()
        testcasedir = "projects" + os.sep + self.args.project.lower()
        if not os.path.exists(testcasedir):
            error(f"Not found TestCaseDir: '{testcasedir}'")
            exit(-1)

        # 检查是否存在项目级的setup.py文件 (用于项目初始化操作)
        result = setupTearDown(project=self.args.project.lower(), feature="", isSetup=True)
        if result != 0:
            return

        # 存储脚本执行结果
        testResultList = list()

        data = searchFilesByDirectory(testcasedir)
        for feature, scriptList in data.items():
            validScriptList = list()
            for script in scriptList:
                status, func = isContainTags(script, self.args.tag, self.args.untag)
                if status:
                    validScriptList.append(func)

            if len(validScriptList) > 0:

                # 检查是否存在模块级的setup.py文件 (用于模块初始化操作)
                result = setupTearDown(project=self.args.project.lower(), feature=feature.lower(), isSetup=True)
                if result != 0:
                    return

                info('')
                info("-------------------------- Test Start --------------------------")
                for validScript in validScriptList:
                    testResult = execTestcase(validScript)
                    if testResult is not None:
                        self.testCaseStatus[testResult[0]] = testResult[1]
                        if testResult[1] == 0:
                            content = f'{testResult[0].__doc__.strip()} *** succeeded! ***'
                            info(content)
                        else:
                            content = f'{testResult[0].__doc__.strip()} *** failed! ***'
                            error(content)
                            # 首次执行失败的也记录到'result.txt', 以备查看
                            writeTestResultToFile(content)
                        testResultList.append(testResult)

                # 检查是否存在模块级的teardown.py文件 (用于模块恢复设置操作)
                result = setupTearDown(project=self.args.project.lower(), feature=feature.lower(), isSetup=False)
                if result != 0:
                    return

        # 检查是否存在项目级的teardown.py文件 (用于项目恢复设置操作)
        result = setupTearDown(project=self.args.project.lower(), feature="", isSetup=False)
        if result != 0:
            return

        info('')
        info("-------------------------- Test Result --------------------------")
        for testResult in testResultList:
            if testResult[1] == 0:
                info(f'{testResult[0].__doc__.strip()} *** succeeded! ***')
            else:
                error(f'{testResult[0].__doc__.strip()} *** failed! ***')
        info('')
        info('')

    def reRunFailedTestCases(self):
        """
        将失败的用例重新执行一次
        :param :
        :return:
        """
        filename = os.path.abspath(os.path.join("logs", kfLog.datetime, 'result.txt'))
        try:
            with open(filename, 'r') as fp:
                content = fp.read()
        except FileNotFoundError as ex:
            error(ex)
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
            return

        # 修改 tag 后, 重新执行
        arglist = list(set(re.findall('TestCase:\s*(.*)\.py.*\*\*\* failed! \*\*\*', content)))
        if len(arglist) > 0:
            for index, item in enumerate(arglist):
                # 查找同一子模块中是否存在以'000'命名的特殊脚本 (要求: 脚本文件名最后一段必须是三个数值)
                initialFile = re.sub(r'_(\d{3})', '_000', item)
                if initialFile not in arglist:
                    arglist.insert(index, initialFile)

            self.args.tag = ",".join(arglist)
            self.args.rerun = 0
            self.searchAndRunTestCase()

    def main(self):

        # 查找用例并执行
        self.searchAndRunTestCase()

        # 执行失败的用例
        # for i in range(args.rerun):
        if int(self.args.rerun) != 0:
            self.reRunFailedTestCases()

        content = "-------------------------- Final Result --------------------------"
        info('')
        info(content)
        writeTestResultToFile(content)
        ok = nok = 0
        for func, status in self.testCaseStatus.items():
            if status == 0:
                content = f'{func.__doc__.strip()} *** succeeded! ***'
                info(content)
                ok += 1
                writeTestResultToFile(content)
            else:
                content = f'{func.__doc__.strip()} *** failed! ***'
                error(content)
                nok += 1
                writeTestResultToFile(content)

        # 统计结果
        content = "-------------------------- Statistic --------------------------"
        info(content)
        writeTestResultToFile(content)
        content = f'Total Testcase: {ok + nok}; Succeed: {ok}; Failed: {nok}\n'
        info(content)
        writeTestResultToFile(content)

        # 将Log转化成Html格式
        logToHtml()



if __name__ == '__main__':

    Run()




