# -*- coding: cp1252 -*-
# Tomado de https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# y modificado con https://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/
# para poder usarlo con la picamera o con una webcam normal
# El objetivo es medir el color de un pixel central cada vez que pulse la barra espaciadora.
# USAGE
# python mide_color.py --picamera 1 si es con picamera o sin parámetro picamera si es con una webcam normal

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from imutils.video import VideoStream
import time

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
greenLower = (26, 144, 196)
greenUpper = (32, 250, 215)
pts = deque(maxlen=args["buffer"])

camera = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

font = cv2.FONT_HERSHEY_SIMPLEX


# keep looping
while True:
	# grab the current frame
	frame = camera.read()

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)

        # Le damos la vuelta
        frame=cv2.flip(frame,1)
        
        #cv2.putText(frame,"width="+str(width)+ " height="+str(height),(225,300), font, 1,(255,255,255),2)


	
	#print "dimensiones imagen:", frame.shape
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

        
        #cv2.putText(frame,"cnts="+str(cnts),(300,30), font, 0.7,(255,255,255),2)
        cv2.putText(frame,"cnts="+str(len(cnts)),(5,30), font, 0.7,(255,255,255),2)
        # Pintamos un circulo alrededor del pixel central pero atencion porque las
        # coordenadas aqui son columna y fila
        cv2.circle(frame,(330,225), 10, (0,255,0), 3)

        # Leemos el pixel central pero atencion porque las
        # coordenadas aqui son fila y columna
        px = frame[225,330] 
        # cprint "pixel central=", px
        cv2.putText(frame,"cnts="+str(len(cnts))+". px="+str(px),(5,30), font, 0.9,(255,255,255),2)
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points queue
#	pts.appendleft(center)

	# loop over the set of tracked points
#	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
#		if pts[i - 1] is None or pts[i] is None:
#			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
#		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
#		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # px = frame[330,225]
        # print "pixel central=", px
        # cv2.circle(frame,(330,225), 5, (0,255,0), -1)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# key = cv2.waitKey(0)

	# if the 'p' key is pressed, entramos en un bucle hasta pulsar 'c'
	if key == ord("p"):
                print "Pulsa c para continuar"
		while key != ord("c"):
                        key = cv2.waitKey(1) & 0xFF
                        

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break 

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
