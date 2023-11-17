import RPi.GPIO as GPIO
#The PWM motor/speed controller we use has a four-pin PWM setup where 1 pin controls forward movement and the other controls backwards movement. 
#This class abstracts that into a goBackward and goForward function on one motor

#Makes ONE (1) PWM motor go forward at a duty_cycle bewteen 0-100
def goForward(forwardPWMpin, backwardPWMpin, duty_cycle):
    forwardPWMpin.ChangeDutyCycle(duty_cycle)
    backwardPWMpin.ChangeDutyCycle(0)
#Makes ONE (1) PWM motor go backward at a duty_cycle bewteen 0-100 
def goBackward(forwardPWMpin, backwardPWMpin, duty_cycle):
    forwardPWMpin.ChangeDutyCycle(0)
    backwardPWMpin.ChangeDutyCycle(duty_cycle)
#Stops one motor
def stopMotor(forwardPWMpin, backwardPWMpin):
    forwardPWMpin.ChangeDutyCycle(0)
    backwardPWMpin.ChangeDutyCycle(0)
