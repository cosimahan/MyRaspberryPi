#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import RPi.GPIO as GPIO  
import time
import os
import sys
import subprocess
import thread  

from flask import Flask ,render_template ,request ,url_for
from rpicar import Cars

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.debug = True

#out1 = 40



GPIO.setmode(GPIO.BOARD)
wlt1= 31
wlt2= 33
wrt1= 35
wrt2= 37

speedGo = 100
speedDiffer = 80


car1 = Cars(wlt1,wlt2,wrt1,wrt2)        


'''
pl = GPIO.PWM(wlp, 50)
pl.start(10)
pr = GPIO.PWM(wrp, 50)
pr.start(10)

def go(wp,wt1,wt2):
    p = GPIO.PWM(wp, 50)
    p.start(10)
    GPIO.output(wt1, GPIO.HIGH)
    GPIO.output(wt2, GPIO.LOW)
    
    p.ChangeDutyCycle(80)

    

def stop(wp,wt1,wt2):
    p = GPIO.PWM(wp, 50)
    p.start(10)
    GPIO.output(wt1, GPIO.LOW)
    GPIO.output(wt2, GPIO.LOW)
    
    p.ChangeDutyCycle(0)
'''    
    

    
@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/gpio/')
def gpio():

    ret = "<br>"
    
    #ipin = int(request.form['pin'])
    ipin = int(request.args.get('pin', '-1'))
    
    ret += request.args.get('pin', 'NULL') + "  " + request.args.get('act', 'NULL') + "<br>"
    if ipin >= 1 and ipin <= 40:
        if request.args.get('act', 'NULL') == 'on' :
            GPIO.setup(ipin, GPIO.OUT)
            GPIO.output(ipin, GPIO.HIGH)
            ret += "ON SUCCESS<br>"
        elif request.args.get('act', 'NULL') == 'off':
            GPIO.setup(ipin, GPIO.OUT)
            GPIO.output(ipin, GPIO.LOW)
            ret += "OFF SUCCESS<br>"
    else:
        pass
    
    pins = range(1,41,2)
    
    '''
    for i in range(1,41):
        ret += str(i)+" <a href=?pin="+str(i)+"&act=on>on</a> <a href=?pin="+str(i)+"&act=off>off</a>"
        if i%2 : ret += "&nbsp;&nbsp;&nbsp;&nbsp;"
        else : ret += "<br>"
    '''

    return render_template('gpio.html', html_ret=ret, html_pins=pins)
    
    
    
@app.route('/direction-control/')
def directionControl():
    ret = "<br>"
    return render_template('direction-control.html', html_ret=ret)
       
@app.route('/direction-control/do/')
def directionControlDo():
    global speedGo
    global speedDiffer

    ret = "<br>"
    goSpeed = request.args.get('go-speed', 'NULL')
    turnSpeed = request.args.get('turn-speed', 'NULL')
    ret += goSpeed + turnSpeed + "<br>"
    
    toGetSpeed = request.args.get('get-speed', 'NULL')
    
    action = request.args.get('act', 'NULL')
    ret += action + "<br>"
    
    if goSpeed != 'NULL':
        speedGo = int(goSpeed)
        ret += "GSPEED"
        return ret
    if turnSpeed != 'NULL':
        speedDiffer = int(turnSpeed)
        ret += "TSPEED"
        return ret
    
    #if toGetSpeed != 'NULL'
    if toGetSpeed == 'goSpeed':
        return str(speedGo)
    elif toGetSpeed == 'turnSpeed':
        return str(speedDiffer)
    
    if action == "forward":
        car1.run(+speedGo,0)
        
        ret += "F"
    elif action == "stop":
        car1.stop()
        ret += "S"
    elif action =="backward":
        car1.run(-speedGo,0)
        ret += "B"
    elif action =="turn-left":
        car1.run(0,-speedDiffer)
        ret += "L"
    elif action =="turn-right":
        car1.run(0,+speedDiffer)
        ret += "R"
    elif action =="forward-left":
        car1.run(+speedGo,-speedDiffer)
        ret += "FL"
    elif action =="forward-right":
        car1.run(+speedGo,+speedDiffer)
        ret += "FR"
    elif action =="backward-left":
        car1.run(-speedGo,+speedDiffer)
        ret += "BL"
    elif action =="backward-right":
        car1.run(-speedGo,-speedDiffer)
        ret += "BR" 
    else :
        ret += "Nothing to do"
    return ret
    
"""
@app.route('/<int:no_io>/')
def io(no_io):
    ret = "$"+str(no_io)
    return ret+''' FUCK
<br>
<a href=on/>on</a>
<br>
<a href=off/>off</a>'''

@app.route('/<int:no_io>/on/')
def on(no_io):

    GPIO.setup(no_io, GPIO.OUT)
    GPIO.output(no_io, GPIO.HIGH)
    ret = "$"+str(no_io)
    return ret+'''  ON
<br>
<a href=../off/>off</a> <br>'''#+str(url_for('index'))
    
@app.route('/<int:no_io>/off/')
def off(no_io):

    GPIO.setup(no_io, GPIO.OUT)
    GPIO.output(no_io, GPIO.LOW)
    ret = "$"+str(no_io)
    return ret+'''  OFF
<br>
<a href=../on/>on</a> <br>'''#+str(url_for('index'))
"""


@app.route('/video-stream/')
def videoStream():
    return render_template('video-stream.html')
    
@app.route('/direction-video/')
def directionVideo():
    return render_template('direction-video.html')

@app.route('/shell/',methods=['GET', 'POST'])
def shell_exec():
    ret = ''
    if request.method == 'POST':
        try :
            cmd = request.form['exec']
        except  KeyError, e:
            cmd = 'NULL'
            ret += "KeyError"
        
    else :
        cmd = request.args.get('exec', 'NULL')
        
    if cmd != 'NULL':
        ret += cmd+'<br>'
        if os.system(cmd) == 0:
            ret += "SUCCESS"
        else:
            ret += "FAILED"
            
    if request.method == 'POST': 
        return ret
    else:
        return render_template('shell.html', html_ret=ret)
        
@app.route('/speech/',methods=['GET', 'POST'])
def speech_ekho():
    ret = ''
    ekhoCmd = 'ekho '
    if request.method == 'POST':
        try :
            cmd = ekhoCmd+'"'+request.form['text']+'" &'
        except  KeyError, e:
            cmd = 'NULL'
            ret += "KeyError"
        
    else :
        cmd = 'NULL'
        
    if cmd != 'NULL':
        ret += cmd+'<br>'
        '''
        if os.system(cmd) == 0:
            ret += "SUCCESS"
        else:
            ret += "FAILED"
        '''
        
        ekhoProcess = subprocess.Popen(cmd, shell=True)
        ret += "SUCCESS" 
        thread.start_new_thread(lookingProcess, (ekhoProcess,10))
            
    if request.method == 'POST': 
        return ret
    else:
        return render_template('speech.html', html_ret=ret)
def lookingProcess(lookProcess,waitTime):
    print("############")
    time.sleep(waitTime)
    print("$$$$$$$$$$"+str(subprocess.Popen.poll(lookProcess)) )
   # if subprocess.Popen.poll(lookProcess) is None :
   #     print("%%%%%%%%%%%")
    lookProcess.kill()
    print("&&&&&&&&&&&&&&&&&")
    
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=False)
