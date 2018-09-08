# Stream Smarts - Personal Data Anomoly Detection



| Overview | [Java](/docs/java.md) | [Notification](/docs/notification.md) |[Random Notes](/docs/notes.md) |
|---|----|----|-----|

## Architectural overview

Continuous home power consumption monitoring ..  with anomaly detection.  

![Architecture](/docs/smarts.png)

Alerting using deep learning function for Apache Kafka's KSQL

# Inspiration
https://github.com/kaiwaehner/ksql-udf-deep-learning-mqtt-iot

## Prerequisites & setup
- clone this repo!
- install docker/docker-compose
- set your Docker maximum memory to something really big, such as 22GB. (preferences -> advanced -> memory)


## Startup
```
# This will take a while the first time
docker-compose up -d
```


## Data Loading

Jump _into_ the `schema-registry` container 

```
docker-compose exec schema-registry bash


# Note, you are navigating within the container
cd /scripts

# Load demonstration records
echo '{"hour": 4, "kwh": 1500}' | ./read_power kafka:29092
echo '{"hour": 9, "kwh": 1500}' | ./read_power kafka:29092

# Now exit
exit
```

## Running KSQL CLI
To connect to KSQL CLI
```
docker-compose exec ksql-cli ksql "http://ksql-server:8088"

                  ===========================================
                  =        _  __ _____  ____  _             =
                  =       | |/ // ____|/ __ \| |            =
                  =       | ' /| (___ | |  | | |            =
                  =       |  <  \___ \| |  | | |            =
                  =       | . \ ____) | |__| | |____        =
                  =       |_|\_\_____/ \___\_\______|       =
                  =                                         =
                  =  Streaming SQL Engine for Apache Kafka® =
                  ===========================================

Copyright 2017-2018 Confluent Inc.

CLI v5.0.0, Server v5.0.0 located at http://ksql-server:8088
```

And try something like
```
ksql> show topics;
```


# Build and deploy KSQL User Defined Anomoly Functions

- The user defined function is a Java classes in `ksql-udf-iot.jar` build artifact

Start `ksql` client and verify 

```
ksql> list functions;

 Function Name           | Type
-------------------------------------
  . . .
 ANOMOLY_LOCATION        | SCALAR
 ANOMOLY_POWER           | SCALAR   <--- You need this one
 ANOMOLY_WATER           | SCALAR
```





## Setting up streams

```

SET 'auto.offset.reset' = 'earliest';

create stream raw_power_stream with (kafka_topic='raw_power', value_format='avro');

create stream  power_stream_rekeyed as select rowtime, hour, kwh, anomoly_power(hour, kwh) as fn from raw_power_stream partition by rowtime;

select timestamptostring(rowtime, 'yyyy-MM-dd HH:mm:ss'), hour, kwh, fn from  power_stream_rekeyed;
2018-09-08 04:21:44 | 4.0 | 1500.0 | 5.458823529411765
2018-09-08 04:21:59 | 9.0 | 1500.0 | 0.6913887506222001

create stream anomoly_power with (value_format='JSON') as select rowtime as event_ts, hour, kwh, fn from power_stream_rekeyed where fn>1.0;
```



## View 



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