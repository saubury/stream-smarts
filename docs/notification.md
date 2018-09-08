# Stream Smarts - Personal Data Anomoly Detection



| [Overview](/README.md) | [Java](/docs/java.md) | Notification|[Random Notes](/docs/notes.md)  |
|---|----|----|-----|




## Setup
- Follow the setup in [readme](/README.md) 
- The stream `anomoly_power` should be running
- By _subscribing_ to the `anomoly_power` topic we can build a notification for significant events

## Configure Pushbullet API

- Get a Push Bullet account
- Install on your phone
- Get an API Token at 
https://www.pushbullet.com/#settings/account
- Set this line in `credentials.py`

```
login = {
    'api_token' : 'ITISASECRET'
}
```

## Run Python Subscriber

```
docker-compose exec kafka-notifier python /scripts/python/kafka_notifier.py
```

![Notification](/docs/notif.png)

