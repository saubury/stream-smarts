
```
docker-compose up -d
```

http://localhost:9021

```
kafka-avro-console-producer  \
--broker-list localhost:9092 \
--topic raw_power              \
--property value.schema='
{
  "type": "record",
  "name": "myrecord",
  "fields": [
    {
      "name": "hour",
      "type": "float"
    },
     {
      "name": "kwh",
      "type": "float"
    }
  ]
}'

{"hour": 9, "kwh": 1500}
```

cd scripts/
echo '{"hour": 9, "kwh": 1500}' | ./read_power

## KSQL
```
show topics;

list functions;

describe function ANOMOLY_POWER;

SET 'auto.offset.reset' = 'earliest';

create stream raw_power_stream with (kafka_topic='raw_power', value_format='avro');

create stream  power_stream_rekeyed as 
select rowtime, hour, kwh, anomoly_power(hour, kwh) as fn 
from raw_power_stream partition by rowtime;

select timestamptostring(rowtime, 'yyyy-MM-dd HH:mm:ss'), hour, kwh, fn 
from  power_stream_rekeyed limit 1;


create stream anomoly_power with (value_format='JSON') as 
select rowtime as event_ts, hour, kwh, fn 
from power_stream_rekeyed where fn>1.0;

select * from anomoly_power;
```

# Load a non-anomoly record
# Note that no records are returned in the other terminal ksql query
```
echo '{"hour": 9, "kwh": 1500}' | ./read_power 
```

# Load an anomoly record
# Note that a record should be returned in the other terminal  ksql query
```
echo '{"hour": 4, "kwh": 1500}' | ./read_power 
```

## Run notifier 
```
docker-compose exec kafka-notifier python /scripts/python/kafka_notifier.py
```