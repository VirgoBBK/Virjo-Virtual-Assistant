#!/usr/bin/python
# -*- coding:utf8 -*

import os
from gtts import gTTS
from espeak import espeak

def tts_offline(message):
	espeak.synth(message.encode('utf-8'))

def tts_online(message):
	try:
	    tts = gTTS(text=message, lang='en')
	    tts.save("audio.mp3")
	    os.system("mpg321 audio.mp3")

	except Exception as e:
		tts_offline(message)
