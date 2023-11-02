import RPi.GPIO as GPIO
from time import sleep
from gpiozero import button

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)
button_1 = Button(16)
button_2 = Button(20)
#
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm_2 = GPIO.PWM(32,1000)
pi_pwm.start(0)				#start PWM of required Duty Cycle 
pi_pwm_2.start(0)				#start PWM of required Duty Cycle 
while True:
    if button_1.is_pressed:
        pi_pwm.ChangeDutyCycle(100)
    else:
        pi_pwm.ChangeDutyCycle(0) #stop motor

    if button_2.is_pressed:
        pi_pwm_2.ChangeDutyCycle(100)
    else:
        pi_pwm_2.ChangeDutyCycle(0) #stop motor
