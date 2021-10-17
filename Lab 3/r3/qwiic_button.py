import busio
import board
import time
from adafruit_bus_device.i2c_device import I2CDevice
from struct import pack, unpack

DEVICE_ADDRESS = 0x6f  # device address of our button
STATUS = 0x03 # reguster for button status
AVAILIBLE = 0x1
BEEN_CLICKED = 0x2
IS_PRESSED = 0x4

# The follow is for I2C communications
i2c = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(i2c, DEVICE_ADDRESS)

def write_register(dev, register, value, n_bytes=1):
    # Write a wregister number and value
    buf = bytearray(1 + n_bytes)
    buf[0] = register
    buf[1:] = value.to_bytes(n_bytes, 'little')
    with dev:
        dev.write(buf)

def read_register(dev, register, n_bytes=1):
    # write a register number then read back the value
    reg = register.to_bytes(1, 'little')
    buf = bytearray(n_bytes)
    with dev:
        dev.write_then_readinto(reg, buf)
    return int.from_bytes(buf, 'little')

# clear out LED lighting settings. For more info https://cdn.sparkfun.com/assets/learn_tutorials/1/1/0/8/Qwiic_Button_I2C_Register_Map.pdf

def LED_clear():
    write_register(device, 0x1A, 1)
    write_register(device, 0x1B, 0, 2)
    write_register(device, 0x19, 0)

def LED(brightness):
    write_register(device, 0x1A, 1)
    write_register(device, 0x1B, 0, 2)
    write_register(device, 0x19, brightness)

def isPressed():
    btn_status = read_register(device, STATUS)
    return (btn_status&IS_PRESSED) != 0 

# while True:
#     try: 
#         if isPressed():
#             LED_Bright(5)
#             print("pressed")
#         else:
#             LED_Bright(0)
#             print("not pressed")
#         time.sleep(0.1)

#     except KeyboardInterrupt:
#         # on control-c do...something? try commenting this out and running again? What might this do
#         write_register(device, STATUS, 0)
#         break
