# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x36)

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False
encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = encoder.position

def get_position():
    global last_position
    position = encoder.position
    if abs(position - last_position) < 50:
        last_position = position
        return position
    else:
        return last_position

def is_pressed():
    global button_held
    global button
    if not button.value and not button_held:
        button_held = True
        return True
    return False

def simple_pressed():
    global button_held
    global button
    if not button.value:
        button_held = True
        return True
    return False

def second_pressed():
    global button_held
    global button 
    if not button.value and button_held:
        button_held = False
        return True
    return False

def is_released():
    global button_held
    global button
    if button.value and button_held:
        button_held = False
        return True
    return False
