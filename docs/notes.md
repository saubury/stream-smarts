| [Overview](/README.md) | [Java](/docs/java.md) | [Notification](/docs/notification.md) |Random Notes |
|---|----|----|-----|


# Python
```
docker-compose exec schema-registry bash

pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url=https://pypi.org/simple/ confluent-kafka
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url=https://pypi.org/simple/ pushbullet.py

echo '{"f1": "value1"}' | kafka-console-producer --broker-list localhost:9092 --topic TEST
```


# CLI
```
echo $PS1
\[\033[36m\]\u:\[\033[33;1m\]\W\[\033[m\]\$
```

# KSQL
```
SET 'auto.offset.reset' = 'earliest';
create stream raw_power with (kafka_topic='raw_mwh', value_format='avro');

create stream  power_stream_rekeyed as select rowtime, hour, mwh, anomoly_power(hour, mwh) as fn from raw_power partition by rowtime;

select timestamptostring(rowtime, 'yyyy-MM-dd HH:mm:ss'), rowtime as event_ts, hour, mwh, fn from power_stream_rekeyed2 where anomoly_power(hour, mwh)>1.0;


create stream anomoly_power with (value_format='JSON') as select rowtime as event_ts, hour, mwh, fn from power_stream_rekeyed where anomoly_power(hour, mwh)>1.0;



run script 'ksql_commands.ksql';

```

# Docker build
```
WARNING: Image for service kafka-notifier was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
```

# Git - don't checkin secrets
```
 git update-index --assume-unchanged scripts/python/credentials.py
 ```

# Function Results

```

2018-09-08 04:51:49 | 4.0 | 100.0 | -0.03137254901960784
2018-09-08 04:51:49 | 4.0 | 1500.0 | 5.458823529411765
2018-09-08 04:51:49 | 4.0 | 3000.0 | 11.341176470588236

2018-09-08 04:51:49 | 9.0 | 100.0 | -0.0054753608760577405
2018-09-08 04:51:49 | 9.0 | 1500.0 | 0.6913887506222001
2018-09-08 04:51:49 | 9.0 | 3000.0 | 1.438028870084619

2018-09-08 04:51:49 | 20.0 | 100.0 | -0.0021996150673632116
2018-09-08 04:51:49 | 20.0 | 1500.0 | 0.3827330217211988
2018-09-08 04:51:49 | 20.0 | 3000.0 | 0.7951608468518009


{"hour": 4, "kwh": 100}
{"hour": 9, "kwh": 100}
{"hour": 20, "kwh": 100}
{"hour": 4, "kwh": 1500}
{"hour": 9, "kwh": 1500}
{"hour": 20, "kwh": 1500}
{"hour": 4, "kwh": 3000}
{"hour": 9, "kwh": 3000}
{"hour": 20, "kwh": 3000}

```


## Other Data Loading Examples

Jump _into_ the `schema-registry` container 

```
docker-compose exec schema-registry bash


# Note, you are navigating within the container
cd /scripts


# Load a day worth of data
cat mwh_20180805.json | ./read_mwh kafka:29092

# Or pass in slowly like this
cat mwh_20180805.json | while read line; do echo $line; sleep 1; done | ./read_mwh kafka:29092

# Now exit
exit
```
