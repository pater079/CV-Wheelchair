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
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

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
	global pwm_back_left, pwm_back_right, pwm_forward_left,pwm_forward_right, max_speed, l_state, r_state, prevTimeL, prevTimeR
	
	i = 0
	def forwardMotor(left: bool):
		global pwm_back_left, pwm_back_right, pwm_forward_left,pwm_forward_right, max_speed, l_state, r_state, prevTimeL, prevTimeR
		if(left):
			if(pwm_forward_left < max_speed):
				if(l_state == "off"):
					currTimeL = time.time()
					prevTimeL = time.time()
					l_state = "ramping"
				elif(l_state == "ramping"):
					currTimeL = time.time()
					if(currTimeL - prevTimeL >= 0.5):
						pwm_forward_left = pwm_forward_left + 5 
						prevTimeL = currTimeL
			else:
				l_state = "at speed"			
				pwm_forward_left = max_speed
		else:
			if(pwm_forward_right < max_speed):
				if(r_state == "off"):
					currTimeR = time.time()
					prevTimeR = time.time()
					r_state = "ramping"
				elif(r_state == "ramping"):
					currTimeR = time.time()
					if(currTimeR - prevTimeR >= 0.5):
						pwm_forward_right = pwm_forward_right + 5 
						prevTimeR = currTimeR
			else:
				r_state = "at speed"
				pwm_forward_right = max_speed
	
	def backwardMotor(left: bool):
		global pwm_back_left, pwm_back_right, pwm_forward_left,pwm_forward_right, max_speed, l_state, r_state, prevTimeL, prevTimeR
		if(left):
			if(pwm_back_left < max_speed):
				if(l_state == "off"):
					currTimeL = time.time()
					prevTimeL = time.time()
					l_state = "ramping"
				elif(l_state == "ramping"):
					currTimeL = time.time()
					if(currTimeL - prevTimeL >= 0.5):
						pwm_back_left = pwm_back_left + 5 
						prevTimeL = currTimeL
			else:
				l_state = "at speed"			
				pwm_back_left = max_speed
		else:
			if(pwm_back_right < max_speed):
				if(r_state == "off"):
					currTimeR = time.time()
					prevTimeR = time.time()
					r_state = "ramping"
				elif(r_state == "ramping"):
					currTimeR = time.time()
					if(currTimeR - prevTimeR >= 0.5):
						pwm_back_right = pwm_back_right + 5 
						prevTimeR = currTimeR
			else:
				r_state = "at speed"
				pwm_back_right = max_speed
    
	if category_name == "forward":
		forwardMotor(True)
		forwardMotor(False)
	elif category_name == "backward":
		backwardMotor(True)
		backwardMotor(False)
	elif category_name == "left":
		forwardMotor(True)
		r_state = "off"
		pwm_back_right = 0
		pwm_forward_right = 0
	elif category_name == "right":
		forwardMotor(False)
		l_state = "off"
		pwm_back_left = 0
		pwm_forward_left = 0
	elif category_name == "stop":
		r_state = "off"
		pwm_back_right = 0
		pwm_forward_right = 0
		l_state = "off"
	else:
		r_state = "off"
		pwm_back_right = 0
		pwm_forward_right = 0
		l_state = "off"


def motorStop(): #function to gradually stop the motors
	global pwm_back_left, pwm_back_right, pwm_forward_left,pwm_forward_right, max_speed, forward_left_motor, backward_right_motor,forward_right_motor, backward_left_motor

	if pwm_back_left > 0 or pwm_back_right > 0: #if the motors are moving backward
		temp_left_speed = pwm_back_left
		temp_right_speed = pwm_back_right
		pwm_back_left = 0 
		pwm_back_right = 0
		pwm_back_left = temp_left_speed
		pwm_back_right = temp_right_speed
		forward_left_motor.ChangeDutyCycle(pwm_forward_left)
		forward_right_motor.ChangeDutyCycle(pwm_forward_right)
		backward_left_motor.ChangeDutyCycle(pwm_back_left)
		backward_right_motor.ChangeDutyCycle(pwm_back_right)
		while pwm_forward_left > 0 and pwm_forward_right > 0:
			pwm_forward_right = max(0, (pwm_forward_right - (temp_right_speed/4)))
			pwm_forward_left = max(0, (pwm_forward_left - (temp_left_speed/4)))
			
		

		

	elif pwm_forward_left > 0 or pwm_forward_right > 0: #if the motors are moving forward
		temp_left_speed2 = pwm_forward_left
		temp_right_speed2 = pwm_forward_right
		pwm_forward_right = 0 
		pwm_forward_left = 0
		pwm_forward_left = temp_left_speed2
		pwm_forward_right = temp_right_speed2
		forward_left_motor.ChangeDutyCycle(pwm_forward_left)
		forward_right_motor.ChangeDutyCycle(pwm_forward_right)
		backward_left_motor.ChangeDutyCycle(pwm_back_left)
		backward_right_motor.ChangeDutyCycle(pwm_back_right)
		while pwm_back_left > 0 and pwm_back_right > 0:
			pwm_back_right = max(0, (pwm_back_right - (temp_right_speed2/4)))
			pwm_back_left = max(0, (pwm_back_left - (temp_left_speed2/4)))


def motorDirection2(category_name: str = 'none'):
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
		if(pwm_back_left != pwm_back_right): #if uneven speeds are set, set the speed to the highest speed
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
	# else:
	# 	pwm_back_left = 0
	# 	pwm_back_right = 0
	# 	pwm_forward_right = 0
	# 	pwm_forward_left = 0
  
	forward_left_motor.ChangeDutyCycle(pwm_forward_left)
	forward_right_motor.ChangeDutyCycle(pwm_forward_right)
	backward_left_motor.ChangeDutyCycle(pwm_back_left)
	backward_right_motor.ChangeDutyCycle(pwm_back_right)

def get_control(model: str, num_hands: int,
	min_hand_detection_confidence: float,
	min_hand_presence_confidence: float, min_tracking_confidence: float,
	camera_id: int, width: int, height: int) -> None:
	
	"""Continuously run inference on images acquired from the camera.

	Args:
		model: Name of the gesture recognition model bundle.
		num_hands: Max number of hands can be detected by the recognizer.
		min_hand_detection_confidence: The minimum confidence score for hand
		min_hand_presence_confidence: The minimum confidence score of hand
			presence score in the hand landmark detection.
		min_tracking_confidence: The minimum confidence score for the hand
			tracking to be considered successful.
		camera_id: The camera id to be passed to OpenCV.
		width: The width of the frame captured from the camera.
		height: The height of the frame captured from the camera.
	"""

	# Start capturing video input from the camera
	cap = cv2.VideoCapture(camera_id)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

	fps_avg_frame_count = 10
	recognition_frame = None
	recognition_result_list = []

	def save_result(result: vision.GestureRecognizerResult,
					unused_output_image: mp.Image, timestamp_ms: int):
		global FPS, COUNTER, START_TIME

		# Calculate the FPS
		if COUNTER % fps_avg_frame_count == 0:
			FPS = fps_avg_frame_count / (time.time() - START_TIME)
			START_TIME = time.time()

		recognition_result_list.append(result)
		COUNTER += 1

	# Initialize the gesture recognizer model
	base_options = python.BaseOptions(model_asset_path=model)
	options = vision.GestureRecognizerOptions(base_options=base_options,
											running_mode=vision.RunningMode.LIVE_STREAM,
											num_hands=num_hands,
											min_hand_detection_confidence=min_hand_detection_confidence,
											min_hand_presence_confidence=min_hand_presence_confidence,
											min_tracking_confidence=min_tracking_confidence,
											result_callback=save_result)
	recognizer = vision.GestureRecognizer.create_from_options(options)

	# Continuously capture images from the camera and run inference
	while cap.isOpened():
		success, image = cap.read()
		if not success:
			sys.exit(
				'ERROR: Unable to read from webcam. Please verify your webcam settings.'
			)

		image = cv2.flip(image, 1)
		# Convert the image from BGR to RGB as required by the TFLite model.
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
		# Run gesture recognizer using the model.
		recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)
		current_frame = image


		if recognition_result_list:
			for hand_index, hand_landmarks in enumerate(
				recognition_result_list[0].hand_landmarks):
				if recognition_result_list[0].gestures:
					gesture = recognition_result_list[0].gestures[hand_index]
					category_name = gesture[0].category_name
					print(category_name)
					motorDirection2(category_name=category_name)
					# forward_left_motor.ChangeDutyCycle(pwm_forward_left)
					# forward_right_motor.ChangeDutyCycle(pwm_forward_right)
					# backward_left_motor.ChangeDutyCycle(pwm_back_left)
					# backward_right_motor.ChangeDutyCycle(pwm_back_right)

		recognition_frame = current_frame
		recognition_result_list.clear()

		if recognition_frame is not None:
			cv2.imshow('gesture_recognition', recognition_frame)

		# Stop the program if the ESC key is pressed.
		if cv2.waitKey(1) == 27:
			break

	recognizer.close()
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	# while True:
		# forward_left_motor.ChangeDutyCycle(pwm_forward_left)
		# forward_right_motor.ChangeDutyCycle(pwm_forward_right)
		# backward_left_motor.ChangeDutyCycle(pwm_back_left)
		# backward_right_motor.ChangeDutyCycle(pwm_back_right)
	get_control('my_gesture_recognizer.task', 1, 0.8,
			0.5, 0.5,
			0, 640, 480)