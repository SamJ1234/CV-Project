#Uses canny to outline the contours of objects,
#then counts the contours.
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
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

#image = cv2.imread('touch4.jpeg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)
canny = cv2.Canny(blur, 5, 150, 3)
dilated = cv2.dilate(canny, (1, 1), iterations=0)

(cnt, hierarchy) = cv2.findContours(
	dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 8)

image = cv2.resize(rgb, (800, 480))
plt.imshow(image)
plt.show()

print("Tictacs in the image: ", len(cnt))
