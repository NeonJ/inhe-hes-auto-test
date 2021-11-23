import json

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError


def producter(server, topict, content):
    producer = KafkaProducer(bootstrap_servers=server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topict, content)
    producer.close()


class Kafka_Producer():

    def __init__(self, kafkahost, kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers='{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort)
        )

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkatopic, value=parmas_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print(e)


class Kafka_Consumer():

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid=None, offset='smallest', key=None):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.key = key
        self.offset = offset
        self.consumer = KafkaConsumer(self.kafkatopic, auto_offset_reset=self.offset, group_id=self.groupid,
                                      bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort)]
                                      )

    def consume_data(self):
        print('Now start steaming topic-{}'.format(self.kafkatopic))
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)
