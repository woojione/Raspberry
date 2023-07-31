import I2C_driver as LCD
from time import *
import smbus

bus= smbus.SMBus(1)

# IC address
ADX_address= 0x53

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
    acc= (acc* 3.9)/1000

    return acc

def main():
    # init
    init_ADXL345()
    mylcd = LCD.lcd()

    num= input('Select Num= ')

    while ( num != 'q'):
        if (num == '1'):
            #mylcd = LCD.lcd()
            LCD_str= input('char input= ')
            mylcd.lcd_clear()
            mylcd.lcd_display_string("I2C LCD Display",1)
            mylcd.lcd_display_string(LCD_str,2)
            sleep(2)
        elif(num == '2'):
            #init_ADXL345()
            for i in range(3):
                x_acc= ADX_measure_acc(ADX_X_addr)
                y_acc= ADX_measure_acc(ADX_Y_addr)
                z_acc= ADX_measure_acc(ADX_Z_addr)
                print ( 'X= %2.2f' % x_acc, 'Y= %2.2f' % y_acc, 'Z= %2.2f' % z_acc)
                sleep(1)
        sleep(1)
        num= input('Select Num= ')
    print('Program_clse')

if __name__ == '__main__':
    main()