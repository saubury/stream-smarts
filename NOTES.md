
docker-compose exec schema-registry bash

pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url=https://pypi.org/simple/ confluent-kafka
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url=https://pypi.org/simple/ pushbullet.py

echo '{"f1": "value1"}' | kafka-console-producer --broker-list localhost:9092 --topic TEST




KSQL

SET 'auto.offset.reset' = 'earliest';
create stream raw_power with (kafka_topic='raw_mwh', value_format='avro');

create stream  power_stream_rekeyed as select rowtime, hour, mwh, anomoly_power(hour, mwh) as fn from raw_power partition by rowtime;

select timestamptostring(rowtime, 'yyyy-MM-dd HH:mm:ss'), rowtime as event_ts, hour, mwh, fn from power_stream_rekeyed2 where anomoly_power(hour, mwh)>1.0;


create stream anomoly_power with (value_format='JSON') as select rowtime as event_ts, hour, mwh, fn from power_stream_rekeyed where anomoly_power(hour, mwh)>1.0;



run script 'ksql_commands.ksql';