**环境准备**

    1.Python3.7.4
    2.安装依赖库：pip install -r requirements.txt

--------------------------------------------------------------------

**目录说明**

    ./common                      公共函数，第三方插件(webdriver,allure)
    ./config/settings.py         配置文件，项目启动必须配置
    ./testCase                   测试用例，子目录对应不同project
    ./testData                   测试数据，目录结构与projects对应
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

            1.多个项目通过路径区分：projects/{moduletname}/test_*.py
            2.测试数据目录结构与case路径对应：testData/{projectname}/file
            3.所有测试数据文件建议采用json文件
 

    项目管理

        1.HES根据配置确定不同项目
        2.HES多个项目采用配置文件区分
            1).可通过不同文件夹区分
            2).采用项目名作为配置文件名称
        3.配置文件建议采用: yaml或py文件


--------------------------------------------------------------------

**注意事项**

    1.report和result本地文件不需要提交到Git,设置忽略文件
    2.运行方式: 启动路径，必须是项目根目录
