import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
pwm1 = GPIO.PWM(8, 100)
pwm1.start(50)

file = open("/sys/class/thermal/thermal_zone0/temp") 
p=8
temp_offset=30

try:
	while 1 :

		file.seek(0)
		temp = int(file.read()) / 1000 
		error=temp-temp_offset
		dc=p*error
		if dc < 0 :
			dc = 0
		if dc > 100 :
			dc = 100
		pwm1.ChangeDutyCycle(dc)
		time.sleep(1)

except KeyboardInterrupt:
	file.close()  
	print 'EXIT::::::'

pwm1.stop()
GPIO.cleanup()
	
