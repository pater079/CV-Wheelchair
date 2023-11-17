import RPi.GPIO as GPIO
import speed-controller-helper as speed_control
from time import sleep
from gpiozero import button

GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		

#set pin numbering system
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(32,GPIO.OUT)

#set up buttons
button_1 = Button(16)
button_2 = Button(20)

#RESET THE PINS AND CYCLES TO THE CORRECT VALUES
motor_frequency = 50
motor1_forward = GPIO.PWM(12, motor_frequency)		#create PWM instance with frequency
motor1_backward = GPIO.PWM(13, motor_frequency)
motor2_forward = GPIO.PWM(32, motor_frequency)
motor2_backward = GPIO.PWM(19, motor_frequency)

motor1_forward.start(0)				#start PWM of required Duty Cycle 
motor2_forward.start(0)				#start PWM of required Duty Cycle 
while True:
    if button_1.is_pressed:
        speed_control.goForward(motor1_forward, motor1_backward, 45)
    else:
       speed_control.stopMotor(motor1_forward, motor1_backward)

    if button_2.is_pressed:
        speed_control.goForward(motor2_forward, motor2_backward, 45)
    else:
        speed_control.stopMotor(motor2_forward, motor2_backward)#stop motor
