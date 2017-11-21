# Tomado de https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# y modificado con https://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/
# para poder usarlo con la picamera o con una webcam normal
# USAGE
# python face_tracking.py --video face_tracking_example.mp4
# python face_tracking_mejorado.py --picamera 1 si es con picamera
# python face_tracking_mejorado.py si es con una webcam normal

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from imutils.video import VideoStream
import time
import rects
from trackers import FaceTracker

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

camera = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

faceTracker = FaceTracker()

# keep looping
while True:
	# grab the current frame
	frame = camera.read()

	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=600)

	# Le damos la vuelta (efecto espejo)
	frame=cv2.flip(frame,1)
	
	faceTracker.update(frame)
	faces = faceTracker.faces
	faceTracker.drawDebugRects(frame)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
