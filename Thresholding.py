#Uses thresholding and contour detection to outline
#the contours of objects and counts them.
#Not very accurate.

# Import libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

    
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# ims = cv2.imread('touch2.jpeg')
# image = cv2.resize(ims, (800, 480))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
plt.imshow(thresh)
plt.show()
(cnt, hierarchy) = cv2.findContours(
	thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
print("Tictacs in the image: ", len(cnt))

plt.imshow(rgb)
plt.show()
