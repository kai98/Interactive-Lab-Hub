import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from adafruit_rgb_display.rgb import color565

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# these setup the code for our buttons 
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# ----

# Helper Functions: 
def clear_image():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def isPressed_A():
    return not buttonA.value

def isPressed_B():
    return not buttonB.value

# Classes
class Interaction:
    Default = 0
    A = 1 # Button A
    B = 2 # Button B
    AnB = 3 # Button A & B

class State:
    Default = 0
    Start = 1
    On = 2
    Wait = 3
    Pause = 4
    Resume = 5
    Next = 6
    Done = 7

class Meditation():
    title = "Title"
    greeting = "Hi"
    themeColor = "White"
    duration = 30
    pause_offset = 0
    start_time = 0
    is_pause = False
    state = State()

    def __init__(self):
        self.state = State.Default
    
class Content:
    sidebar = SideBar()
    main_content = Main_Content()
    class SideBar:
        
        def __init__(self, button_A, interaction_A, button_B, interaction_B):
            self.state = State.Default


    def __init__(self):
        self.state = State.Default


class Display:
    """
               Adafruit   miniPiTFT 1.14"   240x135

            (x0, y2) --- (x1, y2) ----------- (x2, y2)
                |            |                   |
    [Button_A]  |            |                   |
                |            |                   |
            (x0, y1) --- (x1, y1) ----------- (x2, y1)
                |            |                   |
    [Button_B]  |            |                   |
                |            |                   |
            (x0, y0) --- (x1, y0) ----------- (x2, y0)

                   [SIDEBAR]     [MAIN_SCREEN]  
    """
    x0, x1, x2 = 0, 67.5, 240
    y0, y1, y2 = 0, 67.5, 135

 
    class SideBar:
        def show():
            return

        def control():
            return
        
        def label():
            return
        
    class MainScreen: 
        def show():
            return


