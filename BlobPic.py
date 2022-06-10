#Blob detection program for live pictures.
#Converts picture to grayscale, inputs it into the BlobDetector function,
#then outputs the resulting image with text.

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

    
camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1920, 1088))

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
img = rawCapture.array
image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

params = cv2.SimpleBlobDetector_Params()

params.minThreshold = 5
params.maxThreshold = 255

params.minArea = 25
params.maxArea = 2000000

detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(image)

blank = np.zeros((1, 1))
blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.putText(blobs, "Tic Tacs: {}".format(len(keypoints)), (40, 80), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 2)

ims = cv2.resize(blobs, (700, 380))
cv2.imshow("Frame", ims)
key = cv2.waitKey(0)
