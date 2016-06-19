#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import RPi.GPIO as GPIO  
import time
import sys

print sys.argv

out1 = int(sys.argv[1])

GPIO.setmode(GPIO.BOARD)  
GPIO.setup(out1, GPIO.OUT)

if sys.argv[2] == 'on':
	GPIO.output(out1, GPIO.HIGH)
elif sys.argv[2] == 'off' :
	GPIO.output(out1, GPIO.LOW)
