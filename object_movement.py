# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from datetime import datetime

date_print = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
print date_print

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
#pts = deque(maxlen=args["buffer"])

# changed: no max length 
pts = deque()
time = deque()

counter = 0
#(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])


# Start time? 
start_time = datetime.now()
frame_zaehler = 0

# keep looping
while True:
	frame_zaehler = frame_zaehler + 1
	 
	# grab the current frame
	(grabbed, frame) = camera.read()
	#print camera.get(5)
   
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
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
			
			### TIME IN MILLISECONDS!
  			movie_ms = camera.get(0)
			time_pts = str(movie_ms) + ',' + str(center)[1:-1]
			pts.append(time_pts)

			
    # draw path 
	# loop over the set of tracked points
		for i in np.arange(1, len(pts)):
	# 	# if either of the tracked points are None, ignore
	# 	# them
			if pts[i - 1] is None or pts[i] is None:
				continue

			cv2.line(frame, (int(pts[i-1].split(',')[1]),int(pts[i-1].split(',')[2])), 
				(int(pts[i].split(',')[1]),int(pts[i].split(',')[2])), (0, 0, 0), 1)


			cv2.putText(frame, 'x: {0:.{2}f}, y: {1:.{2}f}'.format(x,y,1),
				(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_DUPLEX,
				.4, (0, 0, 0), 1)


		time_difference = datetime.now() - start_time
		time_difference = divmod(time_difference.total_seconds(), 60)[1]

		cv2.putText(frame, "Elapsed time: {0:.{2}f}, fps: {1:.{2}f}".format(time_difference,frame_zaehler/time_difference,1),
			(10, frame.shape[0] - 25), cv2.FONT_HERSHEY_DUPLEX,
			.4, (0, 0, 0), 1)	


	# draw progress bar 
 		ratio_movie_len = camera.get(2)
 		cv2.line(frame,(0,0),(int(frame.shape[1]*ratio_movie_len),0),(0,255,0),2,8)
		cv2.putText(frame, "{0:.{1}f}%".format(ratio_movie_len*100,1),
			(int(frame.shape[1]*ratio_movie_len)-30, 12), cv2.FONT_HERSHEY_SIMPLEX,
			.35, (0, 0, 0), 1)	


	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF
	counter += 1

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

# Save pts
with open("export/" + args.get("video") + "_" + date_print + ".csv","w") as saved_pts:
    for line in pts:
        #print line
        coord = line
        saved_pts.write("%s\n" %coord)
        

#close file again
saved_pts.close()