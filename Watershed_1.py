#This is the watershed algorithm, which takes a
#picture and detects *touching* tic tacs. It is not very accurate.
#It is mainly copied from a PyImageSearch tutorial.
#There are two options starting at line 70 for the output image.

from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
 
# Set up camera for live picture option.
camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(1920, 1088))

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array


#Perform Mean Shift Filtering to aid in the thresholding step.
shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)


# convert the mean shift image to grayscale, then apply
# Otsu's thresholding
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
threshs = cv2.threshold(gray, 60, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(threshs, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

# compute the exact Euclidean distance from every binary
# pixel to the nearest zero pixel, then find peaks in this
# distance map
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=65,
	labels=thresh)

# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

# loop over the unique labels returned by the Watershed
# algorithm
for label in np.unique(labels):
	# if the label is zero, we are examining the 'background'
	# so simply ignore it
	if label == 0:
		continue
	
	# otherwise, allocate memory for the label region and draw
	# it on the mask
	mask = np.zeros(gray.shape, dtype="uint8")
	mask[labels == label] = 255
	
	# detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key=cv2.contourArea)
    #OPTION 1: Uncomment the following line to draw edge contours on output image.
    #cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
	
	#OPTION 2: Uncomment the following lines to draw circles on the output image.
	# draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
	cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
		cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
	
# show the output image
img = cv2.resize(image, (700, 380))
cv2.imshow("Output", img)
cv2.waitKey(0)