import argparse
import logging
import time

from common.AllureReport import *
from config.settings import *
import paramiko

# from pexpect import *

logging.basicConfig(level=logging.DEBUG)

logging.info('''测试前准备，清理历史数据..............................................''')

# 创建result目录
if os.path.exists('./result/'):
    shutil.rmtree('./result/')  # 清空历史数据,系统自动创建resulthe report路径
else:
    print('清楚历史执行明细')

logging.info('Testing  Start....................................................')

# 设置参数
parser = argparse.ArgumentParser()
parser.add_argument('-p', "--project", help="project", default='empower')  # 服务名称
parser.add_argument('-t', "--tag", help="case tag", default='smokeTest1',
                    choices=['smokeTest', 'fullTest', 'asyncTest','OBISCheck'])  # marker，用例标签
parser.add_argument('-pa', "--path", help="report  path", default='/')
parser.add_argument('-c', "--continue", help="continue last obis check", default='False', choices=['False', 'True'])
parser.add_argument('-r', "--retry", help='failed retries', default='0')
parser.add_argument('-g', "--groug", help='nacos group', default='QA', choices=['QA', 'DEV'])

args = parser.parse_args()


if args.tag != 'fullTest':

    os.system(
        'pytest  --reruns %s --reruns-delay 1 --json-report  -v  testCase/   -m  %s    --alluredir  ./result/' % (
            args.retry, args.tag))  # 按模块指定标签测试

else:

    os.system(
        'pytest --reruns %s --reruns-delay 1 --json-report  -v  testCase/   --alluredir  ./result/' % args.retry)  # 模块全量测试

# Allure报告
if os.listdir('./result') != []:
    if not os.path.exists('./report/'):
        os.mkdir('./report/')
    if not os.path.exists('./report/{}'.format(Project.name)):
        os.mkdir('./report/{}'.format(Project.name))
    buildOrder, old_data = get_dirname()
    environment()
    os.system("allure  generate  ./result/  -o  ./report/{}/{}  --clean".format(Project.name, buildOrder))
    all_data, reportUrl = update_trend_data(buildOrder, old_data)
    if not os.path.exists('./report/report_history'):
        os.mkdir('./report/report_history')
    shutil.copytree('./report/{}/{}'.format(Project.name, buildOrder), './report/report_history/{}'.format(buildOrder))
    report_date = time.strftime('%y%m%d%H%M%S', time.localtime())
    report_path = './report/report_history/{}'.format(Project.name + '-' + report_date)
    os.rename('./report/report_history/{}'.format(buildOrder),
              './report/report_history/{}'.format(Project.name + '-' + report_date))
    # Linux环境推送测试报告到Tomcat
    # child = spawn("scp -r {} root@10.32.233.164:/opt/tomcat/webapps".format(report_path))
    # child.expect ("password")
    # child.sendline ("kaifa123")
    # child.read()
    print('Report URL == http://10.32.233.164:9090/{}/'.format(Project.name + '-' + report_date))
else:
    print('无结果数据，无法生成报告')
