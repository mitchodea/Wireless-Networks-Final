from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from confluent_kafka import Consumer, KafkaError

token = "#"
org = "myorg"
bucket = "Kafka-Consumer"
client = InfluxDBClient(url="#", token=token)
c = Consumer({
    'bootstrap.servers': '#',
    'security.protocol': 'sasl_plaintext',
    'auto.offset.reset': 'beginning',
    'group.id': 'my-group',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'sasl.username': '#',
    'sasl.password': '#'
})
c.subscribe(['region-04'])


def consume():
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        str = msg.value().decode('utf-8')
        sensorData = str.split(",")

        print(sensorData)

        region = sensorData[0]
        node = sensorData[1]
        temp = sensorData[2]
        humidity = sensorData[3]
        pressure = sensorData[4]
        elevation = sensorData[5]

        sequence = [f"{region},node={node} temp={temp}",
                    f"{region},node={node} humidity={humidity}",
                    f"{region},node={node} pressure={pressure}",
                    f"{region},node={node} elevation={elevation}"]

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, sequence)
consume()
