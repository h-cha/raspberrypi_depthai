import serial
import time
#import datetime
#import re
#count = 0

ser0 = serial.Serial('/dev/rfcomm0')
ser1 = serial.Serial('/dev/rfcomm1')

while(True):
    ser0.write("right".encode())
    ser1.write("left".encode())
   # print(ser.readline())
    time.sleep(5)
ser.close()
