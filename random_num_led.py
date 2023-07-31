#임의의 숫자를 입력받아 LED 동작

import RPi.GPIO as GPIO
import time  #delay

#pin번호 할당
greenPin=19
bluePin=13
redPin=26

def white():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)

def yellow():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.HIGH)

def Off():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)

#main문
def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(bluePin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
    
    #아래 코드 반복
    while 1:
        keyboard=input("색상 선택: ")
        if keyboard=='r':
            GPIO.output(redPin,GPIO.HIGH) #빨강 on
            #print('red')
            time.sleep(1)
            Off() #led off
        elif keyboard=='b':
            GPIO.output(bluePin,GPIO.HIGH)
            #print('blue')
            time.sleep(1)
            Off()
        elif keyboard=='g':
            GPIO.output(greenPin,GPIO.HIGH)
            #print('green')
            time.sleep(1)
            Off()
        elif keyboard=='w':
            white()
            #print('white')
            time.sleep(1)
            Off()
        elif keyboard=='y':
            yellow()
            #print('yellow')
            time.sleep(1)
            Off()
        else:
            break

if __name__=='__main__':
    main()
