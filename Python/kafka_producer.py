import serial
import struct
import time
# from confluent_kafka import Producer
ser=serial.Serial('/dev/ttyACM0',9600)

region = 4

transmissionStruct = '<b5f?'
transmissionSize = 1 + (5 * 4) + 1

# p = Producer({
#    'bootstrap.servers': '52.88.27.139:9092,54.188.70.115:9092,54.148.71.7:9092',
#    'security.protocol':'sasl_plaintext',
#    'sasl.mechanism':'SCRAM-SHA-256',
#    'sasl.username':'ickafka',
#    'sasl.password':'8dd926d510112b73d4bf2ad8a45c150873d01869eee76e0782fc0d2f65b85763'
#     })

while True:
    if ser.read(1) == b'\xaa':
        rawData = ser.read(transmissionSize)

        if ser.read(1) == b'\xee':
            transmission = struct.unpack(transmissionStruct, rawData)
    
            csvList = []
            csvList.append(f"node-{transmission[0]:02}")
            for value in transmission[1:]:
                csvList.append(f"{value}")
            csvString = ",".join(csvList)

            print(csvString)

            # p.produce('region-04',csvString.encode('utf-8'))
            # p.flush()
