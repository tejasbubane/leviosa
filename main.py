#    			main file to be run for executing the program (main.py)

#							Copyright (C) 2012
 
#	Miheer Mukund Vaidya
#	Jaydev Kshirsagar
#	Akash Agrawal
#	Tejas Bubane

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cv
import tejas

def GetThreshold1(img, color1):
	# Convert the image into an HSV image
	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
	# Ranges specified for colour1 filtering, keeping in mind the deviations.
	cv.InRangeS(imgHSV, cv.Scalar(color1[0][0], color1[0][1], color1[0][2]), cv.Scalar(color1[1][0], color1[1][1], color1[1][2]), imgThreshed)
		#<<<-----------------set color value here
	return imgThreshed

def GetThreshold2(img, color2):
	# Convert the image into an HSV image
	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
	# Ranges specified for YELLOW colour filtering, keeping in mind the deviations.
	cv.InRangeS(imgHSV, cv.Scalar(color2[0][0], color2[0][1], color2[0][2]), cv.Scalar(color2[1][0], color2[1][1], color2[1][2]), imgThreshed)
		#<<<-----------------set color value here
	return imgThreshed

def GetThreshold3(img, color3):
	# Convert the image into an HSV image
	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
	# Ranges specified for RED colour filtering, keeping in mind the deviations.
	cv.InRangeS(imgHSV, cv.Scalar(color3[0][0], color3[0][1], color3[0][2]), cv.Scalar(color3[1][0], color3[1][1], color3[1][2]), imgThreshed)
		#<<<-----------------set color value here
	return imgThreshed

def main():
	L = tejas.leviosa()
	tejas.gtk.main()
	
	# Get color1 ranges from tejas.py
	color1 = tejas.result[0]
	print "Received values: "+str(tejas.result[0])
	color2 = tejas.result[1]
	print "Received values: "+str(tejas.result[1])
	color3 = tejas.result[2]
	print "Received values: "+str(tejas.result[2])
	
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
	imgScribble = 0

	# a flag which indicates a valid mouse click
	clicked = 0
	clicked1 = 0

	# to held previous co-ordinate values.
	prevXred=0
	prevYred=0
	prevXyellow=0
	prevYyellow=0
	prevXblue=0
	prevYblue=0
	
	#initialising fake motioning
	import ctypes
	c=ctypes.CDLL("libhelper.so.1")
	libc=ctypes.CDLL("libc.so.6")
	c.helper_init()
	
	#to held current co-ordinate values
	Xred=-1
	Yred=-1
	Xyellow=-1
	Yyellow=-1
	Xblue=-1
	Yblue=-1
	
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
		dz=0

		#----------------------------------------------------------------------------------------

		# Holds the thresholded image for color1(color1 = white, rest = black)
		imgThresh1 = GetThreshold1(frame, color1)
		moments=0
		# Calculate the moments to estimate the position of RED finger-tip
		moments=cv.Moments(imgThresh1)

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

		# Holds the color2 thresholded image (color2 = white, rest = black)
		imgThresh2 = GetThreshold2(frame, color2)
		moments=0
		# Calculate the moments to estimate the position of RED finger-tip
		moments=cv.Moments(imgThresh2)

		# The actual moment values
		moment01 = cv.GetSpatialMoment(moments, 0, 1)
		moment10 = cv.GetSpatialMoment(moments, 1, 0)
		area = cv.GetSpatialMoment(moments, 0, 0)
		
		if(area==0): 
			continue
		
		prevXblue = Xblue
		prevYblue = Yblue
		if area:
			Xblue = moment10/area
			Yblue = moment01/area

		# Holds the YELLOW thresholded image (yellow = white, rest = black)
		imgThresh3 = GetThreshold3(frame, color3)
		moments=0
		# Calculate the moments to estimate the position of YELLOW finger-tip
		moments=cv.Moments(imgThresh3)

		# The actual moment values
		moment01 = cv.GetSpatialMoment(moments, 0, 1)
		moment10 = cv.GetSpatialMoment(moments, 1, 0)
		area = cv.GetSpatialMoment(moments, 0, 0)
		
		if(area==0): continue
		
		prevXyellow = Xyellow
		prevYyellow = Yyellow
		Xyellow = moment10/area
		Yyellow = moment01/area
		
		Xt = 1390-(abs(Xred + Xyellow)*1.125)
		Yt = (abs(Yred + Yyellow)*0.787)
		
		libc.usleep(150)
		c.helper_mov_absxy(int(Xt),int(Yt))
		#c.helper_mov_relxy(int(dx),int(dy))

		Xdiff = abs( Xred - Xyellow )
		Ydiff = abs( Yred - Yyellow )
		
		Xdiff1 = abs( Xred - Xblue)
		Ydiff1 = abs( Yred - Yblue)
		
		# determine the 'clicked' state, using approximation to circle method.
		d=50
		if(Xdiff * Xdiff + Ydiff * Ydiff < d*d):
			if(not clicked):
				clicked = 1
				print "left clicked"

		else:
			if(clicked):
				clicked = 0
				c.helper_release(1)
				
		if clicked:
			c.helper_press(1)
		
		d=45	
		#if((21*Xdiff + 50*Ydiff <= 50*d) and (50*Xdiff + 21*Ydiff <= 50*d)):
		if(Xdiff1 * Xdiff1 + Ydiff1 * Ydiff1 < d*d):
		#if(Xdiff < 25 and Ydiff < 25):
			if(not clicked1):
				clicked1 = 1
				print "right clicked"

		else:
			if(clicked1):
				clicked1 = 0
				
		if clicked1:
			c.helper_press(3)
			c.helper_release(3)
	
		# Wait for a keypress
		cin = cv.WaitKey(10)
		if not (cin == -1):		
			# If pressed, break out of the loop
			break
		
		# Release the thresholded image... we need no memory leaks.. please
		
		#----------------------------------------------------------------------------------------

	# We're done using the camera. Other applications can now use it
	return 0

if __name__ == '__main__':
	main()
