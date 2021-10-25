import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
default_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Buttons
# these setup the code for our buttons 
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


"""
            Adafruit   miniPiTFT 1.14"   240x135

        (x0, y0) --------(x1, y0)-------- (x2, y0)
            |                |                |
[Button_A]  |                |                |
            |                |                |
        (x0, y1) --------(x1, y1)-------- (x2, y1)    
            |                |                |
[Button_B]  |                |                |
            |                |                |
        (x0, y2) --------(x1, y2)-------- (x2, y2)

"""
x0, x1, x2 = 0, 120, 240
y0, y1, y2 = 0, 67.5, 135

# Button A is pressed
def is_A():
    return not buttonA.value

# Button B is pressed
def is_B():
    return not buttonB.value

def is_AB():
    return is_A() and is_B()

# Customized Functions: 
def text_center(msg, min_x=x0, min_y=y0, max_x=x2, max_y=y2, font=default_font, fill="#FFFFFF", clear=False):
    #FFFFFF -> White color
    if clear:
        clear()
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)
    display_image()

def text_top(msg, font=default_font, fill="#FFFFFF"):
    clear(min_x=x0, min_y=y0, max_x=x2, max_y=y1)
    text_center(msg, min_x=x0, min_y=y0, max_x=x2, max_y=y1, font=font, clear=False)

def text_bottom(msg, font=default_font, fill="#FFFFFF"):
    clear(min_x=x0, min_y=y1, max_x=x2, max_y=y2)
    text_center(msg, min_x=x0, min_y=y1, max_x=x2, max_y=y2, font=font, clear=False)

# Helper Functions: 
def clear(min_x=x0, min_y=y0, max_x=x2, max_y=y2):
    draw.rectangle((min_x, min_y, max_x, max_y), outline=0, fill=0)

def display_image():
    # Display image.
    disp.image(image, rotation)

def get_font(fontsize=24):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

# Pass the main function as action, auto execute every interval time. 
def looper(action, interval=0.5):
    while True:
        clear()
        action()
        display_image()
        time.sleep(interval)