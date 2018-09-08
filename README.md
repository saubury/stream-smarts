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
- set your Docker maximum memory to something really big, such as 10GB. (preferences -> advanced -> memory)


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

-  For this quickstart you'll find the Java class `ksql-udf-iot.jar` is already in the `ext` directory; and the ksql-server should have loaded it
- *Optional* : if you want to build your own `ksql-udf-iot.jar` and deploy follow the [Java Steps](/docs/java.md) 
- Run these ksql commands to check you can see the UDF `ANOMOLY_POWER`
```
ksql> list functions;

 Function Name           | Type
-------------------------------------
  . . .
 ANOMOLY_LOCATION        | SCALAR
 ANOMOLY_POWER           | SCALAR   <--- Has been loaded from ksql-udf-iot.jar
 ANOMOLY_WATER           | SCALAR
```





## Setting up streams

- Now we will create the streams
```
SET 'auto.offset.reset' = 'earliest';

create stream raw_power_stream with (kafka_topic='raw_power', value_format='avro');

create stream  power_stream_rekeyed as \
select rowtime, hour, kwh, anomoly_power(hour, kwh) as fn \
from raw_power_stream partition by rowtime;

select timestamptostring(rowtime, 'yyyy-MM-dd HH:mm:ss'), hour, kwh, fn \
from  power_stream_rekeyed limit 1;

    2018-09-08 11:34:37 | 9.0 | 1500.0 | 0.6913887506222001
    Limit Reached
    Query terminated

create stream anomoly_power with (value_format='JSON') as \
select rowtime as event_ts, hour, kwh, fn \
from power_stream_rekeyed where fn>1.0;
```

- The stream `anomoly_power` is now running.  It will only produce records for significant events.  By _subscribing_ to the `anomoly_power` topic we can build a notification for significant events

## View 
- In the ksql window, start a query like this looking for anomoly records. Keep this query running
```
select * from anomoly_power;
```

- In *another* session 
```
docker-compose exec schema-registry bash

# Note, you are navigating within the container
cd /scripts

# Load a non-anomoly record
# Note that no records are returned in the other terminal ksql query
echo '{"hour": 9, "kwh": 1500}' | ./read_power kafka:29092

# Load an anomoly record
# Note that a record should be returned in the other terminal  ksql query
echo '{"hour": 4, "kwh": 1500}' | ./read_power kafka:29092

# Now exit
exit
```

## What did we see?
- Running a query using the `ANOMOLY_POWER` function allowed a predifined model to be used within a KSQL query
- The stream `anomoly_power` stream created a topic which only had events that breached the limit of the model
- By _subscribing_ to the `anomoly_power` we can build a notification for significant events

## Build a notifier
- If you are keen - go on to [Notification](/docs/notification.md)

## Shutdown and cleanup
```
docker-compose down
```



