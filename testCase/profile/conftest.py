"""
 File       : conftest.py
 Time       : 2022/3/17 9:37
 Author     : 黄大彬
 version    : python 3.7.4
"""

import  pytest ,allure,os,json
import cx_Oracle as  cx

from  config.settings import *


@pytest.fixture(scope='session',autouse=True)
def projectName():

    return  Project.name


@pytest.fixture(scope='session',autouse=True)
def  apiUrl():

    return  setting[Project.name]['api_url']+'/api/v1/Request/RequestMessage'


@pytest.fixture(scope='session',autouse=True)
def  db(projectName):

    try:
        con = cx.connect(setting[projectName]['db_user'], setting[projectName]['db_pwd'], cx.makedsn(setting[projectName]['db_host'], setting[projectName]['db_port'], service_name=setting[projectName]['db_database']))

        cur = con.cursor()
    except  Exception :

        raise   Exception ('数据库连接失败')

    yield   cur

    cur.close()
    con.close()


@pytest.fixture()
def  sqlOne(db):

    def exec(sql):
        db.execute(sql)
        return db.fetchone()
    return exec                      #执行SQL,返回一行数据

@pytest.fixture()
def  sqlAll(db):

    def exec(sql):
        db.execute(sql)
        return db.fetchall()
    return exec                     #执行SQL，返回所有




@pytest.fixture()
def  registerIds(sqlAll,meterNo):

    sql = "select  REGISTER_ID  from H_CONFIG_REGISTER  where  PTL_TYPE in (select  ptl_type  from C_AR_MODEL where MODEL_CODE=(select  MODEL_CODE from  C_AR_METER where  METER_NO='%s'))" % meterNo

    rel=sqlAll(sql)

    id_list=[]

    for i in rel:

        id_list.append(i[0])

    return id_list









@allure.step("获取TestData")
@pytest.fixture()
def requestData(projectName):
    def loadData(path):
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,'testData/%s/%s' % (projectName,path))
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    return loadData



@pytest.fixture()
def  meterNo(projectName):
    return setting[projectName]['meter_no']



