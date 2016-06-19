#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
pwm1 = GPIO.PWM(36, 100)
pwm1.start(90)
pwm2 = GPIO.PWM(38, 100)
pwm2.start(50)


try:
    while 1:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass


pwm1.stop()
pwm2.stop()
GPIO.cleanup()
	
