import serial
import time
#import datetime
#import re
#count = 0

# ser0 = serial.Serial('/dev/rfcomm0')
# ser1 = serial.Serial('/dev/rfcomm1')
ser0 = serial.Serial('/dev/tty.M5StackRIGHT')

while(True):
    ser0.write(b"1")
    # ser1.write("left".encode())
   # print(ser.readline())
    print(1)
    time.sleep(5)
ser.close()
