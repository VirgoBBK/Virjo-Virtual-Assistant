#!/usr/bin/env python
# -*- coding:utf8 -*

import gobject
import sys
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

#Module to handle keyboard interrupt signal
import signal


#Keyboard signal handling routine
def signal_handle(signal, frame):
	print ("You pressed Ctrl+C")
	sys.exit(0)


#Implementation of Speech recognition class
class Speech_Recog(object):
	#Initializing gstreamer pipeline and pocket sphinx element
	def __init__(self):
		self.init_gst()

	#This function will initialize gstreamer pipeline
	def init_gst(self):
	
		#The following code create a gstreamer pipeline with pipeline description. The required descriptors needed for the code is given as parameters.
		self.pipeline = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
		+ '! vader name=vad auto-threshold=true '
		+ '! pocketsphinx name=asr ! fakesink')



		#Accessing pocket sphinx element from gstreamer pipeline
		asr = self.pipeline.get_by_name('asr')

		#Connecting to asr_result function when a speech to text conversion is completed
		asr.connect('result', self.asr_result)
		#User can mention lm and dict for accurate detection
		#asr.set_property('lm', '/home/user/mylanguagemodel.lm')
		#asr.set_property('dict','/home/user/mylanguagemodel.dic')
		
		#This option will set all options are configured well and can start recognition
		asr.set_property('configured', True)
		#Pausing the GStreamer pipeline at first.
		self.pipeline.set_state(gst.STATE_PAUSED)
		

		#Definition of asr_result
	def asr_result(self, asr, text, uttid):
		#Printing the detected text
		print ("Detected Text=>",text)
	

	#This function will start/stop Speech recognition operation
	def start_recognition(self):
		#VADER - Voice Activity DEtectoR, which helps when the speech start and when its ends. Creating VADER object and set the property silent to False, so no speech will detected until key press
		
		vader = self.pipeline.get_by_name('vad')
		vader.set_property('silent', False)
		
		#Waiting for a key press to start recognition
		raw_input("Press any key to start recognition:>")
		
		#Start playing the pipeline
		self.pipeline.set_state(gst.STATE_PLAYING)
		
		#Waiting for stopping the recognition
		raw_input("Press any key to stop recognition:>")
		vader = self.pipeline.get_by_name('vad')
		
		#Setting silent property of VADER to True
		vader.set_property('silent', True)
		
		#Pausing GStreamer pipeline
		self.pipeline.set_state(gst.STATE_PAUSED)

if __name__ == "__main__":
	#Creating an object of Speech_Recog() class
	app_object = Speech_Recog()

	#Assign keyboard interrupt handler 
	signal.signal(signal.SIGINT, signal_handle)

	while True:
		#Calling Speech recognition routine
		app_object.start_recognition()


