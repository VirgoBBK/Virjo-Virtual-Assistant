#!/usr/bin/python
# -*-coding:utf-8 -*

import aiml
import sys
from espeak import espeak as spk
import os 
from GreyMatter.SenseCells import tts

# Change the current path to the desired
os.chdir('./chatbot/aiml')
mybot = aiml.Kernel()
mybot.setBotPredicate("name", "VIRJO")
mybot.setBotPredicate("location", "Lubumbashi")
mybot.setBotPredicate("nationality", "congolese")
mybot.setBotPredicate("botmaster", "Virgo and Jobabou")
mybot.setBotPredicate("birthdate", "Wednesday September 19 2018")

# # If there is a brain file named standard.brn, Kernel() will initialize using boostrap() method
# if os.path.isfile("standard.brn"):
# 	mybot.bootstrap(brainFile = "standard.brn")
# else:

	# If there is not brain file, load all AIML files and save a new brain file
#mybot.bootstrap(learnFiles = "startup.xml", commands = "load aiml b")
mybot.bootstrap(learnFiles = "startup.xml", commands = "load aiml b")
mybot.saveBrain("standard.brn")

# mybot.learn('startup.xml')

# # Calling load aiml b for loading all AIML files
# mybot.respond('load aiml b')

# # Saving loaded patterns into a brain file
# #mybot.saveBrain('standard.brn')

def speech_engine(input):

	response = mybot.respond(input)
	# if response == '':
	# 	response = "I don't understant what you say !"
	print response
	tts.tts_online(response)
	# response = 'espeak "{}"'.format(response)
	# os.system(response)

	