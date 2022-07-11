**HES自动化测试框架Overview**

    1. 自动创建测试环境
    2. 自动拉取用例代码
    3. 自动根据设备类型筛选用例，比如单项表不执行相位夹角，短连接表不执行上下线等
    4. 自动将失败Case的错误类型进行一次大致分类，比如是设备报错，还是配置异常等
    5. 自动提交报告到报告仓库
    6. 自动回收测试环境

--------------------------------------------------------------------


**环境准备**

    1.Python3.6.9
    2.安装依赖库：pip install -r requirements.txt
    3.需要Oracle外部组件支持instantclient-basic, 设置oracle客户端环境变量
    4.需要Allure外部组件，设置Allure环境变量，依赖Java

--------------------------------------------------------------------

**Case Tag**

    1.smokeTest      冒烟测试，主要针对设备的实时操作
    2.asyncTest      HES异步任务测试，主要是HES系统对设备的异步任务操作
    3.obisTest       对所选电表的register_id进行测试并保存到数据库测试表中，支持Read、Set，支持断点续测
    4.interfaceTest  HES非设备操作的接口测试
    5.fullTest       除开obisTest之外的所有Tag测试
    ***多tag执行使用,号连接

--------------------------------------------------------------------

**测试执行**

    1.可以通过pytest单用例执行
    2.可以通过main.py执行
    python main.py --project empower --tag=smokeTest,asyncTest --tester Neon --retry 0 --group QA --resume False
    3.可以通过docker自动执行
    docker run --rm -e project=empower -e tag=smokeTest,asyncTest -e tester=Neon -e retry=0 -e group=QA -e resume=False 10.32.233.112/test/py36-test
    
    ***测试还需要在NACOS(http://10.32.233.164:18848/nacos/)上正确编辑测试环境和测试变量后才能正确执行***
    project, 对应nacose中的data id
    tag, 默认为smoketTest
    tester, 默认为执行主机名
    retry, 0表示用例执行失败不重新执行
    group, QA表示测试环境, DEV表示开发环境
    resume, True表示obisTest继续上一次测试结束点继续执行, False表示开始新的obisTest


--------------------------------------------------------------------


**目录说明**

    ./common                     公共函数，第三方插件(webdriver,allure)
    ./config/settings.yaml       配置文件，项目环境配置，Nacos地址和命令行输入
    ./testCase                   测试用例
    ./testData                   测试数据
    ./result                     运行后的结果文件
    ./report                     HTML格式的测试报告，allure生成
    ./requirements.txt           第三方依赖库
    ./main.py                    启动文件，启动方式：python  main.py

----------------------------------------------------------------------

**基本规范**

    用例规范

        1.所有用例py文件名格式: test_*.py
        2.类命名: class Test_*
        3.用例名: test_*
        4.所有py文件头信息: 文件名、时间、作者、version

    项目结构

        1.多个项目通过路径区分：testCase/模块名称/test_*.py
        2.测试数据目录结构与case路径对应：testData/
        3.所有测试数据文件建议采用json文件

    项目管理

        1.HES尽可能使用相同的测试用例
        2.HES使用NACOS传惨方式进行测试设备和测试环境和测试变量的维护
            如果NACOS不可用本地调试可以直接使用本地的nacos-data文件进行用例编写和测试
        3.配置文件建议采用: yaml格式


--------------------------------------------------------------------

**注意事项**

    1.report和result本地文件不需要提交到Git,设置忽略文件
    2.运行方式: 启动路径，必须是项目根目录