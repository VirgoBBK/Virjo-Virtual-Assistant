#!/usr/bin/env python

import RPi.GPIO as GPIO
import VirJoBot_PWM_Servo_Driver.Servo_init as pwm
import time  


Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

FILE_CONFIG = "/home/pi/VirJoBot/server/config"

EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]

p = pwm.init()

def setSpeed(speed):
	speed *= 40
	print 'speed is: ', speed
	p.setPWM(EN_M0, 0, speed)
	p.setPWM(EN_M1, 0, speed)

def setup():
	global forward0, forward1, backward1, backward0
	forward0 = 'True'
	forward1 = 'True'
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)     
	try:
		for line in open(FILE_CONFIG):
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
		GPIO.setup(pin, GPIO.OUT)   


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


def ctrl(status, direction=1):
	if status == 1:   # Run
		if direction == 1:     # Forward
			forward()
		elif direction == -1:  # Backward
			backward()
		else:
			print 'Argument error! direction must be 1 or -1.'
	elif status == 0: # Stop
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
