import json
import time

import requests


class TestRequest():

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}

    def get(self, url, params):

        try:
            DeviceBusy = 1
            while DeviceBusy == 1:
                r = requests.get(url=url, params=params, headers=self.headers)
                response = json.loads(r.text)
                time.sleep(1)
                if r.status_code == 504:
                    print('504 Busying and try again')
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
                r = requests.post(url=url, json=params, headers=self.headers)
                response = json.loads(r.text)
                time.sleep(1)
                if r.status_code == 504:
                    print('504 Busying and try again')
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
    a = TestRequest().get(url='http://empower.hes-api.kaifa.tst/Mdm/getTime',
                          params='deviceNo=M202009040003&deviceType=1&taskType=0')
    print(a)
