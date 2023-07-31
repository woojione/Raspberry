#sw1을 누르면 RED led duty 증가
#sw2을 누르면 BLUE led duty 증가
#Interrupt방식

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


def led(pin):
    PWM_LED= GPIO.PWM(pin, 50)
    PWM_LED.start(0)
    for duty in range(0,100,10):
        PWM_LED.ChangeDutyCycle(duty)
        time.sleep(0.5)
    PWM_LED.ChangeDutyCycle(0)


def off():
    GPIO.output(r,GPIO.LOW)
    GPIO.output(b,GPIO.LOW)

def main():
    GPIO.output(r,False)
    GPIO.output(b,False)
    #GPIO.add_event_detect(sw2,GPIO.FALLING,led)

    while True:
        if GPIO.input(sw1)==GPIO.HIGH:
            led(r)
        elif GPIO.input(sw2)==GPIO.HIGH:
            led(b)
        else:
            off()
        

try:
    main()
finally:
    GPIO.cleanup()