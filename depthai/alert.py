import serial
from config import labelMap

ser0 = serial.Serial('/dev/rfcomm0')
ser1 = serial.Serial('/dev/rfcomm1')

#############  TODO  ###########
##                            ##
## labelがcarの時だけalert      ##
##                            ##
################################

class AlertM5Stack:

    def send_message(self, frame, results):
        height = frame.shape[0]
        width  = frame.shape[1]
      
        for result in results:
            label = labelMap[result.label]
            # xは横軸
            x1 = int(result.xmin * width)
            x2 = int(result.xmax * width)

            locate = (x1 + x2) // 2
            center = width // 2

            # left
            if locate <= center:
                print("left")
                ser1.write("left".encode())
            # right
            else:
                print("right")
                ser0.write("right".encode())
        ser.close()



# while(True):
#     ser0.write("right".encode())
#     ser1.write("left".encode())
#    # print(ser.readline())
#     time.sleep(5)
# ser.close()
