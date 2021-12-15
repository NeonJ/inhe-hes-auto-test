"""
 File       : main.py
 Time       : 2021/11/2 16:37
 Author     : 黄大彬
 version    : python 3.7
"""

import logging, os, shutil
import time

from config.settings import *

logging.basicConfig(level=logging.DEBUG)

logging.info('''测试前准备，清理历史数据..............................................''')

# 创建result目录

if os.path.exists('./result/'):
    shutil.rmtree('./result/')  # 清空历史数据,系统自动创建resulthe report路径

else:
    print('一切ok')

logging.info('Testing  Start !!!!!!!!!!!!!!!!!!!!!!!!')

if Project.name is not None:

    if Project.tag:

        # 指定tag和项目
        os.system(
            'pytest   --json-report   -v  testCase/%s   -m  %s    --alluredir  ./result/' % (Project.path, Project.tag))
    else:

        # 不指定tag
        os.system('pytest  --json-report     -v  testCase/%s     --alluredir  ./result/' % Project.path)
else:

    print('settings文件参数错误，name是必填参数')

# 报告生成
# if os.listdir('./result') != []:
#     os.system("allure  generate  ./result/  -o  ./report/%s  --clean" % time.strftime('%Y%m%d%H%M%S',time.localtime()))
#
# else:
#
#     print('无结果数据，无法生成报告')
