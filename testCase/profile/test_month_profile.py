"""
 File       : test_month_profile.py
 Time       : 2022/3/17 9:36
 Author     : 黄大彬
 version    : python 3.7.4
"""


import  requests,pytest,allure,time



class  Test_Month:

    def  test_get_month_profile_sync(self,apiUrl,requestData,projectName,meterNo):

        '''同步获取月结曲线'''

        data=requestData('MeterFrozenData/meter_monthly_data.json')['meter_monthly_data']['request']
        data['payload'][0]['deviceNo']=meterNo

        time.sleep(3)

        re=requests.post(url=apiUrl,json=data)

        assert re.status_code==200
        assert re.json()['header']['messageType']=='RESPONSE'
        assert re.json()['reply']['replyCode']==200
        assert len(re.json()['payload'][0]['data']) !=0