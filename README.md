# Stream Smarts - Personal Data Anomoly Detection



| Overview | [Java](/docs/java.md) | [Notification](/docs/notification.md) |
|---|----|-----|

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

# Load a single record
echo '{"hour": 3, "mwh": 321}' | ./read_mwh kafka:29092

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



```
# build ksql-udf-iot.jar
ls -l ext/ksql-udf-iot.jar

# stop KSQL server
docker-compose stop ksql-server

# Replace the UDF ksql-udf-iot.jar
rm ext/ksql-udf-iot.jar
cp java/out/artifacts/ksql-udf-iot.jar ext

# Restrt KSQL server
docker-compose start ksql-server
```




## Setting up streams

```
create stream raw_power with (kafka_topic='raw_mwh', value_format='avro');

create stream  power_stream_rekeyed as select rowtime, hour, mwh, anomoly_power(hour, mwh) as fn from raw_power partition by rowtime;

create stream anomoly_power with (value_format='JSON') as select rowtime as event_ts, hour, mwh, fn from power_stream_rekeyed where fn>1.0;
```



## View 

# Compil Stuff
```
cd java
mvn clean package
ls target/ksql-udf-iot-1.0.jar
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