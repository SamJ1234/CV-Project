#Blob detection program for videos. Performs the same fucnction as
#BlobPic.py, but with a video stream.

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

    
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        params = cv2.SimpleBlobDetector_Params()

        params.minThreshold = 5
        params.maxThreshold = 255
        
        params.minArea = 1000
        params.maxArea = 5000


        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(image)

        blank = np.zeros((1, 1))
        blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.putText(blobs, "Tic Tacs: {}".format(len(keypoints)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.75, (255, 0, 0), 2)
        
        params = cv2.SimpleBlobDetector_Params()

        params.minThreshold = 5
        params.maxThreshold = 255


        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(image)

        blank = np.zeros((1, 1))
        blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 255, 0),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.putText(blobs, "Tic Tacs: {}".format(len(keypoints)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.75, (255, 0, 0), 2) 
        cv2.imshow("Frame",blobs)
        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)
        
        if key ==ord("q"):
            cv2.destroyAllWindows()
            break