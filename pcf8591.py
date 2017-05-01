# PCF8591 driver - 4x AIN, 1x AOUT.
#
# Copyright (c) 2017 Jan A. Humpl <jan.a.humpl@centrum.cz>
#
# Distributed under terms of the MIT license.

from machine import I2C
from machine import Pin

BASE_ADDR = 0x48

CTRL_AUTO_INCREMENT_FLAG = 0x04
CTRL_OUTPUT_ENABLE_FLAG  = 0x40

CTRL_READ  = CTRL_OUTPUT_ENABLE_FLAG | CTRL_AUTO_INCREMENT_FLAG
CTRL_WRITE = CTRL_OUTPUT_ENABLE_FLAG | CTRL_AUTO_INCREMENT_FLAG


i2c = None
device_addr = BASE_ADDR


def init(sda, scl, addr):
    global i2c
    global device_addr

    addr = addr & 0x07
    device_addr = BASE_ADDR | addr

    i2c = I2C(sda=Pin(sda), scl=Pin(scl))


def measure():
    try:
        i2c.writeto(device_addr, bytes({CTRL_WRITE}))
        data = i2c.readfrom(device_addr, 5)
    except:
        data = b'\x00\x00\x00\x00\x00'
        print('ADC reading error.')
    return data[1:5]


def output(value):
    try:
        i2c.writeto(device_addr, bytes({CTRL_WRITE, value}))
    except:
        print('ADC writing error.')
