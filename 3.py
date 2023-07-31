import I2C_driver as LCD
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text

ECHO= 20
TRIG= 21
redPin=26
greenPin=19
bluePin=13
servoPin=18

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# Create single-ended input on channels 0 and 1
vrx = AnalogIn(ads, ADS.P0)
vry = AnalogIn(ads, ADS.P1)
# Create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)


GPIO.setmode(GPIO. BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(bluePin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(servoPin, GPIO.OUT)
p = GPIO.PWM(servoPin, 50) # GPIO 12 for PWM with 50Hz
p.start(0) # Initialization

# def demo(n, block_orientation, rotate, inreverse):
#     # create matrix device
#     serial = spi(port=0, device=0, gpio=noop())
#     device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
#                      rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)

def main():
    mylcd = LCD.lcd()
    while True:
        mylcd.lcd_clear()


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

        #num=[9,8,7,6,5,4,'3o','2ooo','1oooo']

        if distance>=4 : #거리 10cm이상
            mylcd.lcd_display_string("protect",1)
            time.sleep(1)
        elif distance<=4:
            mylcd.lcd_display_string("danger!",1)
            mylcd.lcd_display_string(str(distance),2)
            time.sleep(1)

        with canvas(device) as draw:
            if 9<distance <= 10:
                text(draw, (1, 1), "9", fill="white")
            elif 8<distance <= 9:
                text(draw, (1, 1), "8", fill="white")
            elif 7<distance <= 8:
                text(draw, (1, 1), "7", fill="white")
            elif 6<distance <= 7:
                text(draw, (1, 1), "6", fill="white")
            elif 5<distance <= 6:
                text(draw, (1, 1), "5", fill="white")
            elif 4<distance <= 5:
                text(draw, (1, 1), "4", fill="white")
            elif 3<distance <= 4:
                text(draw, (1, 1), "3", fill="white")
                #text(draw, (1, 1), "O", fill="white")
            elif 2<distance <= 3:
                text(draw, (1, 1), "2", fill="white")
            elif 1<distance <= 2:
                text(draw, (1, 1), "1", fill="white")



if __name__ == '__main__':
    main()