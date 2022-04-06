import json
import time

import requests

class HESRequest():

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}

    def get(self, url, params):

        try:
            DeviceBusy = 1
            while DeviceBusy == 1:
                r = requests.get(url=url, params=params, headers=self.headers, timeout=66)
                response = json.loads(r.text)
                time.sleep(1)
                if r.status_code == 504:
                    print('504 and try again')
                    time.sleep(1)
                    continue
                elif 'Device Busying !' in json.dumps(response):
                    print('Device Busying and try again')
                    time.sleep(1)
                    continue
                else:
                    DeviceBusy = 0
                return response

        except BaseException as e:
            print("get请求错误，错误原因：%s" % e)

    def post(self, url, params):

        # data = json.dumps(params)
        print(url)
        print(params)
        try:
            DeviceBusy = 1
            while DeviceBusy == 1:
                r = requests.post(url=url, json=params, headers=self.headers, timeout=66)
                response = json.loads(r.text)
                time.sleep(1)
                if r.status_code == 504:
                    print('504 and try again')
                    time.sleep(1)
                    continue
                elif 'Device Busying !' in json.dumps(response):
                    print('Device Busying and try again')
                    time.sleep(1)
                    continue
                else:
                    DeviceBusy = 0
            return response

        except BaseException as e:
            print("post请求错误，错误原因：%s" % e)



if __name__ == '__main__':
    pass
    # data = loadData('testData/{}/MeterFrozenData/meter_daily_data.json'.format(Project.name))['meter_daily_entries']
    # requestData = data['request']
    # requestData['payload'][0]['deviceNo'] = setting[Project.name]['meter_no']
    # response = HESRequest().post(url=Project.request_url,
    #                      params=requestData)
    # print(response)
    # print(type(response))
    # assert response.get('reply')['replyCode'] == 201