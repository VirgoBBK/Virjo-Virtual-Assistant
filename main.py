import sys
import yaml
import speech_recognition as sr
from GreyMatter.SenseCells.tts import tts
from brain import brain

profile = open('profile.yaml')
profile_data = yaml.safe_load(profile)
profile.close()

# Functioning Variables
name = profile_data['name']
city_name = profile_data['city_name']
city_code = profile_data['city_code']

tts('Welcome ' + name + ', systems are now ready to run. How can I help you?')


def main():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)

	try:
		speech_text = r.recognize_google(audio).lower().replace("'", "")
		print("Melissa thinks you said '" + speech_text + "'")

		brain(name, speech_text, city_name, city_code)

	except sr.UnknownValueError:
		print("Melissa could not understand audio")
		
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	
	

main()