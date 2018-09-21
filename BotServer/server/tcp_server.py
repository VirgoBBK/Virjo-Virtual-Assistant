#!/usr/bin/env python
# -*- coding:utf-8 -*

import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
from socket import *
from time import ctime 
from threading import Thread 


ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # numéro de bus de la raspberry

HOST = ''     
PORT = 21567
BUFSIZ = 1024   
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM) 
tcpSerSock.bind(ADDR)   
tcpSerSock.listen(5)     
                         
video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialisation du GPIO connecté au DC motor. 
video_dir.home_x_y()
car_dir.home()

class VirjoBotMotor(Thread):
	"""docstring for VirjoBotMotor"""

	def __init__(self):
		super(VirjoBotMotor, self).__init__()

	def run(self):

		while True:
			print 'Waiting for connection...'

			tcpCliSock, addr = tcpSerSock.accept() 
			print '...connected from :', addr     

			while True:
				data = ''
				data = tcpCliSock.recv(BUFSIZ)   
				if not data:
					break
				if data == ctrl_cmd[0]:
					print 'motor moving forward'
					motor.forward()
				elif data == ctrl_cmd[1]:
					print 'recv backward cmd'
					motor.backward()
				elif data == ctrl_cmd[2]:
					print 'recv left cmd'
					car_dir.turn_left()
				elif data == ctrl_cmd[3]:
					print 'recv right cmd'
					car_dir.turn_right()
				elif data == ctrl_cmd[6]:
					print 'recv home cmd'
					car_dir.home()
				elif data == ctrl_cmd[4]:
					print 'recv stop cmd'
					motor.ctrl(0)
				elif data == ctrl_cmd[5]:
					print 'read cpu temp...'
					temp = cpu_temp.read()
					tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
				elif data == ctrl_cmd[8]:
					print 'recv x+ cmd'
					video_dir.move_increase_x()
				elif data == ctrl_cmd[9]:
					print 'recv x- cmd'
					video_dir.move_decrease_x()
				elif data == ctrl_cmd[10]:
					print 'recv y+ cmd'
					video_dir.move_increase_y()
				elif data == ctrl_cmd[11]:
					print 'recv y- cmd'
					video_dir.move_decrease_y()
				elif data == ctrl_cmd[12]:
					print 'home_x_y'
					video_dir.home_x_y()
				elif data[0:5] == 'speed':     
					print data
					numLen = len(data) - len('speed')
					if numLen == 1 or numLen == 2 or numLen == 3:
						tmp = data[-numLen:]
						print 'tmp(str) = %s' % tmp
						spd = int(tmp)
						print 'spd(int) = %d' % spd
						if spd < 24:
							spd = 24
						motor.setSpeed(spd)
				elif data[0:5] == 'turn=':	
					print 'data =', data
					angle = data.split('=')[1]
					try:
						angle = int(angle)
						car_dir.turn(angle)
					except:
						print 'Error: angle =', angle
				elif data[0:8] == 'forward=':
					print 'data =', data
					spd = data[8:]
					try:
						spd = int(spd)
						motor.forward(spd)
					except:
						print 'Error speed =', spd
		                elif data[0:9] == 'backward=':
		                        print 'data =', data
		                        spd = data.split('=')[1]
					try:
						spd = int(spd)
			                        motor.backward(spd)
					except:
						print 'ERROR, speed =', spd

				else:
					print 'Command Error! Cannot recognize command: ' + data

		tcpSerSock.close()



