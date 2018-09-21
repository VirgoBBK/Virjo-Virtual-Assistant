#!/usr/bin/env python
# -*- coding:utf-8 -*

import PCA9685 as servo
import time

MinPulse = 200
MaxPulse = 700

Current_x = 0
Current_y = 0

def setup(busnum=None):
	global Xmin, Ymin, Xmax, Ymax, home_x, home_y, pwm
	offset_x = 0
	offset_y = 0
	try:
		for line in open('config'):
			if line[0:8] == 'offset_x':
				offset_x = int(line[11:-1])
				#print 'offset_x =', offset_x
			if line[0:8] == 'offset_y':
				offset_y = int(line[11:-1])
				#print 'offset_y =', offset_y
	except:
		pass
	Xmin = MinPulse + offset_x
	Xmax = MaxPulse + offset_x
	Ymin = MinPulse + offset_y
	Ymax = MaxPulse + offset_y
	home_x = (Xmax + Xmin)/2
	home_y = Ymin + 80
	if busnum == None:
		pwm = servo.PWM()                  
	else:
		pwm = servo.PWM(bus_number=busnum) 
	pwm.frequency = 60

# ==========================================================================================
# Controler le servo connecté au channel 14 pour faire pivoter la caméra dans le sens positif des abscisses
# ==========================================================================================
def move_decrease_x():
	global Current_x
	Current_x += 25
	if Current_x > Xmax:
		Current_x = Xmax
        pwm.write(14, 0, Current_x)   # CH14 <---> X axis
# ==========================================================================================
# Controler le servo connecté au channel 14 pour faire pivoter la caméra dans le sens négatif des abscisses
# ==========================================================================================
def move_increase_x():
	global Current_x
	Current_x -= 25
	if Current_x <= Xmin:
		Current_x = Xmin
        pwm.write(14, 0, Current_x)
# ==========================================================================================
# Controler le servo connecté au channel 15 pour faire pivoter la caméra dans le sens positif des ordonnées
# ==========================================================================================
def move_increase_y():
	global Current_y
	Current_y += 25
	if Current_y > Ymax:
		Current_y = Ymax
        pwm.write(15, 0, Current_y)   # CH15 <---> Y axis
# ==========================================================================================
# Controler le servo connecté au channel 15 pour faire pivoter la caméra dans le sens négatif des ordonnées
# ==========================================================================================		
def move_decrease_y():
	global Current_y
	Current_y -= 25
	if Current_y <= Ymin:
		Current_y = Ymin
        pwm.write(15, 0, Current_y)
# ==========================================================================================		
# Controler les servos connectés aux  channels 14 et 15 au même moment pour faire avancer la caméra
# ==========================================================================================
def home_x_y():
	global Current_y
	global Current_x
	Current_y = home_y 
	Current_x = home_x
	pwm.write(14, 0, Current_x)
	pwm.write(15, 0, Current_y)

def calibrate(x,y):
	pwm.write(14, 0, (MaxPulse+MinPulse)/2+x)
	pwm.write(15, 0, (MaxPulse+MinPulse)/2+y)

def test():
	while True:
		home_x_y()
		time.sleep(0.5)
		for i in range(0, 9):
			move_increase_x()
			move_increase_y()
			time.sleep(0.5)
		for i in range(0, 9):
			move_decrease_x()
			move_decrease_y()
			time.sleep(0.5)

if __name__ == '__main__':
	setup()
	home_x_y()
