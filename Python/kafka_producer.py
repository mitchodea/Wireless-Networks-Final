import serial
import time
from confluent_kafka import Producer
ser=serial.Serial('COM4',9600)

p = Producer({
   'bootstrap.servers': '52.88.27.139:9092,54.188.70.115:9092,54.148.71.7:9092',
   'security.protocol':'sasl_plaintext',
   'sasl.mechanism':'SCRAM-SHA-256',
   'sasl.username':'ickafka',
   'sasl.password':'8dd926d510112b73d4bf2ad8a45c150873d01869eee76e0782fc0d2f65b85763'
    })

while True:
    serialData=str(ser.readline())
    sensorData=(serialData[2:][:-5])
    inputArray = sensorData.split(",")
    if (len(inputArray)<5):
        sensorData="0,0,0,0,0"
    
    print(sensorData)
    p.produce('region-04',sensorData.encode('utf-8'))
    p.flush()