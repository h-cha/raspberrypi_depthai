import serial
import logging
import cv2
log = logging.getLogger(__name__)

# ser0 = serial.Serial('/dev/rfcomm0')
# ser1 = serial.Serial('/dev/rfcomm1')
# ser1 = serial.Serial('/dev/tty.M5StackLEFT')
# ser0 = serial.Serial('/dev/tty.M5StackRIGHT')


#############  TODO  ###########
##                            ##
## labelがcarの時だけalert      ##
##                            ##
################################

class AlertM5Stack:
    def __init__(self):
        self.ONOFF = False
        self.count = 0

    def parse_frame(self, results):
        
        for i, tracking in enumerate(results):
            # if tracking['now_distance'] > 0 and tracking['status'] != 'LOST' and self.count % 2 == 0:
            if tracking['now_distance'] > 0 and tracking['status'] != 'LOST':    
                self.ONOFF = True
                # ser0.write(b"2")
                print(tracking['now_distance'])
                print("dangerOn")
                self.count += 1
            elif tracking['dangerous'] == True and tracking['status'] != 'LOST':
            # if tracking['dangerous'] == True and tracking['status'] != 'LOST':
                if self.ONOFF == False:
                    self.ONOFF = True
                    # ser0.write(b"1")
                    # print(tracking['now_distance'])
                    print("On")
            else:
                if self.ONOFF == True:
                    self.ONOFF = False
                    # ser0.write(b"0")
                    print("OFF")