import RPi.GPIO as GPIO
import keyboard
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from time import time, sleep
from rpi_ws281x import *
import argparse

# Copyright 2023 The MediaPipe Authors. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain pwdt vision

# GPIO Setup
PWM_FREQ = 500  # Frequency for PWM
MOTOR_PINS = {
    "forward_left": 13,
    "backward_left": 12,
    "forward_right": 19,
    "backward_right": 18,
}
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Initialize all motor pins
for pin in MOTOR_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

# Create PWM instances for each motor
motors = {name: GPIO.PWM(pin, PWM_FREQ) for name, pin in MOTOR_PINS.items()}
for motor in motors.values():
    motor.start(0)  # Start with 0 duty cycle

# Global State Variables
pwm_values = {
    "back_left": 0,
    "back_right": 0,
    "forward_left": 0,
    "forward_right": 0,
}
max_speed = 50  # Maximum PWM duty cycle value
motor_states = {"left": "off", "right": "off"}
prev_times = {"left": time(), "right": time()}



def motorDirection(category_name: str = "none"):
    """Control motor direction based on gesture input."""
    global pwm_values, motor_states, prev_times

    def adjust_pwm(side: str, direction: str):
        """Helper function to ramp up PWM for left or right motors."""
        pwm_key = f"{direction}_{side}"
        state_key = f"{side}"
        prev_time_key = f"{side}"

        if pwm_values[pwm_key] < max_speed:
            if motor_states[state_key] == "off":
                prev_times[prev_time_key] = time()
                motor_states[state_key] = "ramping"
            elif motor_states[state_key] == "ramping":
                if time() - prev_times[prev_time_key] >= 0.5:
                    pwm_values[pwm_key] += 5
                    prev_times[prev_time_key] = time()
            else:
                motor_states[state_key] = "at speed"
                pwm_values[pwm_key] = max_speed

    # Control motor direction based on the recognized gesture category
    if category_name == "forward":
        adjust_pwm("left", "forward")
        adjust_pwm("right", "forward")
    elif category_name == "backward":
        adjust_pwm("left", "back")
        adjust_pwm("right", "back")
    elif category_name == "left":
        adjust_pwm("left", "forward")
        motor_states["right"] = "off"
        pwm_values["back_right"] = pwm_values["forward_right"] = 0
    elif category_name == "right":
        adjust_pwm("right", "forward")
        motor_states["left"] = "off"
        pwm_values["back_left"] = pwm_values["forward_left"] = 0
    else:  # Stop or unknown gesture
        motor_states["left"] = motor_states["right"] = "off"
        for key in pwm_values:
            pwm_values[key] = 0


def apply_motor_pwm():
    """Apply current PWM values to the motors."""
    motors["forward_left"].ChangeDutyCycle(pwm_values["forward_left"])
    motors["backward_left"].ChangeDutyCycle(pwm_values["back_left"])
    motors["forward_right"].ChangeDutyCycle(pwm_values["forward_right"])
    motors["backward_right"].ChangeDutyCycle(pwm_values["back_right"])

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


def motorStop(): # Function to gradually stop the motors
    global pwm_back_left, pwm_back_right, pwm_forward_left, pwm_forward_right, max_speed
    global forward_left_motor, backward_right_motor, forward_right_motor, backward_left_motor

    # Gradual stop when moving backward
    if pwm_back_left > 0 or pwm_back_right > 0:
        temp_left_speed = pwm_back_left
        temp_right_speed = pwm_back_right
        while pwm_back_left > 0 or pwm_back_right > 0:
            pwm_back_left = max(0, pwm_back_left - (temp_left_speed / 4))
            pwm_back_right = max(0, pwm_back_right - (temp_right_speed / 4))
            backward_left_motor.ChangeDutyCycle(pwm_back_left)
            backward_right_motor.ChangeDutyCycle(pwm_back_right)
            sleep(0.1)

    # Gradual stop when moving forward
    elif pwm_forward_left > 0 or pwm_forward_right > 0:
        temp_left_speed = pwm_forward_left
        temp_right_speed = pwm_forward_right
        while pwm_forward_left > 0 or pwm_forward_right > 0:
            pwm_forward_left = max(0, pwm_forward_left - (temp_left_speed / 4))
            pwm_forward_right = max(0, pwm_forward_right - (temp_right_speed / 4))
            forward_left_motor.ChangeDutyCycle(pwm_forward_left)
            forward_right_motor.ChangeDutyCycle(pwm_forward_right)
            sleep(0.1)



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
		motorStop()

	# else:
	# 	pwm_back_left = 0
	# 	pwm_back_right = 0
	# 	pwm_forward_right = 0
	# 	pwm_forward_left = 0
  
	forward_left_motor.ChangeDutyCycle(pwm_forward_left)
	forward_right_motor.ChangeDutyCycle(pwm_forward_right)
	backward_left_motor.ChangeDutyCycle(pwm_back_left)
	backward_right_motor.ChangeDutyCycle(pwm_back_right)

def get_control(
    model: str,
    num_hands: int,
    min_hand_detection_confidence: float,
    min_hand_presence_confidence: float,
    min_tracking_confidence: float,
    camera_id: int,
    width: int,
    height: int,
) -> None:
    """Run gesture recognition on images acquired from the camera."""
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    recognition_results = []
    fps_avg_frame_count = 10
    COUNTER, START_TIME = 0, time()

    def save_result(
        result: vision.GestureRecognizerResult,
        unused_output_image: mp.Image,
        timestamp_ms: int,
    ):
        """Callback function to save gesture recognition results and calculate FPS."""
        nonlocal COUNTER, START_TIME
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time() - START_TIME)
            START_TIME = time()
        recognition_results.append(result)
        COUNTER += 1

    # Initialize gesture recognizer model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=num_hands,
        min_hand_detection_confidence=min_hand_detection_confidence,
        min_hand_presence_confidence=min_hand_presence_confidence,
        min_tracking_confidence=min_tracking_confidence,
        result_callback=save_result,
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("ERROR: Unable to read from webcam.")
            break

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        recognizer.recognize_async(mp_image, time() * 1000)

        # Process recognized gestures
        if recognition_results:
            for gesture in recognition_results[0].gestures:
                category_name = gesture[0].category_name
                motorDirection(category_name)
                apply_motor_pwm()
            recognition_results.clear()

        # Display the image with recognized gesture (optional)
        cv2.imshow("Gesture Recognition", image)
        if cv2.waitKey(1) == 27:  # Exit on ESC key
            break

    recognizer.close()
    cap.release()
    cv2.destroyAllWindows()


# Main function
if __name__ == "__main__":
    get_control("my_gesture_recognizer.task", 1, 0.8, 0.5, 0.5, 0, 640, 480)
