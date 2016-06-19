#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import RPi.GPIO as GPIO  
import time, sys
import threading

in1 = 38
out1 = 40
out2 = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
tr = False

def watchIO():
    
    
    try:
        while tr :
            
            in1v = GPIO.input(in1)
            GPIO.output(out1,in1v)
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        print 'EXIT::::::'

        

tr = True
t = threading.Thread(target = watchIO, name = 'watchIO_thread')
t.start()

cou = 0
try:
    while 1 : 
        in1v = GPIO.input(in1)
        GPIO.output(out2,in1v)
        time.sleep(0.01)
except KeyboardInterrupt:
        tr = False
        print 'EXIT::::::'
        GPIO.output(out2,False)
        GPIO.output(out1,False)