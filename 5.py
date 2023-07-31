import smbus
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
bus= smbus.SMBus(1)
ADX_address= 0x53
# Create single-ended input on channels 0 and 1
vrx = AnalogIn(ads, ADS.P0)
vry = AnalogIn(ads, ADS.P1)
# Create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)

# X, Y, Z axis
ADX_X_addr= 0x32
ADX_Y_addr= 0x34
ADX_Z_addr= 0x36

#ADXL345
def init_ADXL345():
    bus.write_byte_data(ADX_address, 0x2D, 0x08)

def ADX_measure_acc(addr):
    acc0= bus.read_byte_data(ADX_address, addr)

    acc1= bus.read_byte_data(ADX_address, addr+1)

    acc= (acc1 << 8) + acc0

    if( acc > 0x1FF):
        acc= (65536 - acc)* -1
    acc= (acc* 3.9)/1000 #가속도 값으로 변환

    return acc

GPIO.setmode(GPIO. BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(bluePin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(servoPin, GPIO.OUT)
p = GPIO.PWM(servoPin, 50) # GPIO 12 for PWM with 50Hz
p.start(0) # Initialization


def joy():
        # Read the joystick position data
        vrx_pos = vrx.value
        vry_pos = vry.value
     # Determine the joystick direction
        if vrx_pos > 30000:
            direction = "left"
            for i in range(7,13,1): #서보모터 90->180도
                p.ChangeDutyCycle(i)
            print('left')
        elif vrx_pos < 10000:
            direction = "right"
            for i in range(7,1,-1): #서보모터 90->0도
                p.ChangeDutyCycle(i)
            print('right')
        elif vry_pos > 30000:
            direction = "up"
            GPIO.output(bluePin, GPIO.HIGH)
            print('up')
            
        elif vry_pos < 10000:
            direction = "down"
            GPIO.output(bluePin, GPIO.LOW)
            print('down')
        else:
            direction = "center"
            p.ChangeDutyCycle(7) #서보모터 90도
            print('center')

        # Draw the direction on the matrix display
        with canvas(device) as draw:
            if direction == "right":
                text(draw, (1, 1), ">", fill="white")
            elif direction == "left":
                text(draw, (1, 1), "<", fill="white")

            elif direction == "up":
                text(draw, (1, 1), "^", fill="white")
            
            elif direction == "down":
                text(draw, (1, 1), "v", fill="white")

def ad():
        x_acc = ADX_measure_acc(ADX_X_addr)
        y_acc = ADX_measure_acc(ADX_Y_addr)
        z_acc = ADX_measure_acc(ADX_Z_addr)

        if x_acc>0:
            direction = "right"
        elif x_acc<0:
            direction = "left"
        elif y_acc>0:
            direction = "up"
        elif y_acc<0:
            direction = "down"

        with canvas(device) as draw:
            if direction == "right":
                text(draw, (1, 1), ">", fill="white")
            elif direction == "left":
                text(draw, (1, 1), "<", fill="white")

            elif direction == "up":
                text(draw, (1, 1), "^", fill="white")
            
            elif direction == "down":
                text(draw, (1, 1), "v", fill="white")



def main():
    init_ADXL345()
    mylcd = LCD.lcd()
    while True:
        mylcd.lcd_clear()
        mylcd.lcd_display_string("CCTV On",1)
        joy()
        ad()


if __name__ == '__main__':
    main()