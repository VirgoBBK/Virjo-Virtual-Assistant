#!/usr/bin/python
# -*- coding:utf8 -*

from datetime import datetime
from SenseCells.tts import tts_online, tts_offline

def what_is_time():
	tts("The time is " + datetime.strftime(datetime.now(), '%H:%M:%S'))