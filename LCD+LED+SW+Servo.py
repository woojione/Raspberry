import smbus
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

#pin number
sw1= 23
#sw2=13
greenPin=19
redPin=26
bluePin=13
servoPin=18

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

#setmode
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

#setup
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(bluePin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(servoPin,GPIO.OUT)

#GPIO.setup(servoPin, GPIO.OUT)
p = GPIO.PWM(servoPin, 50) # GPIO 12 for PWM with 50Hz
p.start(0) # Initialization

#RGB function
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

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  # Main program block

  # Initialise display
  lcd_init()

  while True:
    #sw 누르면 servo
    if GPIO.input(sw1) == GPIO.HIGH:
        white()
        for i in range(7,13,1): #서보모터 90->180도
          p.ChangeDutyCycle(i)
        lcd_string("LED ON",LCD_LINE_1)
        lcd_string("3",LCD_LINE_2)
        time.sleep(1)
        lcd_string("2",LCD_LINE_2)
        time.sleep(1)
        lcd_string("1",LCD_LINE_2)
        time.sleep(1)
        Off()
        lcd_string("LED OFF",LCD_LINE_1)
        lcd_string(" ",LCD_LINE_2)
    else:
       p.ChangeDutyCycle(7)
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)