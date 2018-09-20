# Initial configuration
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print "Measuring Distance"
print "Press ctrl+c to stop me"

# Setting the GPIO pins on the default mode
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
time.sleep(0.02)
GPIO.output(23, False)
print "Setting Trigger pin to zero by default"
time.sleep(1)

while True:
	# Sending and receiving the pulses
	GPIO.output(23, True)
	time.sleep(0.00001)
	GPIO.output(23, False)

	while GPIO.input(24) == 0:
		start_time = time.time()

	while GPIO.input(24) == 1:
		end_time = time.time()

	# Distance calculation
	time_diff = end_time - start_time
	distance = 17150 * time_diff
	print "Measured Distance is : ", distance, " cm"
	if distance < 100 :
		print "obstacle detected"
		os.system('mpg321 alarm.mp3 &')
GPIO.cleanup()
