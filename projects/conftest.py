"""
 File       : conftest.py
 Time       : 2021/11/2 16:31
 Author     : 黄大彬
 version    : python 3.7
"""

import  allure,pytest
import  cx_Oracle  as cx
from config.settings import *

@allure.step("建立数据库连接")
@pytest.fixture(scope='session',autouse = True )
def  db():

    try:

        name=Project.name

        con = cx.connect(setting[name]['db_user'], setting[name]['db_pwd'],
                         cx.makedsn(setting[name]['db_host'], setting[name]['db_port'],
                        service_name=setting[name]['db_service']))

        cur = con.cursor()

        yield cur

    except  Exception :

        raise   Exception ('数据连接失败')

    cur.close()
    con.close()



@allure.step("项目名称")
@pytest.fixture(scope='session',autouse = True )
def  project():

    yield Project.name


