#!/usr/bin/python
# -*- coding:utf8 -*

import pywapi
from SenseCells.tts import tts
import requests

def weather(city_name, city_code):
	 
	# #this will give you a dictionary of all cities in the world with this city's name Be specific (city, country)!
	# lookup = pywapi.get_location_ids(city_name)
	# city_code = list(lookup.keys())[0]
	city_code = unicode(city_code)
	city_name = unicode(city_name)

	weather_com_result = pywapi.get_weather_from_weather_com(city_code)

	if not weather_com_result.__contains__('error'):
		weather_result = "Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "degree celcius now in " + city_name

		tts(weather_result)

	else:
		tts('It seems that there is a connecting problem, please check your internet connection')		
		print("It seems that there is a connecting problem, please check your internet connection")
