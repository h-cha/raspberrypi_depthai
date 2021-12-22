import serial
import time
#import datetime
import re

ser = serial.Serial('COM3', 9600)



while(True):
	ser.write(b"1")
	
	time.sleep(60)
	



ser.close()