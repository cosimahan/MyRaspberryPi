#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import nokia5110
import time
screen = nokia5110.Nokia5110(15,13,12,11)
while True:
    cmd = """ifconfig eth0 | awk '/inet addr/ {split($2, a, \":\"); print a[2]}'"""
    p = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    eth0IP = p.stdout.read().strip()
    
    cmd = """ifconfig wlan0 | awk '/inet addr/ {split($2, a, \":\"); print a[2]}'"""
    p = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    wlan0IP = p.stdout.read().strip()


    cmd = """iwconfig wlan0 | awk '/ESSID/ {split($4, a, \"\\\"\"); print a[2]}'"""
    p = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    wlan0Essid = p.stdout.read().strip()

    #if int(time.strftime("%S", time.localtime()))%6 == 0:
    screen.resetScreen()
    
    screen.printLine('eth0: '+eth0IP,0)
    screen.printLine(eth0IP,1)
    screen.printLine('wlan0: '+wlan0Essid,2)
    screen.printLine(wlan0IP,3)
    screen.printLine(time.strftime("%m-%d %H:%M:%S", time.localtime()),5)
    
    time.sleep(0.1)

