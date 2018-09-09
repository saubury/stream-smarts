#!/bin/python
# Heavily borrowing from https://www.confluent.io/blog/real-time-syslog-processing-with-apache-kafka-and-ksql-part-2-event-driven-alerting-with-slack/
# rmoff / 05 Apr 2018

from confluent_kafka import Consumer, KafkaError
from pushbullet import Pushbullet
import json
import requests


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
pb = Pushbullet(credentials.login['pushbullet_api_token'])

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

    # Send a push notification to phone via push-bullet
    push = pb.push_note('Unusual power usage of {:.0f} Wh at {:.0f}:00.   Please check!'.format( app_json_msg['KWH']
       , app_json_msg['HOUR']),     'Full message: {}'.format( app_json_msg))

    # Notifiy GoogleHome via Hass.io - Home Assistant
    # url = 'http://192.168.1.195:8123/api/services/tts/google_say?api_password={}'.format(credentials.login['hassio_password'])
    # data = '{"entity_id": "media_player.office_speaker", "message": "Warning. The power usage is more than expected"}'
    # response = requests.post(url, data=data)


c.close()
