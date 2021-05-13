import serial
import struct
import time
from confluent_kafka import Producer
ser=serial.Serial('COM8',9600)

region = 9

transmissionStruct = '<b6f'
transmissionSize = 1 + (6 * 4)

p = Producer({
   'bootstrap.servers': '#',
    'security.protocol':'sasl_plaintext',
    'sasl.mechanism':'SCRAM-SHA-256',
    'sasl.username':'#',
    'sasl.password':'#'
     })

while True:
    if ser.read(1) == b'\xaa':
        rawData = ser.read(transmissionSize)

        if ser.read(1) == b'\xee':
            transmission = struct.unpack(transmissionStruct, rawData)
    
            csvList = [f"region-{region:02}"]
            csvList.append(f"node-{transmission[0]:02}")
            for value in transmission[1:]:
                csvList.append(f"{value}")
            csvString = ",".join(csvList)

            print(csvString)

            p.produce(csvList[0],csvString.encode('utf-8'))
            p.flush()
