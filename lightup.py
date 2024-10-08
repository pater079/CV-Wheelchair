import RPi.GPIO as GPIO
import keyboard
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from time import time, sleep
from rpi_ws281x import *
import argparse

def light_on():
    print("hello")
    # LED strip configuration:
    LED_COUNT      = 30     # Number of LED pixels.
    LED_PIN        = 11      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
    LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

if __name__ == "__main__":
    light_on()