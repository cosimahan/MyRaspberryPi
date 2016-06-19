# -*- coding: utf-8 -*-  
import RPi.GPIO as GPIO  
import time
import smbus


class PCA9685:
    
    mode1adr=0x00 #0x00
    mode2adr=0x01
    subadr1=0x02
    subadr2=0x03
    subadr3=0x04
    allcalladr=0x05
    led0_on_l_adr=0x06
    led0_on_h_adr=0x07
    led0_off_l_adr=0x08
    led0_off_h_adr=0x09
    led1_on_l_adr=0x0a
    led1_on_h_adr=0x0b
    led1_off_l_adr=0x0c
    led1_off_h_adr=0x0d
    #....................
    all_led_on_l_adr=0xfa
    all_led_on_h_adr=0xfb
    all_led_off_l_adr=0xfc
    all_led_off_h_adr=0xfd
    pre_scale=0xfe #freq
    
    init_mode=0x01
    
    freq = 0
    
    def __init__(self,i2c_ch,PCA9685adr):
        self.PCA9685adr = PCA9685adr
        self.bus = smbus.SMBus(i2c_ch)
        self.bus.write_byte_data(self.PCA9685adr,self.mode1adr,self.init_mode)
        self.setFreq(50)
        
    def toByte(self,x1):
        if x1<0xff:
            x_l=x1
            x_h=0x00
        else :
            x_h=x1/256
            x_l=x1-x_h*256
        return x_l,x_h
        
    def write_16(self,led_num,uInt16):
        (uInt16L,uInt16H)=self.toByte(uInt16)
        self.bus.write_byte_data(self.PCA9685adr,led_num,uInt16L)
        self.bus.write_byte_data(self.PCA9685adr,led_num+1,uInt16H)
        
    def write_8(self,led_num,uInt8):
        self.bus.write_byte_data(self.PCA9685adr,led_num,uInt8)
        
        
    def setFreq(self,freq):
        data=(25000000/(4096*freq))-1
        data=int(data+0.49)
        oldmode = self.bus.read_byte_data(self.PCA9685adr,self.mode1adr)
        newmode = (oldmode & 0x7F) | 0x10
        self.bus.write_byte_data(self.PCA9685adr,self.mode1adr,newmode)
        self.bus.write_byte_data(self.PCA9685adr,self.pre_scale,data)
        self.bus.write_byte_data(self.PCA9685adr,self.mode1adr,oldmode)
        
        time.sleep(0.005)
        self.bus.write_byte_data(self.PCA9685adr,self.mode1adr,oldmode|0xa1)
        self.bus.write_byte_data(self.PCA9685adr,self.mode1adr,oldmode)
        self.freq = freq
    def getFreq(self):
        return self.freq
    
    def setDuty(self,led_num,duty):
        data = int(float(duty)/100*4095)
        
        if duty < 0:
            self.write_16(self.led0_on_l_adr+4*led_num,0)
            self.write_16(self.led0_off_l_adr+4*led_num,0)
        if duty < 100 and duty >= 0:
            self.write_16(self.led0_on_l_adr+4*led_num,0)
            self.write_16(self.led0_off_l_adr+4*led_num,data)
        elif duty >= 100:
            self.write_16(self.led0_on_l_adr+4*led_num,0x1000)
            self.write_16(self.led0_off_l_adr+4*led_num,0x0FFF)



class Cars(object):
    
    i2c_ch = 1
    pca9685addr = 0x40
    
    pwm_ch_A = 0
    pwm_ch_B = 1

    def __init__(self,wheelDireA1,wheelDireA2,wheelDireB1,wheelDireB2):
        self.pca9685 = PCA9685(self.i2c_ch,self.pca9685addr) # 0x40 is pca9685's addr
        self.wheelA = Wheels(self.pca9685,self.pwm_ch_A,wheelDireA1,wheelDireA2)
        self.wheelB = Wheels(self.pca9685,self.pwm_ch_B,wheelDireB1,wheelDireB2)
        
    def run(self,speed,speedDiffer):
        
        self.wheelA.run(speed+speedDiffer)
        
        self.wheelB.run(speed-speedDiffer)
        
    def stop(self):
        self.wheelA.stop()
        self.wheelB.stop()
        
        
    

class Wheels(object):
    def __init__(self,pca9685,pwm_ch,wheelDire1,wheelDire2):
        self.pca9685 = pca9685
        self.pwm_ch = pwm_ch
        self.wheelDire1 = wheelDire1
        self.wheelDire2 = wheelDire2
        GPIO.setup(self.wheelDire1, GPIO.OUT)
        GPIO.setup(self.wheelDire2, GPIO.OUT)


    def run(self,speed,freq=50):
        if(self.pca9685.getFreq != freq):
            self.pca9685.setFreq(freq)
        
        
        if speed > 0:
            GPIO.output(self.wheelDire1, GPIO.HIGH)
            GPIO.output(self.wheelDire2, GPIO.LOW)
            self.pca9685.setDuty(self.pwm_ch,speed)
            
        elif speed == 0:
            GPIO.output(self.wheelDire1, GPIO.LOW)
            GPIO.output(self.wheelDire2, GPIO.LOW)
            self.pca9685.setDuty(self.pwm_ch,100)# let wheel's speed = 0
        elif speed < 0:
            GPIO.output(self.wheelDire1, GPIO.LOW)
            GPIO.output(self.wheelDire2, GPIO.HIGH)
            self.pca9685.setDuty(self.pwm_ch,-speed)
            
        
        
    def stop(self):

        GPIO.output(self.wheelDire1, GPIO.LOW)
        GPIO.output(self.wheelDire2, GPIO.LOW)
        self.pca9685.setDuty(self.pwm_ch,0)
        #self.p.stop()