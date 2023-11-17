import RPi.GPIO as GPIO
from time import sleep
from gpiozero import button

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)
# button_1 = Button(16)
# button_2 = Button(20)

input_val = "FORWARD" #input value should be defined with input from the neural net. This could be accomplished by reading a value from an object that calculates using the neural network.
wheel_speed = 100

#
left_motor = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
right_motor = GPIO.PWM(32,1000)
left_motor.start(0)				#start PWM of required Duty Cycle 
right_motor.start(0)				#start PWM of required Duty Cycle 
while True:
    if val == "FORWARD":
        left_motor.ChangeDutyCycle(wheel_speed)
        right_motor.ChangeDutyCycle(wheel_speed)
    elif val == "BACKWARD":
        left_motor.ChangeDutyCycle(-wheel_speed)
        right_motor.ChangeDutyCycle(-wheel_speed)
    elif val == "LEFT":
        #Turning speeds may need to be less than driving speeds.
        left_motor.ChangeDutyCycle(-wheel_speed)
        right_motor.ChangeDutyCycle(wheel_speed)
    elif val == "RIGHT":
        #Turning speeds may need to be less than driving speeds.
        left_motor.ChangeDutyCycle(wheel_speed)
        right_motor.ChangeDutyCycle(-wheel_speed)
    elif val == "STOP":
        left_motor.ChangeDutyCycle(0)
        right_motor.ChangeDutyCycle(0)
    else:
        left_motor.ChangeDutyCycle(0)
        right_motor.ChangeDutyCycle(0)

