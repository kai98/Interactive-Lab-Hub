import board
import busio
import adafruit_ssd1306
import time

class OLED:
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)

    """
                OLED 128 x 32
    (0, 0)---------------------------(127, 0)
       |---------------------------------|
    (0, 31)--------------------------(127, 31)
    """

    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
