#!/usr/bin/python
import spidev
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Define GPIO to motor
DC_motor_a = 7
DC_motor_b = 11

GPIO.setup(DC_motor_a, GPIO.OUT)
GPIO.setup(DC_motor_b, GPIO.OUT)

# Define sensor channels
temp_channel = 0

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
delay = 1


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

while (1):
    light_level = ReadChannel(temp_channel)
    if (light_level < 100):
        lcd_string("Store off", LCD_LINE_2)
        GPIO.output(DC_motor_a, True)
        GPIO.output(DC_motor_b, FALSE)
        time.sleep(1)
    else:
        GPIO.output(DC_motor_b, TRUE)
        GPIO.output(DC_motor_a, FALSE)
        time.sleep(1)


