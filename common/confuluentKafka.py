# _*_ coding: utf-8 _*_
# @Time      : 2022/4/7 17:33
# @Author    : Jiannan Cao
# @FileName  : confuluentKafka.py
# !/usr/bin/python

import datetime
import time

from confluent_kafka import Producer

from common.CountTime import count_time
from common.ProducerConsumer import *

kafkaserver = '10.32.233.63'
kafkaport = '30359'


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        # print('Message delivery failed: {}'.format(err))
        pass
    else:
        # print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        pass


@count_time
def c_kafka(topic, payloads, sleep_time=0, **conf):
    p = Producer(**conf)
    for i in payloads:
        p.poll(0)
        p.produce(topic, json.dumps(i).encode('utf-8'), callback=delivery_report)
        if sleep_time > 0:
            p.flush()
            time.sleep(int(sleep_time))
    if sleep_time == 0:
        p.flush()
    return len(payloads)


@count_time
def py_kafka(topic, payloads):
    producer = Kafka_Producer(kafkaserver, kafkaport, topic)
    for i in payloads:
        producer.sendjsondata(i)
    return len(payloads)


@count_time
def hdatadaily(meter_start, meter_end, day_count, daily_time):
    payloads = []
    for i in range(int(day_count)):
        print('daily = ', daily_time)
        for j in range(meter_end - meter_start):
            payloads.append(
                {
                    "Number" : str(meter_start + j)
                    # "ADDITIONAL_INFO_MAP": {
                    #     "COMM_DEVICE_NO": "KFM00" + str(meter_start + j),
                    #     "PROFILE_OBIS": "1.0.99.2.0.255"
                    # },
                    # "DATAS": {
                    #     "9300": daily_time,
                    #     "A213A": "0",
                    #     "0300": "146.755",
                    #     "0400": "0.000",
                    #     "0700": "0.104",
                    #     "0800": "0.000",
                    #     "0900": "0.000",
                    #     "0A00": "65.492"
                    # },
                    # "MNO": "KFM00" + str(meter_start + j),
                    # "DTS": daily_time,
                    # "CTS": "220408013755",
                    # "SRC": "3",
                    # "DATA_INTERVAL": 0
                }
            )
        daily_time = datetime.datetime.strptime(daily_time.__str__(), "%y%m%d%H%M%S")
        daily_time = (daily_time + datetime.timedelta(days=1)).strftime('%y%m%d%H%M%S')
    return payloads


@count_time
def hdatamonthly(meter_start, meter_end, monthly_count, monthly_time):
    payloads = []
    for i in range(int(monthly_count)):
        print('daily = ', monthly_time)
        for j in range(meter_end - meter_start):
            payloads.append(
                {
                    "ADDITIONAL_INFO_MAP": {"COMM_DEVICE_NO": meter_start + j, "PROFILE_OBIS": "0.1.98.1.0.255"},
                    "DATAS": {"9300": monthly_time, "A213": "2099200", "0000": "4.688", "0300": "4.688",
                              "0400": "0.000",
                              "F710": "0.000", "F720": "0.000", "F730": "0.000", "F740": "0.000",
                              "0310": "3.519",
                              "0320": "0.000", "0330": "0.000", "0340": "1.169", "0410": "0.000",
                              "0420": "0.000",
                              "0430": "0.000", "0440": "0.000", "4300": "0.000", "4300T": "000101000000",
                              "4310": "0.000",
                              "4310T": "000101000000", "4320": "0.000", "4320T": "000101000000",
                              "4330": "0.000",
                              "4330T": "000101000000", "4340": "0.000", "4340T": "000101000000",
                              "4400": "0.000",
                              "4400T": "000101000000", "4410": "0.000", "4410T": "000101000000",
                              "4420": "0.000",
                              "4420T": "000101000000", "4430": "0.000", "4430T": "000101000000",
                              "4440": "0.000",
                              "4440T": "000101000000", "8330": "0.000"}, "MNO": meter_start + j,
                    "DTS": monthly_time,
                    "CTS": "220221154255", "SRC": "0", "DATA_INTERVAL": 0}
            )
        monthly_time = monthly_time + 100000000
    return payloads


@count_time
def hdataprofile(meter_start, meter_end, lp_count, lp_time):
    payloads = []
    for i in range(int(lp_count)):
        print('daily = ', lp_time)
        for j in range(meter_end - meter_start):
            payloads.append({
                "ADDITIONAL_INFO_MAP": {"COMM_DEVICE_NO": meter_start + j, "PROFILE_OBIS": "1.0.99.1.0.255"},
                "DATAS": {"9300": lp_time, "E300": "0.000", "E400": "0.000", "E110": "0.000",
                          "E120": "0.000",
                          "E130": "0.000", "E140": "0.000"}, "MNO": meter_start + j, "DTS": lp_time,
                "CTS": lp_time, "SRC": "0", "DATA_INTERVAL": 15})
            payloads.append({
                "ADDITIONAL_INFO_MAP": {"COMM_DEVICE_NO": meter_start + j, "PROFILE_OBIS": "1.0.99.1.2.255"},
                "DATAS": {"9300": lp_time, "8311": "224", "8391": "0.000", "8330": "1.000"},
                "MNO": meter_start + j, "DTS": lp_time, "CTS": lp_time, "SRC": "0",
                "DATA_INTERVAL": 15})
        lp_time = datetime.datetime.strptime(lp_time.__str__(), "%y%m%d%H%M%S")
        lp_time = (lp_time + datetime.timedelta(minutes=15)).strftime('%y%m%d%H%M%S')
    return payloads


if __name__ == "__main__":
    sleep_time = 0
    conf = {
        'bootstrap.servers': '10.32.233.63:30359',
        'client.id': 'Neon',
        'queue.buffering.max.messages': '1000000',
        'linger.ms' : 100

    }
    # conf = {'bootstrap.servers': '10.x.x.x:19092',
    # 'sasl.username': kafka_user, 'compression.codec':'snappy',
    # 'sasl.password': kafka_password, 'sasl.mechanisms':'PLAIN', 'security.protocol': 'SASL_PLAINTEXT',
    # 'message.max.bytes':'1000000000', 'queue.buffering.max.messages': '10000000', 'message.max.bytes' :'1000000000',
    # 'queue.buffering.max.kbytes': '2147483647', 'queue.buffering.max.ms' : '500', 'queue.buffering.max.messages':'10000000'}

    dailytopic = 'RELAY-CONFIG'
    monthlytopic = 'hdatamonthly'
    lptopic = 'hdataprofile'

    # print(py_kafka(dailytopic,hdatadaily(10000, 20000, 2, 220329000000)))

    # print('Daily Push: Meter No.100000~200000, Date 220301000000~220305000000')
    print(c_kafka(dailytopic, hdatadaily(100000, 200000, 10, 220329000000), sleep_time, **conf))
    # print('Monthly Push: Meter No.100000~20000, Date 220301000000~220701000000')
    # print(c_kafka(monthlytopic, hdatamonthly(100000, 200000, 5, 220301000000), sleep_time, **conf))
    # print('LP Push: Meter No.100000~20000, Date 220301000000~220701000000')
    # print(c_kafka(lptopic, hdataprofile(100000, 200000, 5, 220301000000), sleep_time, **conf))

    # 指定Offset消费
    topic = "RELAY-CONFIG"
    groupid = "Neon"
    brokerlist = "10.32.233.63:30359"

    # consumer = KafkaConsumer(bootstrap_servers=brokerlist,
    #                          auto_offset_reset='latest',
    #                          enable_auto_commit=True,  # 自动提交消费数据的offset
    #                          consumer_timeout_ms=10000,  # 如果1秒内kafka中没有可供消费的数据，自动退出
    #                          value_deserializer=lambda m: json.loads(m.decode('ascii')),  # 消费json 格式的消息
    #                          group_id='Neon')
    # partition = TopicPartition(topic, 0)
    # start = 2110170
    # end = 2110177
    # consumer.assign([partition])
    # consumer.seek(partition, start)
    #
    # for msg in consumer:
    #     if msg.offset > end:
    #         break
    #     else:
    #         print(msg)

    # consumer1 = KafkaConsumer(
    #     bootstrap_servers=brokerlist,
    #     # auto_offset_reset='earliest' , # 'earliest',
    #     # enable_auto_commit= False ,
    #     group_id='Neon',
    #     value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    # consumer1.subscribe("RELAY-CONFIG")
    # while True:
    #     msg = consumer1.poll(timeout_ms=5)
    #     print(msg)
    #     time.sleep(1)


    # 指定通道指定partition消费
    # consumer.assign([TopicPartition(topic, 0)])
    # for msg in consumer:
    #     print(msg)

    # msg = next(consumer)
    # print(msg)

    # consumer.subscribe('HesTaskProfile')
    # for msg in consumer:
    #     print(msg)
