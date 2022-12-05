import argparse
import logging
import socket
import time

import yaml

from common.AllureReport import *
from common.WinSFTP import *

logging.basicConfig(level=logging.DEBUG)

logging.info('''测试前准备，清理历史数据..............................................''')

# 创建result目录
result_path = os.path.join(os.path.dirname(__file__), 'result')
if os.path.exists(result_path):
    shutil.rmtree(result_path)  # 清空历史数据,系统自动创建resulthe report路径
else:
    print('清楚历史执行明细')

logging.info('Testing  Start....................................................')

# 设置参数
parser = argparse.ArgumentParser()
parser.add_argument("--project", help="project", required=True)  # 服务名称
parser.add_argument("--tag", help="case tag", default='smokeTest')  # marker，用例标签
parser.add_argument("--path", help="report  path", default='/')
parser.add_argument("--resume", help="continue last obis check", default='False', choices=['False', 'True'])
parser.add_argument("--retry", help='failed retries', default='0')
parser.add_argument("--group", help='nacos group', default='QA', choices=['QA', 'DEV'])
parser.add_argument("--tester", help='tester name', default=socket.gethostname())

args = parser.parse_args()


def config():
    config_dict = {}
    config_dict['nacos_url'] = 'http://192.168.215.76:1848'
    config_dict['project'] = args.project
    config_dict['tag'] = args.tag
    config_dict['path'] = args.path
    config_dict['resume'] = args.resume
    config_dict['retry'] = args.retry
    config_dict['group'] = args.group
    config_dict['tester'] = args.tester
    return config_dict


def writeConfig():
    current_path = os.path.abspath(__file__)
    config_file_path = os.path.join(
        os.path.abspath(os.path.dirname(current_path) + os.path.sep + "." + os.path.sep + 'config'),
        'settings.yaml')
    with open(config_file_path, 'w') as f:
        yaml.dump(data=config(), stream=f, allow_unicode=True)


var = '--project {} --tag {} --tester {} --resume {} --retry {} --group {}'.format(args.project, args.tag, args.tester,
                                                                                   args.resume, args.retry, args.group)
print(var)
writeConfig()
tag = str(args.tag).replace(',',' or ')

if args.tag != 'fullTest':
    os.system(
        'pytest --reruns %s --reruns-delay 1 --json-report  -v  %s/testCase/ -m "%s"  --alluredir  %s' % (
            args.retry, os.path.dirname(__file__), tag, result_path))  # 按模块指定标签测试
    # 'pytest  --reruns %s --reruns-delay 1 --json-report  -v  %s/testCase/   -m  %s  -s %s   --alluredir  %s' % (
    #     args.retry, os.path.dirname(__file__), args.tag, var, result_path))  # 按模块指定标签测试
else:
    os.system(
        'pytest --reruns %s --reruns-delay 1 --json-report  -v  %s/testCase/  --alluredir  %s' % (args.retry,
                                                                                                  os.path.dirname(
                                                                                                      __file__),
                                                                                                  result_path))  # 模块全量测试

# Allure报告
report_path = os.path.join(os.path.dirname(__file__), 'report')
if os.listdir(result_path) != []:
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    if not os.path.exists(report_path + '/{}'.format(args.project)):
        os.mkdir(report_path + '/{}'.format(args.project))
    buildOrder, old_data = get_dirname()
    environment()
    os.system("allure  generate  {}  -o  {}/{}/{}  --clean".format(result_path, report_path, args.project, buildOrder))
    all_data, reportUrl = update_trend_data(buildOrder, old_data)
    if not os.path.exists('{}/report_history'.format(report_path)):
        os.mkdir('{}/report_history'.format(report_path))
    shutil.copytree('{}/{}/{}'.format(report_path, args.project, buildOrder),
                    '{}/report_history/{}'.format(report_path, buildOrder))
    report_date = time.strftime('%y%m%d%H%M%S', time.localtime())
    history_path = '{}/report_history/{}'.format(report_path, args.project + '-' + report_date)
    os.rename('{}/report_history/{}'.format(report_path, buildOrder),
              '{}/report_history/{}'.format(report_path, args.project + '-' + args.tester + '-' + report_date))
    # 推送报告到报告仓库
    # warehouse_dir = r'/opt/tomcat/webapps'
    # local_report_dir = r'{}/report_history/{}'.format(report_path,
    #                                                   args.project + '-' + args.tester + '-' + report_date)
    # host = Linux('10.32.233.164', 'root', 'kaifa123')
    # host.sftp_put_dir(local_report_dir, warehouse_dir)
    # print('Report URL == http://10.32.233.164:9090/{}/'.format(
    #     args.project + '-' + args.tester + '-' + report_date))
else:
    print('无结果数据，无法生成报告')
