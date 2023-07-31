import I2C_driver as LCD
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import smbus
# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.core.legacy import text

ECHO= 20
TRIG= 21
redPin=26
greenPin=19
bluePin=13
servoPin=18

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
# Create single-ended input on channels 0 and 1
vrx = AnalogIn(ads, ADS.P0)
vry = AnalogIn(ads, ADS.P1)



GPIO.setmode(GPIO. BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(bluePin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(servoPin, GPIO.OUT)
p = GPIO.PWM(servoPin, 50) # GPIO 12 for PWM with 50Hz
p.start(0) # Initialization


bus = smbus.SMBus(1)

# IC address
address = 0x53

# x-axis, y-axis, z-axis adress
x_adr = 0x32
y_adr = 0x34
z_adr = 0x36

# ADXL345 init
def init_ADXL345():    
    print('ADXL345 init function')
    bus.write_byte_data(address, 0x2D, 0x08)

# data measure
def measure_acc(adr):    
    acc0 = bus.read_byte_data(address, adr)

    acc1 = bus.read_byte_data(address, adr + 1)

    acc = (acc1 << 8) + acc0

    if acc > 0x1FF:
        acc = (65536 - acc) * -1

    acc = acc * 3.9 / 1000

    return acc

def main():
    mylcd = LCD.lcd()
    init_ADXL345()

    while True:
        mylcd.lcd_clear()
        #mylcd.lcd_display_string("CCTV On",1)

        #초음파
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG,False)
        time.sleep(0.2)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)

        #초음파
        while GPIO.input(ECHO)==0:
            pulse_start=time.time()

        while GPIO.input(ECHO)==1:
            pulse_end=time.time()
        
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        print("distance:",distance,"cm")


        x_acc = measure_acc(x_adr)

        if distance<=5 : #거리 5cm이하
            if 0.06<x_acc<0.08:
                for i in range(7,1,-1): #서보모터 90->0도
                    p.ChangeDutyCycle(i)
                mylcd.lcd_display_string("Rock Off!",2)
                time.sleep(5)
            else:
                p.ChangeDutyCycle(7)
                mylcd.lcd_display_string("Danger!!",1)
                mylcd.lcd_display_string("Rock On!",2)
                time.sleep(1)

        elif distance>=5 : #거리 5cm이상            
            p.ChangeDutyCycle(7) #도어락 잠금
            mylcd.lcd_display_string("Rock On!",2)
            time.sleep(1)


if __name__ == '__main__':
    main()