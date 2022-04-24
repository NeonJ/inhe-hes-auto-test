"""
 File       : test_evebt_profile.py
 Time       : 2022/3/17 10:15
 Author     : 黄大彬
 version    : python 3.7.4
"""


import  requests,time



class  Test_Daily:

    def  test_get_event_profile_sync(self,apiUrl,requestData,projectName,meterNo):

        '''同步获取事件曲线'''

        data=requestData('MeterFrozenData/meter_event_data.json')['meter_daily_event']['request']
        data['payload'][0]['deviceNo']=meterNo

        time.sleep(3)

        re=requests.post(url=apiUrl,json=data)

        assert re.status_code==200
        assert re.json()['header']['messageType']=='RESPONSE'
        assert re.json()['reply']['replyCode']==200
        assert len(re.json()['payload'][0]['data']) !=0