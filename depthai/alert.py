import serial
from config import labelMap
import time

#ser0 = serial.Serial('/dev/rfcomm0')
# ser1 = serial.Serial('/dev/rfcomm1')
# ser1 = serial.Serial('/dev/tty.M5StackLEFT')
#ser0 = serial.Serial('/dev/tty.M5StackRIGHT')
ONOFF = False

#############  TODO  ###########
##                            ##
## labelがcarの時だけalert      ##
##                            ##
################################

class AlertM5Stack:

    def send_message(self, results):
        height = 300
        width  = 300
        count = 0
      
        for result in results:
            print(result["depth_z"])
            # person 
            #if ONOFF == False:
            #   if result["label"] == 15 and result["depth_x"] < 10 :
            #       ser0.write(b"1")
            #       ONOFF = True
            # else:
            #   print(ONOFF)
            #   if result["label"] == 15 and result["depth_x"] > 10 :
            #       ser0.write(b"0")
            #       ONOFF = False


            # person tracking
            #if ONOFF == False:
            #   if result["label"] == 15 and result["depth_x"] < 10 :
            #       ser0.write(b"1")
            #       ONOFF = True
            # else:
            #   print(ONOFF)
            #   if result["label"] == 15 and result["depth_x"] > 10 :
            #       ser0.write(b"0")
            #       ONOFF = False



            # label = labelMap[result.label]
            # xは横軸
            # x1 = int(result.xmin * width)
            # x2 = int(result.xmax * width)

            # locate = (x1 + x2) // 2
            # center = width // 2
            

            # left
            # if locate <= center:
            #     print("left")
                # ser1.write(b"1")
                # time.sleep(2)
            # right
            # else:
            #     print("right")
            #     if count % 3 == 0:
            #         ser0.write(b"1")
            # count += 1
            # time.sleep(2)
            
        # ser0.close()


# while(True):
#     ser0.write("right".encode())
#     ser1.write("left".encode())
#    # print(ser.readline())
#     time.sleep(5)
# ser.close()
