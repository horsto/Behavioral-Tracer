# USAGE
# give it multiple files separated by comma after the -v --video tag 


from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import random
from datetime import datetime
from scipy import misc
import math


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")

args = vars(ap.parse_args())

for video_no in xrange(len(args["video"].split(','))):
	date_print = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
	print date_print
	# changed: no max length 
	pts = deque()
	time = deque()

	counter = 0
	#(dX, dY) = (0, 0)

	# Start time? 
	start_time = datetime.now()


	# if a video path was not supplied, grab the reference
	# to the webcam
	if not args.get("video", False):
		camera = cv2.VideoCapture(0)
		 
		# grab the current frame
		(grabbed, frame) = camera.read()

		average_image = frame
		#frame_first = imutils.resize(frame_first, width=600)
		average_image = cv2.cvtColor(average_image,cv2.COLOR_BGR2GRAY)
		average_image = cv2.GaussianBlur(average_image, (13, 13), 0)

	# otherwise, grab a reference to the video file
	else:
		camera = cv2.VideoCapture(args["video"].split(',')[video_no])
		
		# extract background area from randomly sampled frames of the video
		frame_count = int(camera.get(7))
		print "Number of frames: " + str(frame_count)

		for i in range(100): # take 100 randomly sampled frames from the video
			random_frame = int(random.random()*frame_count)
			camera.set(1,random_frame)
			(grabbed, frame) = camera.read()

			if not grabbed: 
				break		
			frame = np.array(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),ndmin=3)
			if i == 0:
				average_image = frame
						
			else:
				average_image = np.concatenate((average_image, frame), axis=0)

			#print average_image.shape

		average_image = average_image.mean(axis=0)
		average_image  = np.array(average_image, np.uint8)
		average_image = cv2.medianBlur(average_image, 13)
		#cv2.imwrite("export/" + args["video"].split(',')[video_no] + ".png",average_image)
		

	# set frame back to beginning of video:
	camera.set(1,0)


	# define 
	def imclearborder(imgBW, radius):

	    # Given a black and white image, first find all of its contours
	    imgBWcopy = imgBW.copy()
	    contours = cv2.findContours(imgBWcopy.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

	    # Get dimensions of image
	    imgRows = imgBW.shape[0]
	    imgCols = imgBW.shape[1]    

	    contourList = [] # ID list of contours that touch the border

	    # For each contour...
	    for idx in np.arange(len(contours)):
	        # Get the i'th contour
	        cnt = contours[idx]

	        # Look at each point in the contour
	        for pt in cnt:
	            rowCnt = pt[0][1]
	            colCnt = pt[0][0]

	            check1 = (rowCnt >= 0 and rowCnt < radius) or (rowCnt >= imgRows-1-radius and rowCnt < imgRows)
	            check2 = (colCnt >= 0 and colCnt < radius) or (colCnt >= imgCols-1-radius and colCnt < imgCols)

	            if check1 or check2:
	                contourList.append(idx)
	                break

	    for idx in contourList:
	        cv2.drawContours(imgBWcopy, contours, idx, (0,0,0), -1)
	        #print 'deleted ROI'

	    return imgBWcopy

	frame_zaehler = 0
	# keep looping
	while True:
		frame_zaehler = frame_zaehler + 1
		 
		# grab the current frame
		(grabbed, frame) = camera.read()

		if args.get("video") and not grabbed:
			break

		if frame_zaehler == 1:
			frame_sicherung = frame.copy()


		frame_grey = frame
		frame_grey = cv2.cvtColor(frame_grey,cv2.COLOR_BGR2GRAY)
		frame_grey = cv2.medianBlur(frame_grey, 13)
		frame_grey = average_image - frame_grey 
		frame_grey[frame_grey < 50] = 255

		#frame_grey(frame_grey < 50) = 255
		threshold_lower = 165
		threshold_upper = 255
		ret1,mask = cv2.threshold(frame_grey,int(threshold_lower),int(threshold_upper),cv2.THRESH_BINARY)
		#ret, mask = cv2.threshold(frame_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		mask = 255-mask
		kernel = np.ones((3,3),np.uint8)
		mask = cv2.erode(mask,kernel,iterations=1)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

	 	Iclear = imclearborder(mask, 5)

		cnts = cv2.findContours(Iclear.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]

		center = None
		distance = []
		sorted_idx = 0

		#  proceed if at least one contour was found
		if len(cnts) > 0:
			# sort for distance to center
			if len(cnts) > 1:
				for idx in xrange(len(cnts)):
					((x, y), radius) = cv2.minEnclosingCircle(cnts[idx])
					# get distance euclidian
					calc_distance = math.sqrt((x-frame.shape[0]/2)**2+(y-frame.shape[1]/2)**2)
					distance.append(calc_distance)
				sorted_idx = distance.index(min(distance))


			M = cv2.moments(cnts[sorted_idx])
			((x, y), radius) = cv2.minEnclosingCircle(cnts[sorted_idx])

			# why? because M (moments) are much smoother ... 
			# and this double calculation doesn't slow down algorithm too much 
			try:
	  			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			except: 
				center = [int(x),int(y)]

			#  proceed if radius has minimum size
			if radius > 10:
				
				cv2.circle(frame, (center[0], center[1]), 4,
				 	(0, 255, 0), 2)

				# TIME IN MILLISECONDS!
	  			movie_ms = camera.get(0)
				time_pts = str(movie_ms) + ',' + str(center)[1:-1]
				pts.append(time_pts)

				
	   		cv2.putText(frame, 'x: {0:.{2}f}, y: {1:.{2}f}'.format(x,y,1),
				(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_PLAIN,
				1, (255, 255, 255), 1)


		time_difference = datetime.now() - start_time
		time_difference = divmod(time_difference.total_seconds(), 60)[0]*60 + divmod(time_difference.total_seconds(), 60)[1]

		cv2.putText(frame, "Elapsed time[s]: {0:.{2}f}, fps: {1:.{2}f}".format(time_difference,frame_zaehler/time_difference,1),
			(10, frame.shape[0] - 25), cv2.FONT_HERSHEY_PLAIN,
			1, (255, 255, 255), 1)	


		# draw progress bar 
	 	ratio_movie_len = camera.get(2)
	 	cv2.line(frame,(0,0),(int(frame.shape[1]*ratio_movie_len),0),(255,255,255),4,8)
		cv2.putText(frame, "{0:.{1}f}%".format(ratio_movie_len*100,1),
			(int(frame.shape[1]*ratio_movie_len)-47, 15), cv2.FONT_HERSHEY_PLAIN,
			1, (255, 255, 255), 1)	


		# show the frame to our screen and increment the frame counter
		cv2.imshow(args["video"].split(',')[video_no] + " Frame + Trace", frame)
		#cv2.imshow("Cleared Mask",Iclear)


		key = cv2.waitKey(1) & 0xFF
		counter += 1

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break


	# finished
	print "Elapsed time: " + str(time_difference) + "s, FPS at the end: " + str(frame_zaehler/time_difference)

	# Save screenshot
	# draw path 
	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
	# 	# if either of the tracked points are None, ignore
	# 	# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		cv2.line(frame_sicherung, (int(pts[i-1].split(',')[1]),int(pts[i-1].split(',')[2])), 
			(int(pts[i].split(',')[1]),int(pts[i].split(',')[2])), (0,255, 0), 1)

	# draw circle at start and end point 
	cv2.circle(frame_sicherung, (int(pts[i].split(',')[1]),int(pts[i].split(',')[2])), 3,
				 	(255, 0, 0), 2)
	cv2.circle(frame_sicherung, (int(pts[0].split(',')[1]),int(pts[0].split(',')[2])), 3,
				 	(255,255,255), 2)

	big = misc.imresize(frame_sicherung, 2.5)
	cv2.imwrite("export/" + args["video"].split(',')[video_no] + "_trace.png",big)



	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()

	# Save pts
	with open("export/" + args["video"].split(',')[video_no] + "_" + date_print + ".csv","a+") as saved_pts:
	    for line in pts:
	        #print line
	        coord = line
	        saved_pts.write("%s\n" %coord)
	        
	#close file again
	saved_pts.close()
	
	# delete variables
	del pts
	del time
	del saved_pts


