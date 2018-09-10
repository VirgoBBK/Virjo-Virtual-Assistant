#!/usr/bin/python
# -*- coding:utf8 -*

import pywapi
from SenseCells.tts import tts

def weather(city_name, city_code):
	city = unicode(raw_input("City name > S"))
	 
	#this will give you a dictionary of all cities in the world with this city's name Be specific (city, country)!
	lookup = pywapi.get_location_ids(city)
	city_code = list(lookup.keys())[0]

	weather_com_result = pywapi.get_weather_from_weather_com(city_code)
	print weather_com_result

	# weather_result = "Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "degree celcius now in " + city_name

	# tts(weather_result)