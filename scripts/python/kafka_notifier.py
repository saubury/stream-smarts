#!/bin/python
# Heavily borrowing from https://www.confluent.io/blog/real-time-syslog-processing-with-apache-kafka-and-ksql-part-2-event-driven-alerting-with-slack/
# rmoff / 05 Apr 2018

from confluent_kafka import Consumer, KafkaError
from pushbullet import Pushbullet
import json

# API keys held in a non-commited file
import credentials

# Subscribe to ANOMOLY_POWER topic
settings = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'python_pushbullet',
    'default.topic.config': {'auto.offset.reset': 'largest'}
}
c = Consumer(settings)
c.subscribe(['ANOMOLY_POWER'])

# Connect to pushbullet service
pb = Pushbullet(credentials.login['api_token'])

# Poll for messages; and extract JSON and call pushbullet for any messages
while True:
    msg = c.poll()
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    app_json_msg = json.loads(msg.value().decode('utf-8'))
    push = pb.push_note('Unusal power usage of {:.0f} MWh at {:.0f}:00.  Perhaps you have left something running?'.format( app_json_msg['MWH']
       , app_json_msg['HOUR']),     'Full message: {}'.format( app_json_msg))

c.close()
