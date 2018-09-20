#!/usr/bin/env python
# -*- coding:utf-8 -*

import PCA9685 as servo
import time 

def Map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup(busnum=None):
	global leftPWM, rightPWM, homePWM, pwm
	leftPWM = 400
	homePWM = 450
	rightPWM = 500
	offset =0
	try:
		for line in open('config'):
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
	except:
		print 'config error'
	leftPWM += offset
	homePWM += offset
	rightPWM += offset
	if busnum == None:
		pwm = servo.PWM()                  # Initialisation du servo contrôleur
	else:
		pwm = servo.PWM(bus_number=busnum)  # Initialisation du servo contrôleur
	pwm.frequency = 60

# ==========================================================================================
# Controler le servo connecté au channel 0 du servo control board, pour faire tourner VirJo à gauche
# ==========================================================================================
def turn_left():
	global leftPWM
	pwm.write(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Faire tourner VirJo à droite
# ==========================================================================================
def turn_right():
	global rightPWM
	pwm.write(0, 0, rightPWM)

# ==========================================================================================
# Faire tourner VirJo
# ==========================================================================================

def turn(angle):
	angle = Map(angle, 0, 255, leftPWM, rightPWM)
	pwm.write(0, 0, angle)

def home():
	global homePWM
	pwm.write(0, 0, homePWM)

def calibrate(x):
	pwm.write(0, 0, 450+x)

def test():
	while True:
		turn_left()
		time.sleep(1)
		home()
		time.sleep(1)
		turn_right()
		time.sleep(1)
		home()

if __name__ == '__main__':
	setup()
	home()


