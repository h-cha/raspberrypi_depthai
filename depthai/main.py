import logging
import math

import cv2
import numpy as np

from alert import AlertM5Stack
from config import labelMap
from depthai_utils import DepthAI
from distance import DistanceGuardian, DistanceGuardianDebug



class Main:
    depthai_class = DepthAI
    distance_guardian_class = DistanceGuardian
    alert_class = AlertM5Stack

    def __init__(self):
        self.depthai = self.depthai_class()
        self.distance_guardian = self.distance_guardian_class()
        self.alert = self.alert_class()

    def parse_frame(self, frame, results):
        distance_results = self.distance_guardian.parse_frame(frame, results)
        should_alert = self.alert.parse_frame(distance_results)
        # if should_alert:
        #     img_h = frame.shape[0]
        #     img_w = frame.shape[1]
        #     cv2.putText(frame, "Too close", (int(img_w / 3), int(img_h / 2)), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 1)
        return distance_results

    def run(self):
        try:
            print("Setup complete, parsing frames...")
            for frame, results in self.depthai.capture():
                # cv2.imshow("new", frame)
                self.parse_frame(frame, results)
                # self.alert.send_message(detections)
            # self.depthai.capture()
        finally:
            del self.depthai


if __name__ == '__main__':
    Main().run()
