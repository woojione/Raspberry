#버튼 한번 누르면 led on 다시 누르면 off

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
    GPIO.output(r,GPIO.LOW)
    GPIO.output(b,GPIO.LOW)
    flag=0
    flag2=0
    while True:
    
        if GPIO.input(sw1)==GPIO.HIGH:
            flag+=1
            print("flag1: ",flag)
            time.sleep(0.5)

        elif GPIO.input(sw2)==GPIO.HIGH:
            flag2+=1
            print("flag2: ",flag)
            time.sleep(0.5)

        if (flag%2)==1:
            GPIO.output(r,GPIO.HIGH)
        elif (flag%2)==0:
            GPIO.output(r,GPIO.LOW)

        if (flag2%2)==1:
            GPIO.output(b,GPIO.HIGH)
        elif (flag2%2)==0:
            GPIO.output(b,GPIO.LOW)


try:
    main()
finally:
    GPIO.cleanup()