import logging
import time

from common.AllureReport import *
from config.settings import *

# from pexpect import *

logging.basicConfig(level=logging.DEBUG)

logging.info('''测试前准备，清理历史数据..............................................''')

# 创建result目录
if os.path.exists('./result/'):
    shutil.rmtree('./result/')  # 清空历史数据,系统自动创建resulthe report路径
else:
    print('清楚历史执行明细')

logging.info('Testing  Start....................................................')

if Project.name is not None:
    if Project.tag:

        os.system(
            "pytest  --reruns %s --reruns-delay 1 --json-report   -v  testCase/%s   -m  %s    --alluredir  ./result/" % (
                Project.retry, Project.path, Project.tag))
    else:
        # 不指定tag
        os.system('pytest  --json-report     -v  testCase/%s     --alluredir  ./result/' % Project.path)
else:
    print('settings文件参数错误，name是必填参数')

# 报告生成 按照时间生成报告
# if os.listdir('./result') != []:
#     report_date = time.strftime('%y%m%d%H%M%S',time.localtime())
#     report_path = './report/{}/{}'.format(Project().name, Project().name + '-' + report_date)
#     os.system("allure  generate  ./result/  -o  {}  --clean".format(report_path))
# else:
#     print('无结果数据，无法生成报告')


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

# 报告生成 按照项目＋执行次数生成报告
# if os.listdir('./result') != []:
#     if not os.path.exists('./report/{}'.format(Project.name)):
#         os.mkdir('./report/{}'.format(Project.name))
#     buildOrder, old_data = get_dirname()
#     environment()
#     os.system("allure  generate  ./result/  -o  ./report/{}/{}  --clean".format(Project.name, buildOrder))
#     time.sleep(3)
#     all_data, reportUrl = update_trend_data(buildOrder, old_data)
# else:
#     print('无结果数据，无法生成报告')
