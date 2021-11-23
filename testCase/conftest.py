# """
# # File       : conftest.py
# # Time       ：2021/5/12 14:18
# # Author     ：黄大彬
# # version    ：python 3.7
# """
#
#
# import shutil
# import  requests,pytest,allure
# import  cx_Oracle  as cx
# from common.readConfig import  *
# from faker import  Faker
# from common.public.shipmentFile import *
# from common.utilTool import *
#
#
#
# @pytest.fixture(scope="session",autouse=True)
# def   tmp_dir():
#
#     '''创建临时目录'''
#
#     tmp_path=os.path.join(os.path.dirname(__file__),'../tmp')
#     if not os.path.exists(tmp_path):
#         os.mkdir(tmp_path)
#     else:
#         shutil.rmtree(tmp_path)
#         os.mkdir(tmp_path)
#
#     yield tmp_path
#
#     shutil.rmtree(tmp_path)
#
#
#
#
#
# @allure.step('获取用户权限')
# @pytest.fixture(autouse=True,scope='session')
# def  token(gateway):
#
#     re=requests.post(url=gateway+'/api/gateway-service/tokens.json',json={"language":"en","username":User.user(),"password":User.pwd()})
#     access_token=re.json()['data']['access_token']
#
#     yield {'Access-Token':access_token,'Application-Id':'AMI_WEB'}
#
#
#
#
# @allure.step("获取服务端网关地址")
# @pytest.fixture(scope='session',autouse = True )
# def  gateway():
#
#     yield  Url.gateWayUrl()
#
#
#
#
#
# @allure.step("建立数据库连接")
# @pytest.fixture(scope='session',autouse = True )
# def  db():
#     try:
#         con = cx.connect(Oracle.user(), Oracle.pwd(), cx.makedsn(Oracle.host(), Oracle.port(), service_name=Oracle.servicename()))
#
#         cur = con.cursor()
#     except  Exception :
#
#         raise   Exception ('数据库连接失败')
#
#     yield   cur
#
#     cur.close()
#     con.close()
#
#
#
#
# @pytest.fixture()
# def  sqlOne(db):
#
#     def exec(sql):
#         db.execute(sql)
#         return db.fetchone()
#     return exec                      #执行SQL,返回一行数据
#
#
#
# @pytest.fixture()
# def  sqlAll(db):
#
#     def exec(sql):
#         db.execute(sql)
#         return db.fetchall()
#     return exec                     #执行SQL，返回所有
#
#
# @pytest.fixture()
# def  jobId(db):
#
#     def exec(name):
#         if isinstance(name,str) :
#
#             sql="select  id  from   POWER_JOB_INFO  where JOB_NAME='%s' and APP_ID in (select  ID  from POWER_APP_INFO) "  % name
#             db.execute(sql)
#             return db.fetchone()[0]
#         else:
#             print('参数异常，参数类型必须是字符串')
#     return exec                                 #执行SQL，通过name获取powerjob  jobId
#
#
#
# @pytest.fixture()
# def  powerjob():
#
#     '''powerjob 地址'''
#
#     return  Url.powerjob()
#
#
#
# @pytest.fixture()
# def  runJob(powerjob,sqlOne):
#
#     '''触发powerjob执行'''
#
#     def exec(name):
#
#         #获取jobId
#         sql = "select  id  from   POWER_JOB_INFO  where JOB_NAME='%s' and APP_ID in (select  ID  from POWER_APP_INFO) " % name
#
#         #触发powerjob
#
#         re=requests.get(url=powerjob+'/job/run',params={'jobId':str(sqlOne(sql)[0])})
#         return re
#
#     return exec                    #执行powejob
#
#
#
#
#
# @pytest.fixture()
# def fakerCN():
#     f = Faker(locale='zh_CN')
#     yield f                           #造中国式数据
#
#
# @pytest.fixture()
# def fakerUS():
#     f = Faker(locale='en_US')
#     yield f                            #造美国式数据
#
#
#
#
# @pytest.fixture(scope='session',autouse=True)
# def  addTr(gateway,token):
#
#     '''添加TR'''
#
#     for i  in  range(10,100):
#         url = gateway + '/api/user-service/regions/add.json'
#
#         data={
#         "regionParentId":"3000015",
#         "regionParentTypeId":"13",
#         "isAdd":True,
#         "regionDesc":"",
#         "childRegionTypeId":"11",
#         "regionNo":FakerData.randomId(5),
#         "regionName":'APIADD'+str(i)
#     }
#
#         re=requests.post(url=url,json=data,headers=token)
#         assert  re.status_code==200
#
#
#
#
# @pytest.fixture(scope='session',autouse=True)
# def  importMeter(token,gateway):
#
#     '''导入三种类型档案'''
#
#     with allure.step('step1:生成meter shipmentfile'):
#
#         MoreMeter().produce()
#
#
#     with allure.step('step2:上传文件'):
#         data = {'businessType': 'SHIPMENT_FILE', 'accessToken': token['Access-Token']}  # 上传文件参数通过params传递
#
#         file = {'file': open(os.path.join(os.path.dirname(__file__),
#                                           '../template/shipment_file_meter_moreMeter.xlsx'), 'rb')}
#         re = requests.post(url=gateway + '/api/system-service/excel/upload/crossTemp', params=data, files=file)
#
#         fileId = re.json()['data']
#         assert re.status_code == 200
#         assert re.json()['code'] == 200
#
#
#     with allure.step('step3:add file'):
#         data = {
#             "deviceType": "METER",
#             "isAdd": True,
#             "fileType": "NEW_EXCEL",
#             "regionId": "0",
#             "importId": fileId
#         }
#
#         re = requests.post(url=gateway + '/api/archive/shipment/addFile.json', json=data, headers=token)
#         assert re.json()['desc'] == "OK"
#         assert re.status_code == 200
#
#
#     with allure.step('step4:变更file状态'):
#         url = gateway + '/api/archive/shipment/parse/%s.json' % fileId  # 表:C_AR_SFILE_IMPORT
#         re = requests.post(url=url, headers=token)
#         assert re.status_code == 200
#         assert re.json()['desc'] == 'OK'
#
#
#     with  allure.step('step5:触发powerjob'):
#         data = {'jobId':'1605838'}  # shipmentfile job ID
#
#         re = requests.get(url=Url.powerjob() + '/job/run', params=data)
#
#         assert re.status_code == 200
#         assert re.json()['success'] is True  # 上传完
#
#         time.sleep(5)
#
#
#
#
