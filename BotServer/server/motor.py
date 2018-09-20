#!/usr/bin/env python
# -*- coding:utf-8 -*

import RPi.GPIO as GPIO
import PCA9685 as p
import time

# ===========================================================================
# Les pins de la Raspberry:  pin11, 12, 13 and 15 pour réalizer des rotations horlogiques/anti-horlogiques, des mouvements vers l'avant et l'arrière.
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Configurer channel 4 and 5 du servo driver IC pour générer PWM, pour le contrôle de la vitesse
# ===========================================================================
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]


def setSpeed(speed):
	speed *= 40
	print 'speed is: ', speed
	pwm.write(EN_M0, 0, speed)
	pwm.write(EN_M1, 0, speed)

def setup(busnum=None):
	global forward0, forward1, backward1, backward0
	global pwm
	if busnum == None:
		pwm = p.PWM()                  # Initialisation du servo contrôleur
	else:
		pwm = p.PWM(bus_number=busnum) # Initialisation du servo contrôleur.

	pwm.frequency = 60
	forward0 = 'True'
	forward1 = 'True'
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)        # Numéro GPIO de part sa position physique
	try:
		for line in open("config"):
			if line[0:8] == "forward0":
				forward0 = line[11:-1]
			if line[0:8] == "forward1":
				forward1 = line[11:-1]
	except:
		pass
	if forward0 == 'True':
		backward0 = 'False'
	elif forward0 == 'False':
		backward0 = 'True'
	if forward1 == 'True':
		backward1 = 'False'
	elif forward1 == 'False':
		backward1 = 'True'
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Définir tous les pins en mode output

# ===========================================================================
# Controler le DC motor pour le faire tourner en sens horlogique pour faire avancer VirJo
# ===========================================================================

def motor0(x):
	if x == 'True':
		GPIO.output(Motor0_A, GPIO.LOW)
		GPIO.output(Motor0_B, GPIO.HIGH)
	elif x == 'False':
		GPIO.output(Motor0_A, GPIO.HIGH)
		GPIO.output(Motor0_B, GPIO.LOW)
	else:
		print 'Config Error'

def motor1(x):
	if x == 'True':
		GPIO.output(Motor1_A, GPIO.LOW)
		GPIO.output(Motor1_B, GPIO.HIGH)
	elif x == 'False':
		GPIO.output(Motor1_A, GPIO.HIGH)
		GPIO.output(Motor1_B, GPIO.LOW)

def forward():
	motor0(forward0)
	motor1(forward1)

def backward():
	motor0(backward0)
	motor1(backward1)

def forwardWithSpeed(spd = 50):
	setSpeed(spd)
	motor0(forward0)
	motor1(forward1)

def backwardWithSpeed(spd = 50):
	setSpeed(spd)
	motor0(backward0)
	motor1(backward1)

def stop():
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)

# ===========================================================================
# Le premier parameter(status) permet de contrôler l'état de VirJo, pour le faire rouler ou l'arrêter. Le parametre (direction) permet de contrôler la direction
# ===========================================================================
def ctrl(status, direction=1):
	if status == 1:   # Run
		if direction == 1:     # Avancer
			forward()
		elif direction == -1:  # Réculer
			backward()
		else:
			print 'Argument error! direction must be 1 or -1.'
	elif status == 0: # S'arrêter
		stop()
	else:
		print 'Argument error! status must be 0 or 1.'

def test():
	while True:
		setup()
		ctrl(1)
		time.sleep(3)
		setSpeed(10)
		time.sleep(3)
		setSpeed(100)
		time.sleep(3)
		ctrl(0)

if __name__ == '__main__':
	setup()
	setSpeed(50)
	stop()
