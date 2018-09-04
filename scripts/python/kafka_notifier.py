#!/bin/python
# Heavily borrowing from https://www.confluent.io/blog/real-time-syslog-processing-with-apache-kafka-and-ksql-part-2-event-driven-alerting-with-slack/
# rmoff / 05 Apr 2018

from confluent_kafka import Consumer, KafkaError
from pushbullet import Pushbullet
import credentials



settings = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'python_pushbullet',
    'default.topic.config': {'auto.offset.reset': 'largest'}
}

pb = Pushbullet(credentials.login['api_token'])


c = Consumer(settings)
c.subscribe(['TEST'])


while True:
    msg = c.poll()

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {}'.format(msg.value().decode('utf-8')))
    push = pb.push_note("Kafka Notice!", 'Received message: {}'.format(msg.value().decode('utf-8')))


c.close()
