# sudo python3 button-keyboard-motor-control.py 
# cd cv-wheelchair/CV-Wheelchair/hardware
import RPi.GPIO as GPIO
import keyboard
from time import sleep
import time
#from gpiozero import button

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
#button_1 = Button(36)
#button_2 = Button(38)
#

freq = 500
pi_pwm = GPIO.PWM(ledpin, freq)	#create PWM instance with frequency
pi_pwm_2 = GPIO.PWM(13,freq)
pi_pwm.start(0)				#start PWM of required Duty Cycle 
pi_pwm_2.start(0)				#start PWM of required Duty Cycle 

motor2_forward = GPIO.PWM(18, freq)
motor2_backward = GPIO.PWM(19,freq)
motor2_forward.start(0)
motor2_backward.start(0)


pwm_back_left = 0
pwm_back_right = 0
pwm_forward_left = 0
pwm_forward_right = 0

max_speed = 45

l_state = "off"
r_state = "off"

prevTimeL = time.time()
prevTimeR = time.time()

def ramp_motor_speed(pwm_instance, final_speed, ramp_time=2.0):
    current_percentage = 0.05  # Start from the defined percentage
    increment_time = 0.1  # Time between increments (in seconds)
    increment_value = (1.0 - 0.05) / (ramp_time / increment_time)  # Calculate increment value

    while current_percentage <= 1.0:  # Ramp up to 100%
        current_speed = final_speed * current_percentage  # Calculate current speed
        pwm_instance.ChangeDutyCycle(current_speed)
        sleep(increment_time)  # Wait for the next increment
        current_percentage += increment_value  # Increase the percentage

    # Set to final speed to ensure it's at the target speed
    pwm_instance.ChangeDutyCycle(final_speed)

i = 0
while True:
	pi_pwm.ChangeDutyCycle(pwm_forward_left)
	motor2_backward.ChangeDutyCycle(pwm_forward_right)
	print("Left (Q) " + str(pwm_forward_left))
	print("Right (P) " + str(pwm_forward_right))
	if (keyboard.is_pressed('q')):
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
		print ("button 1 was pushed")
	else:
		l_state = "off"
		pwm_forward_left = 0

	if  keyboard.is_pressed('e'):
		pi_pwm_2.ChangeDutyCycle(45)
		print ("button 2 was pushed") 
	else:
		pi_pwm_2.ChangeDutyCycle(0) #stop motor
        
	if keyboard.is_pressed('i'):
		motor2_forward.ChangeDutyCycle(45)
	else:
		motor2_forward.ChangeDutyCycle(0)
        
	if keyboard.is_pressed('p'):
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
	else:
		pwm_forward_right = 0
	sleep(0.01)
