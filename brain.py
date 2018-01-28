#!/usr/bin/python
# -*- coding:utf8 -*

from GreyMatter import general_conversations, tell_time, weather, define_subject
from chatbot import chat 

def brain(name, speech_text, city_name, city_code):
	
	def check_message(check):
		"""
		This function checks if the items in the list (specified in
		argument) are present in the user's input speech.
		"""

		words_of_message = speech_text.split()
		if set(check).issubset(set(words_of_message)):
			return True
		else:
			return False


	if check_message(['how', 'weather']) or check_message(['hows', 'weather']):
		weather.weather(city_name, city_code)

	elif check_message(['define']):
		define_subject.define_subject(speech_text)

	else:
		chat.speech_engine(speech_text)