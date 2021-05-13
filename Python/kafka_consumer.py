from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from confluent_kafka import Consumer, KafkaError

token = "aplJXu9cQ6Iw7iucxKyv6DjXDtEzipc-Vrv8XfpmmAn7BVJyaA2yVMjVmrfcyT46-w3sZzMeZa8EXa9RmIQcIg=="
org = "myorg"
bucket = "Kafka-Consumer"
client = InfluxDBClient(url="http://3.25.197.187:8086", token=token)
c = Consumer({
    'bootstrap.servers': '52.88.27.139:9092,54.188.70.115:9092,54.148.71.7:9092',
    'security.protocol': 'sasl_plaintext',
    'auto.offset.reset': 'beginning',
    'group.id': 'my-group',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'sasl.username': 'ickafka',
    'sasl.password': '8dd926d510112b73d4bf2ad8a45c150873d01869eee76e0782fc0d2f65b85763'
})
c.subscribe(['region-09'])


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
        air_quality = sensorData[4]
        flame = sensorData[5]
        elevation = sensorData[6]
        pressure = sensorData[7]

        sequence = [f"{region},node={node} temp={temp}",
                    f"{region},node={node} humidity={humidity}",
                    f"{region},node={node} air_quality={air_quality}",
                    f"{region},node={node} flame={flame}",
                    f"{region},node={node} elevation={elevation}",
                    f"{region},node={node} pressure={pressure}"]

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, sequence)
consume()
