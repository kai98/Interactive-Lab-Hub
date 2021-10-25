import board
import busio
import adafruit_mpu6050
from time import sleep
from subprocess import Popen, call

i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

def vertical_y():
    x, y, z = mpu.acceleration
    # Gravity of Earth is 9.81. I set the threshold as 8
    # vertical - Up
    if y > 8:
        return 1
    elif y < -8:
        return -1
    else:
        return 0

# while True:
#     # print(mpu.acceleration)
#     x, y, z = mpu.acceleration
#     if y > 9:
#         print("up")
#     elif y < -9:
#         print("down")
#     else:
#         print("nah")
#     sleep(0.1)