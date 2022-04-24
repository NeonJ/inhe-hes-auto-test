"""
 File       : test_obis_check.py
 Time       : 2022/3/17 13:58
 Author     : 黄大彬
 version    : python 3.7.4
"""

import  pytest,requests,time,allure
from   config.settings import *
import  cx_Oracle  as cx


def obis_list():

    '''获取meter对应的所有obis'''

    try:
        con = cx.connect(setting[Project.name]['db_user'], setting[Project.name]['db_pwd'],
                         cx.makedsn(setting[Project.name]['db_host'], setting[Project.name]['db_port'],
                                    service_name=setting[Project.name]['db_database']))

        cur = con.cursor()
    except  Exception:

        raise Exception('数据库连接失败')

    sql = "select  REGISTER_ID  from H_CONFIG_REGISTER  where  PTL_TYPE in (select  ptl_type  from C_AR_MODEL where MODEL_CODE=(select  MODEL_CODE from  C_AR_METER where  METER_NO='%s'))" % \
          setting[Project.name]['meter_no']

    cur.execute(sql)

    rel = cur.fetchall()

    id_list = []

    for i in rel:
        id_list.append(i[0])

    return id_list



class  Test_OBIS:

    @pytest.mark.parametrize('obis_id',obis_list())
    def  test_obis_check_meter(self,apiUrl,meterNo,obis_id):


        data={
  "header": {
    "correlationId": "68e19310-1253-4a6c-bd9c-e60266e52429",
    "messageId": "05a98597-fa9c-49bd-99ca-69d30d30dace",
    "createTime": "20200910191946",
    "serviceType": "GET_COMMON",
    "businessType": "GET_COMMON",
    "source": "MDM",
    "messageType": "REQUEST",
    "asyncReplyFlag": False
  },
  "payload": [
    {
      "deviceNo": "M202009040003",
      "deviceType": "METER",
      "transactionId": "5ebbd125-e1d0-4a90-b0af-6d13d22f78e6",
      "data": [
        {
          "registerId": "9300"
        }
      ]
    }
  ]
}
        data['payload'][0]['deviceNo']=meterNo
        data['payload'][0]['data'][0]['registerId']= obis_id
        re=requests.post(url=apiUrl,json=data)

        assert re.status_code==200
        allure.attach(name='response',body=re.text)
        time.sleep(2)




    def  test_obis_check_dcu(self,apiUrl,meterNo):

        pass


