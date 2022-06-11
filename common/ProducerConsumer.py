import json
# import jsonpath

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
            kafka_port=self.kafkaPort, ack=0)
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

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid='test-consumer-group1', offset='smallest', key=None):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.offset = offset
        self.groupid = groupid
        self.key = key
        self.consumer = KafkaConsumer(self.kafkatopic, group_id=self.groupid, auto_offset_reset=self.offset,
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

    def dealFilter(self, filters, connectType):
        sentence = ''
        for n, f in enumerate(filters):
            idx = f.find(' ')
            col = f[:idx]
            condition = f[idx:]
            tmp = "jsonpath.jsonpath(data,'$..{0}')[0]".format(col) + ' ' + condition
            if n != 0:
                sentence = connectType + sentence
            sentence = tmp + sentence
        return sentence

    def dataFilter(self, data, filter=''):
        filter = filter.replace('=', '==')
        if filter:
            if 'and' in filter:
                filter = filter.split('and')
                filter_sentence = self.dealFilter(filter, 'and')
            else:
                filter = filter.split('or')
                filter_sentence = self.dealFilter(filter, 'and')
            if eval(filter_sentence):
                return data
        else:
            return data

    def get_data(self, code='15a152a9-19eb-447f-b034-9cefe9a5f93f'):
        for msg in self.consumer:
            data = msg.value
            # data = self.dataFilter(eval(str(data, 'utf-8')), filter)
            if code in str(data,'utf-8'):
                print(data)

if __name__ == '__main__':
    Kafka_Consumer('10.32.233.127', 30753, 'dev-communication-log').get_data()
