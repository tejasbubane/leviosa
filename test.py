# TrackColour.cpp : Defines the entry point for the console application.
#

#include "stdafx.h"
#include <stdio.h>
#include <opencv/cv.hpp>
import cv

#def GetThresholdedImage(img):
#	# Convert the image into an HSV image
#	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
#	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
#
#	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
#
#	# Values 20,100,100 to 30,255,255 working perfect for yellow at around 6pm
#	cv.InRangeS(imgHSV, cv.Scalar(112, 100, 100), cv.Scalar(124, 255, 255), imgThreshed)
#
#	cv.InRangeS(imgHSV, cv.Scalar(20, 130, 200), cv.Scalar(40, 200, 255), imgThreshed)
#	return imgThreshed

def GetRedThresholded(img):
	# Convert the image into an HSV image
	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
	# Ranges specified for RED colour filtering, keeping in mind the deviations.
	cv.InRangeS(imgHSV, cv.Scalar(15, 200, 180), cv.Scalar(35,255,245 ), imgThreshed)   #<<<-----------------set color value here
	return imgThreshed

def GetYellowThresholded(img):
	# Convert the image into an HSV image
	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
	# Ranges specified for YELLOW colour filtering, keeping in mind the deviations.
	cv.InRangeS(imgHSV, cv.Scalar(45, 130, 50), cv.Scalar(65, 230, 150), imgThreshed)	  #<<<-----------------set color value here
	return imgThreshed

def main():

	# Initialize capturing live feed from the camera
	capture = 0
	capture = cv.CaptureFromCAM(0)

	# Couldn't get a device? Throw an error and quit
	if (not capture):
		print "Could not initialize capturing...\n"
		return -1

	# The two windows we'll be using
	cv.NamedWindow("video")
	cv.NamedWindow("thresh")

	# This image holds the "scribble" data...
	# the tracked positions of the ball
	imgScribble = 0

	# a flag which indicates a valid mouse click
	clicked = 0

	# to hold the previous co-ordinate values.
	prevXred=0
	prevYred=0
	prevXyellow=0
	prevYyellow=0
	
	#initialising fake motioning
	import ctypes
	c=ctypes.CDLL("libhelper.so.1")
	libc=ctypes.CDLL("libc.so.6")
	c.helper_init()

	Xred=-1
	Yred=-1
	Xyellow=-1
	Yyellow=-1
	# An infinite loop
	while(True):
		#----------------------------------------------------------------------------------------

		# Will hold a frame captured from the camera
		frame = 0
		frame = cv.QueryFrame(capture)

		# If we couldn't grab a frame... quit
		if(not frame):
			break
		
		# If this is the first frame, we need to initialize it
		if(imgScribble == 0):
			imgScribble = cv.CreateImage(cv.GetSize(frame), 8, 3)

		# representative co-ordinates of RED & YELLOW finger-tips, initialized.
		dx=0
		dy=0

		#----------------------------------------------------------------------------------------

		# Holds the RED thresholded image (red = white, rest = black)
		imgRedThresh = GetRedThresholded(frame)
		moments=0
		# Calculate the moments to estimate the position of RED finger-tip
		moments=cv.Moments(imgRedThresh)

		# The actual moment values
		moment01 = cv.GetSpatialMoment(moments, 0, 1)
		moment10 = cv.GetSpatialMoment(moments, 1, 0)
		area = cv.GetSpatialMoment(moments, 0, 0)
		
		if(area==0): 
			continue
		
		prevXred = Xred
		prevYred = Yred
		if area:
			Xred = moment10/area
			Yred = moment01/area

		# Print it out for debugging purposes
		#print "position "+ str(Xred)+' '+ str(Yred)+'\n'

		#----------------------------------------------------------------------------------------

		# Holds the YELLOW thresholded image (yellow = white, rest = black)
		imgYellowThresh = GetYellowThresholded(frame)
		moments=0
		# Calculate the moments to estimate the position of YELLOW finger-tip
		moments=cv.Moments(imgYellowThresh)

		# The actual moment values
		moment01 = cv.GetSpatialMoment(moments, 0, 1)
		moment10 = cv.GetSpatialMoment(moments, 1, 0)
		area = cv.GetSpatialMoment(moments, 0, 0)
		
		if(area==0): continue
		
		prevXyellow = Xyellow
		prevYyellow = Yyellow
		Xyellow = moment10/area
		Yyellow = moment01/area
		
		#dx = (Xyellow - prevXyellow) 
		#dy = (Yyellow - prevYyellow)
		
		#x=1390-Xyellow*2.125
		#y=Yyellow*1.575
		
		Xt = 1390-(abs(Xred + Xyellow)*1.125)
		Yt = (abs(Yred + Yyellow)*0.7875)
		
		libc.usleep(150)
		c.helper_mov_absxy(int(Xt),int(Yt))
		#c.helper_mov_relxy(int(dx),int(dy))
		# Print it out for debugging purposes
		#print "position "+ str(Xyellow)+' '+ str(Yyellow)
		
		#----------------------------------------------------------------------------------------

		# find distance between RED & YELLOW finger-tips
		# for faster calculation, individually Xdiff, Ydiff
		# considered, instead of sqrt((x2-x1)^2 + (y2-y2)^2)

		Xdiff = abs( Xred - Xyellow )
		Ydiff = abs( Yred - Yyellow )
		
		# determine the 'clicked' state, using approximation to circle method.
		d=50
		#if((21*Xdiff + 50*Ydiff <= 50*d) and (50*Xdiff + 21*Ydiff <= 50*d)):
		if(Xdiff * Xdiff + Ydiff * Ydiff < d*d):
		#if(Xdiff < 25 and Ydiff < 25):
			if(not clicked):
				clicked = 1
				print "clicked"

		else:
			if(clicked):
				clicked = 0
				
		if clicked:
			c.helper_press()
			c.helper_release()
			
		# convey prevXred,prevYred,Xred,Yred,clicked for generation of appropriate mouse event.	
				
		#libc.sleep(2)
		#c.helper_mov_relxy()
		
		#c.helper_mov_relxy()
		#libc.sleep(2)
		#if clicked
		#c.helper_press()
		#c.helper_release()
		#----------------------------------------------------------------------------------------

#		# We want to draw a line only if its a valid position
#		if(lastX>0 and lastY>0 and posX>0 and posY>0):
#		
#			# Draw a yellow line from the previous point to the current point
#			cv.Line(imgScribble, cv.Point(posX, posY), cv.Point(lastX, lastY), cv.Scalar(0,255,255), 5)
#		
#
#		# Add the scribbling image and the frame... and we get a combination of the two
#		cv.Add(frame, imgScribble, frame)
		#cv.ShowImage("thresh", imgYellowThresh)
		#cv.ShowImage("video", frame)

		#----------------------------------------------------------------------------------------
		
		# Wait for a keypress
		cin = cv.WaitKey(10)
		if not (cin == -1):		
			# If pressed, break out of the loop
			break
		
		# Release the thresholded image... we need no memory leaks.. please
		
		#----------------------------------------------------------------------------------------

	# We're done using the camera. Other applications can now use it
	return 0
main()
