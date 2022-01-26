import uuid
from pathlib import Path

import blobconverter
import cv2
import depthai as dai
from imutils.video import FPS
import time
import argparse
from datetime import datetime, timedelta
from arg_manager import parseArgs

syncNN = True
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


class DepthAI:
    def create_pipeline(self):
        args = parseArgs()
        print("Creating DepthAI pipeline...")
        # Start defining a pipeline
        pipeline = dai.Pipeline()

        # Define a source - color camera
        colorCam = pipeline.createColorCamera()
        spatialDetectionNetwork = pipeline.createMobileNetSpatialDetectionNetwork()
        monoLeft = pipeline.createMonoCamera()
        monoRight = pipeline.createMonoCamera()
        stereo = pipeline.createStereoDepth()
        objectTracker = pipeline.createObjectTracker()

        xoutRgb = pipeline.createXLinkOut()
        xoutNN = pipeline.createXLinkOut()
        xoutBoundingBoxDepthMapping = pipeline.createXLinkOut()
        xoutDepth = pipeline.createXLinkOut()
        xoutTracker = pipeline.createXLinkOut()

        xoutRgb.setStreamName("rgb")
        xoutNN.setStreamName("detections")
        xoutBoundingBoxDepthMapping.setStreamName("boundingBoxDepthMapping")
        xoutDepth.setStreamName("depth")
        xoutTracker.setStreamName("tracklets")


        colorCam.setPreviewSize(300, 300)
        colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        colorCam.setInterleaved(False)
        colorCam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        colorCam.setPreviewKeepAspectRatio(False)

        monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        # Setting node configs
        stereo.setOutputDepth(True)
        stereo.setConfidenceThreshold(255)

        # spatialDetectionNetwork.setBlobPath(nnBlobPath)
        spatialDetectionNetwork.setBlobPath(str(blobconverter.from_zoo(name='mobilenet-ssd', shaves=6)))
        spatialDetectionNetwork.setConfidenceThreshold(0.5)
        spatialDetectionNetwork.input.setBlocking(False)
        spatialDetectionNetwork.setBoundingBoxScaleFactor(0.5)
        spatialDetectionNetwork.setDepthLowerThreshold(100)
        # spatialDetectionNetwork.setDepthUpperThreshold(5000)

        # Create outputs

        monoLeft.out.link(stereo.left)
        monoRight.out.link(stereo.right)

        colorCam.preview.link(spatialDetectionNetwork.input)

        # fullFrame
        if args.full_frame:
            colorCam.video.link(xoutRgb.input)
        else:
            spatialDetectionNetwork.passthrough.link(xoutRgb.input)

        spatialDetectionNetwork.out.link(xoutNN.input)
        spatialDetectionNetwork.boundingBoxMapping.link(xoutBoundingBoxDepthMapping.input)

        stereo.depth.link(spatialDetectionNetwork.inputDepth)
        spatialDetectionNetwork.passthroughDepth.link(xoutDepth.input)

        objectTracker.passthroughTrackerFrame.link(xoutRgb.input)

        if args.tracking_target_person:
            objectTracker.setDetectionLabelsToTrack([15])  # track only person
        else:
            objectTracker.setDetectionLabelsToTrack([7])  # track only car

        # possible tracking types: ZERO_TERM_COLOR_HISTOGRAM, ZERO_TERM_IMAGELESS
        objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
        # take the smallest ID when new object is tracked, possible options: SMALLEST_ID, UNIQUE_ID
        objectTracker.setTrackerIdAssigmentPolicy(dai.TrackerIdAssigmentPolicy.SMALLEST_ID)

        # fullFrame
        if args.full_frame:
            colorCam.video.link(objectTracker.inputTrackerFrame)
        else:
            spatialDetectionNetwork.passthrough.link(objectTracker.inputTrackerFrame)

        spatialDetectionNetwork.passthrough.link(objectTracker.inputDetectionFrame)
        spatialDetectionNetwork.out.link(objectTracker.inputDetections)
        objectTracker.out.link(xoutTracker.input)

        print("Pipeline created.")
        return pipeline

    def __init__(self):
        self.pipeline = self.create_pipeline()
        self.detections = []

    def capture(self):
        with dai.Device(self.pipeline) as device:
            # Start pipeline
            device.startPipeline()

            # Output queues will be used to get the rgb frames and nn data from the outputs defined above
            previewQueue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            detectionNNQueue = device.getOutputQueue(name="detections", maxSize=4, blocking=False)
            xoutBoundingBoxDepthMapping = device.getOutputQueue(name="boundingBoxDepthMapping", maxSize=4, blocking=False)
            depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
            trackQueue = device.getOutputQueue(name="tracklets", maxSize=4, blocking=False)

            frame = None
            detections = []

            startTime = time.monotonic()
            counter = 0
            fps = 0
            color = (255, 255, 255)

            while True:
                inPreview = previewQueue.get()
                inNN = detectionNNQueue.get()
                # depth = depthQueue.get()
                track = trackQueue.get()

                counter+=1
                current_time = time.monotonic()
                if (current_time - startTime) > 1 :
                    fps = counter / (current_time - startTime)
                    counter = 0
                    startTime = current_time

                frame = inPreview.getCvFrame()
                # depthFrame = depth.getFrame()

                # depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
                # depthFrameColor = cv2.equalizeHist(depthFrameColor)
                # depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)
                detections = inNN.detections
                # if len(detections) != 0:
                #     boundingBoxMapping = xoutBoundingBoxDepthMapping.get()
                #     roiDatas = boundingBoxMapping.getConfigData()

                #     for roiData in roiDatas:
                #         roi = roiData.roi
                #         # roi = roi.denormalize(depthFrameColor.shape[1], depthFrameColor.shape[0])
                #         topLeft = roi.topLeft()
                #         bottomRight = roi.bottomRight()
                #         xmin = int(topLeft.x)
                #         ymin = int(topLeft.y)
                #         xmax = int(bottomRight.x)
                #         ymax = int(bottomRight.y)

                #         # cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)


                # If the frame is available, draw bounding boxes on it and show the frame
                height = frame.shape[0]
                width  = frame.shape[1]
                # for detection in detections:
                #     # Denormalize bounding box
                #     x1 = int(detection.xmin * width)
                #     x2 = int(detection.xmax * width)
                #     y1 = int(detection.ymin * height)
                #     y2 = int(detection.ymax * height)
                #     try:
                #         label = labelMap[detection.label]
                #     except:
                #         label = detection.label
                    # cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                    # cv2.putText(frame, "{:.2f}".format(detection.confidence*100), (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                    # cv2.putText(frame, f"X: {int(detection.spatialCoordinates.x)} mm", (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                    # cv2.putText(frame, f"Y: {int(detection.spatialCoordinates.y)} mm", (x1 + 10, y1 + 65), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                    # cv2.putText(frame, f"Z: {int(detection.spatialCoordinates.z)} mm", (x1 + 10, y1 + 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)

                    # cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

                # cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)
                # cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 0), thickness=5, lineType=cv2.LINE_4)
                # cv2.imshow("depth", depthFrameColor)
                # cv2.imshow("rgb", frame)

                bboxes = []
                # height = frame.shape[0]
                # width  = frame.shape[1]
                # for detection in self.detections:
                #     bboxes.append({
                #         'id': uuid.uuid4(),
                #         'label': detection.label,
                #         'confidence': detection.confidence,
                #         'x_min': int(detection.xmin * width),
                #         'x_max': int(detection.xmax * width),
                #         'y_min': int(detection.ymin * height),
                #         'y_max': int(detection.ymax * height),
                #         'depth_x': detection.spatialCoordinates.x / 1000,
                #         'depth_y': detection.spatialCoordinates.y / 1000,
                #         'depth_z': detection.spatialCoordinates.z / 1000,
                #     })

                trackletsData = track.tracklets
                for t in trackletsData:
                    # Denormalize bounding box
                    # x1 = int(t.xmin * width)
                    # x2 = int(t.xmax * width)
                    # y1 = int(t.ymin * height)
                    # y2 = int(t.ymax * height)
                    roi = t.roi.denormalize(frame.shape[1], frame.shape[0])

                    x1 = int(roi.topLeft().x)
                    y1 = int(roi.topLeft().y)
                    x2 = int(roi.bottomRight().x)
                    y2 = int(roi.bottomRight().y)
 
 



                    try:
                        label = labelMap[t.label]
                    except:
                        label = t.label

                    statusMap = {dai.Tracklet.TrackingStatus.NEW : "NEW", dai.Tracklet.TrackingStatus.TRACKED : "TRACKED", dai.Tracklet.TrackingStatus.LOST : "LOST", dai.Tracklet.TrackingStatus.REMOVED : "REMOVED" }
                    # cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 1, color)
                    # cv2.putText(frame, f"ID: {[t.id]}", (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_TRIPLEX, 1, color)
                    # cv2.putText(frame, statusMap[t.status], (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_TRIPLEX, 1, color)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

                    # cv2.putText(frame, f"X: {int(t.spatialCoordinates.x / 1000)} m", (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 1, color)
                    # cv2.putText(frame, f"Y: {int(t.spatialCoordinates.y / 1000)} m", (x1 + 10, y1 + 60), cv2.FONT_HERSHEY_TRIPLEX, 1, color)
                    cv2.putText(frame, f"{int(t.spatialCoordinates.z / 1000)} m", (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 1, color)

                    bboxes.append({
                        'id': t.id,
                        'label': t.label,
                        # 'confidence': t.confidence,
                        'x_min': int(roi.topLeft().x),
                        'x_max': int(roi.bottomRight().x),
                        'y_min': int(roi.topLeft().y),
                        'y_max': int(roi.bottomRight().y),
                        'depth_x': t.spatialCoordinates.x / 1000,
                        'depth_y': t.spatialCoordinates.y / 1000,
                        'depth_z': t.spatialCoordinates.z / 1000,
                        'status': statusMap[t.status],
                        'time': datetime.now(),
                    })

                cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 1, color)

                cv2.imshow("tracker", frame)

                if cv2.waitKey(1) == ord('q'):
                    break
                
                yield frame, bboxes