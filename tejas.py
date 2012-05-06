#    			GUI for Leviosa
#	This is the GUI for Leviosa project that can select custom colors
#  Copyright (C) 2012  
#  Tejas Pramod Bubane (tejasbubane@gmail.com)
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

#import pygtk
#pygtk.require('2.0')
import gtk
import cv

result = []

class leviosa:
	def default(self, widget, data): #send default values
		result.append([[15, 200, 180], [35, 255, 245]])
		result.append([[45, 130, 50], [65, 230, 150]])
		result.append([[155, 165, 180], [175, 235, 255]])
	
	def custom(self, widget, data): # get custom values from color-selection widget and send them
		
		# Initialize capturing live feed from the camera
		capture = 0
		capture = cv.CaptureFromCAM(0)

		# Couldn't get a device? Throw an error and quit
		if (not capture):
			print "Could not initialize capturing...\n"
			return -1
			
		cv.NamedWindow("video")
		
		for i in range(20):
			# Will hold a frame captured from the camera
			frame = 0
			frame = cv.QueryFrame(capture)
			cv.ShowImage("video", frame)
		
		for i in range(3):	#loop to get three custom values
			cdlg = gtk.ColorSelectionDialog("Select Color")
			response = cdlg.run()
			if response == gtk.RESPONSE_OK:
				colorsel = cdlg.colorsel
				color = colorsel.get_current_color()
			cdlg.destroy()
			l1 = int(color.hue * 180) - 10
			if l1 < 0: l1 = 0
			l2 = int(color.saturation * 255) - 40
			if l2 < 0: l2 = 0
			u1 = int(color.hue * 180) + 10
			if u1 > 180: u1 = 180
			u2 = int(color.saturation * 255) + 40
			if u2 > 255: u2 = 255
			result.append([[l1, l2, 100], [u1, u2, 255]])
		return result
		
	def delete_event(self, widget, event, data=None): #exit safely from gtk
		gtk.main_quit()
		return False
	
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_title("Leviosa")
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(100)
		self.box1 = gtk.HBox(False, 0)
		self.window.add(self.box1)
		self.button1 = gtk.Button("Default Colors")
		self.button1.connect("clicked", self.default, None)
		self.box1.pack_start(self.button1, True, True, 0)
		self.button1.show()
		self.button2 = gtk.Button("Custom Colors")
		self.button2.connect("clicked", self.custom, None)
		self.box1.pack_start(self.button2, True, True, 0)
		self.button2.show()

		self.box1.show()
		self.window.show()

def main():
	gtk.main()

#if __name__ == '__main__':
#	L = leviosa()
#	main()
