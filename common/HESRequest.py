import json
import time

import requests


# from elasticsearch import Elasticsearch


class HESRequest():

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}

    def get(self, url, params):

        print(url)
        print('Request --- ', params)
        r = requests.get(url=url, params=params, headers=self.headers, timeout=66)
        # response = json.loads(r.text)
        elapsed = r.elapsed.total_seconds()
        if r.status_code == 504:
            print('504 and try again')
            time.sleep(1)
            r = requests.get(url=url, params=params, headers=self.headers, timeout=66)
            # response = json.loads(r.text)
            elapsed = r.elapsed.total_seconds()
        elif 'Device Busying' in r.text:
            print('Device Busying and try again')
            time.sleep(1)
            r = requests.get(url=url, params=params, headers=self.headers, timeout=66)
            # response = json.loads(r.text)
            elapsed = r.elapsed.total_seconds()
        return json.loads(r.text), elapsed

    def post(self, url, params):

        # data = json.dumps(params)
        print(url)
        print('Request --- ', params)
        # try:
        #     DeviceBusy = 1
        #     while DeviceBusy == 1:
        #         r = requests.post(url=url, json=params, headers=self.headers, timeout=66)
        #         response = json.loads(r.text)
        #         elapsed = r.elapsed.total_seconds()
        #         time.sleep(1)
        #         if r.status_code == 504:
        #             print('504 and try again')
        #             time.sleep(1)
        #             continue
        #         elif 'Device Busying' in json.dumps(response):
        #             print('Device Busying and try again')
        #             time.sleep(1)
        #             continue
        #         else:
        #             DeviceBusy = 0
        #     return response, elapsed
        # except BaseException as e:
        #     print("post请求错误，错误原因：%s" % e)
        r = requests.post(url=url, json=params, headers=self.headers, timeout=66)
        # response = json.loads(r.text)
        elapsed = r.elapsed.total_seconds()
        if r.status_code == 504:
            print('504 and try again')
            time.sleep(1)
            r = requests.post(url=url, json=params, headers=self.headers, timeout=66)
            # response = json.loads(r.text)
            elapsed = r.elapsed.total_seconds()
        elif 'Device Busying' in r.text:
            print('Device Busying and try again')
            time.sleep(1)
            r = requests.post(url=url, json=params, headers=self.headers, timeout=66)
            # response = json.loads(r.text)
            elapsed = r.elapsed.total_seconds()
        return json.loads(r.text), elapsed

# if __name__ == '__main__':
#     pass
#     # data = loadData('testData/MeterFrozenData/meter_daily_data.json'.format(Project.name))['meter_daily_entries']
#     # requestData = data['request']
#     # requestData['payload'][0]['deviceNo'] = device['device_number']transactionId = str(device['device_number']) + '_' + time.strftime('%y%m%d%H%M%S',time.localtime())
# requestData['payload'][0]['transactionId'] = transactionId
#     # response, elapsed = HESRequest().post(url=requestMessage,
#     #                      params=requestData)
#     # print('Response --- ',response)
#     # print(type(response))
#     # assert response.get('reply')['replyCode'] == 201
