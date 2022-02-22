import serial
import string
import time

ser=serial.Serial('/dev/ttyUSB2', 9600)

potVals = [0,0,0,0]
while True:
    serialData=ser.readline()
    if serialData == "Start":
        for i in range(0,4):
            potVals[i] = ser.readline()
        print(potVals)