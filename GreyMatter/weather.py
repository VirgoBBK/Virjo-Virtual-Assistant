#!/usr/bin/python
# -*- coding:utf8 -*

import pywapi
from SenseCells.tts import tts_online, tts_offline
import requests

def weather(city_name, city_code):
	 
	#city_code = unicode(city_code)
	#city_name = unicode(city_name)

	try:
		#weather_com_result = pywapi.get_weather_from_weather_com(city_code)
		weather_com_result = pywapi.get_weather_from_yahoo(city_code)

	except Exception as e:
		print("Exception : ", e)

	if not weather_com_result.__contains__('error'):
		weather_result = "Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "degree celcius now in " + city_name

		tts(weather_result)

	else:
		tts_offline('It seems that there is a connecting problem, please check your internet connection')		
		print("It seems that there is a connecting problem, please check your internet connection")
