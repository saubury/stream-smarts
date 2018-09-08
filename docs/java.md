# Stream Smarts - Personal Data Anomoly Detection



| [Overview](/README.md) | Java | [Notification](/docs/notification.md) |[Random Notes](/docs/notes.md) |
|---|----|-----|-----|



# Java Overview

# Build and deploy KSQL User Defined Anomoly Functions

## Compile Code to Create Anomoly Functions
```
cd java
mvn clean package
ls target/ksql-udf-iot-1.0.jar
```

## Deploy KSQL User Defined Functions

```
# build ksql-udf-iot.jar as above
ls -l ext/ksql-udf-iot.jar

# stop KSQL server
docker-compose stop ksql-server

# Replace the UDF ksql-udf-iot.jar
rm ext/ksql-udf-iot.jar
cp java/out/artifacts/ksql-udf-iot.jar ext

# Restrt KSQL server
docker-compose start ksql-server
```


## Check KSQL User Defined Functions Available

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




