#버튼 누르고 있으면 led on

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
r = 26
b=13
sw1=23
sw2=24


GPIO.setup(r, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 


def off():
    GPIO.output(r,GPIO.LOW)
    GPIO.output(b,GPIO.LOW)

def main():
    GPIO.output(r,False)
    GPIO.output(b,False)

    while True:
        
        if GPIO.input(sw1)==True:
            GPIO.output(r,True)
        elif GPIO.input(sw2)==True:
            GPIO.output(b,True)
        else:
            off()
        

try:
    main()
finally:
    GPIO.cleanup()