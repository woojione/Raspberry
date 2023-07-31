import RPi.GPIO as GPIO
import time
ECHO= 20
TRIG= 21
redPin=26
greenPin=19
bluePin=13

GPIO.setmode(GPIO. BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(bluePin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
PWM_LED= GPIO.PWM(redPin, 50)
PWM_LED.start(0)

while True:
    

    #print("distance measurement in progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    #print("waiting for sensor to settle")
    time.sleep(0.2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)


    while GPIO.input(ECHO)==0:
        pulse_start=time.time()

    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("distance:",distance,"cm")

    if distance<=5 :
        for duty in range(0,100,10):
            PWM_LED.ChangeDutyCycle(duty)
            time.sleep(0.1)
        for duty in range(100,0,-10):
            PWM_LED.ChangeDutyCycle(duty)
            time.sleep(0.1)
        print("warning!")

    else:
        PWM_LED.ChangeDutyCycle(0)
