import serial
import time
from confluent_kafka import Producer
ser=serial.Serial('COM4',9600)

transmissionStruct = 'b<b<hf'
transmissionSize = 1 + 1 + 2 + 4

p = Producer({
   'bootstrap.servers': '52.88.27.139:9092,54.188.70.115:9092,54.148.71.7:9092',
   'security.protocol':'sasl_plaintext',
   'sasl.mechanism':'SCRAM-SHA-256',
   'sasl.username':'ickafka',
   'sasl.password':'8dd926d510112b73d4bf2ad8a45c150873d01869eee76e0782fc0d2f65b85763'
    })

while True:
    while ser.read(1) != 0xaa:
        rawData = ser.read(transmissionSize)

        if ser.read(1) == 0xee:
            transmission = unpack(transmissionStruct, rawData)
    
            print(f"node-{transmission[0]}:\n\
                    \tv1: {transmission[1]}\n\
                    \tv2: {transmission[2]}\n\
                    \tv3: {transmission[3]}\n")
            p.produce('region-04',)
            p.flush()