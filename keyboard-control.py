import RPi.GPIO as GPIO
import keyboard
from time import sleep
import time



# Copyright 2023 The MediaPipe Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain pwdt vision
import sys
import time

COUNTER, FPS = 0, 0
START_TIME = time.time()
freq = 500


ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

forward_left_motor = GPIO.PWM(13, freq)	#create PWM instance with frequency
backward_left_motor = GPIO.PWM(12,freq)
forward_left_motor.start(0)				#start PWM of required Duty Cycle 
backward_left_motor.start(0)				#start PWM of required Duty Cycle 

backward_right_motor = GPIO.PWM(18, freq)
forward_right_motor = GPIO.PWM(19,freq)
backward_right_motor.start(0)
forward_right_motor.start(0)

pwm_back_left = 0
pwm_back_right = 0
pwm_forward_left = 0
pwm_forward_right = 0
max_speed = 50
l_state = "off"
r_state = "off"
prevTimeL = time.time()
prevTimeR = time.time()


def motorDirection(category_name: str = 'none'):
	global pwm_back_left, pwm_back_right, pwm_forward_left, pwm_forward_right, max_speed, forward_left_motor, backward_right_motor,forward_right_motor, backward_left_motor
 
	if category_name == "forward":
		pwm_forward_left = min(pwm_forward_left + 5, max_speed)
		pwm_back_left = 0
		pwm_forward_right = min(pwm_forward_right + 5, max_speed)
		pwm_back_right = 0
		if(pwm_forward_left != pwm_forward_right):
			pwm_forward_left = max(pwm_forward_left, pwm_forward_right)
			pwm_forward_right = pwm_forward_left
	elif category_name == "backward":
		
		pwm_back_left = min(pwm_back_left + 5, max_speed)
		pwm_back_right = min(pwm_back_right + 5, max_speed)
		pwm_forward_left = 0
		pwm_forward_right = 0
		if(pwm_back_left != pwm_back_right):
			pwm_back_left = max(pwm_back_left, pwm_back_right)
			pwm_back_right = pwm_back_left
	elif category_name == "left":
		pwm_forward_left = min(pwm_forward_left + 5, max_speed)
		pwm_back_left = 0
		pwm_back_right = min(pwm_back_right + 5, max_speed)
		pwm_forward_right = 0
	elif category_name == "right":
		pwm_forward_right = min(pwm_forward_right + 5, max_speed)
		pwm_back_left = min(pwm_back_left + 5, max_speed)
		pwm_back_right = 0
		pwm_forward_left = 0
	elif category_name == "stop":
		pwm_back_left = 0
		pwm_back_right = 0
		pwm_forward_right = 0
		pwm_forward_left = 0
  
	forward_left_motor.ChangeDutyCycle(pwm_forward_left)
	forward_right_motor.ChangeDutyCycle(pwm_forward_right)
	backward_left_motor.ChangeDutyCycle(pwm_back_left)
	backward_right_motor.ChangeDutyCycle(pwm_back_right)

def get_control():
    isRunning = True
    direction = 'none'
	# Continuously capture images from the camera and run inference
    while isRunning:
        if keyboard.is_pressed('w'):
            direction = 'forward'
        elif keyboard.is_pressed('a'):
            direction = 'left'
        elif keyboard.is_pressed('s'):
            direction = 'backward'
        elif keyboard.is_pressed('d'):
            direction = 'right'
        else:
            direction = 'stop'
        if keyboard.is_pressed('Esc'):
            break
		
        print(direction)
        motorDirection(category_name=category_name)



if __name__ == '__main__':
	get_control()