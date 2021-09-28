# import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
from time import sleep
import time as time_module
import os

os.environ['TZ'] = 'US/Eastern'
time_module.tzset()
print(time_module.tzname)

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

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

def draw_text_align_in_range(min_x, min_y, max_x, max_y, msg, font=font, fill="#FFFFFF"):
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)
    # print((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2))

def draw_text_align(msg, font=font, fill="#FFFFFF"):
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    min_x, min_y, max_x, max_y = Display.x0, Display.y0, Display.x1, Display.y1
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)
    # print((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2))

def get_current_min():
    real_time = time_module.localtime()
    print(real_time)
    return to_min(real_time[3], real_time[4])

# Classes
class Interaction:
    Default = 0
    A = 1 # Button A
    B = 2 # Button B
    AnB = 3 # Button A & B


def to_min(h, m):
    total_min = h * 60 + m
    return total_min


class Display:
    """
               Adafruit   miniPiTFT 1.14"   240x135

            (x0, y0) ------------------------ (x1, y0)
                |                                 |
    [Button_A]  |         [ Time Slot ]           |
                |                                 |
            (x0, y1) ------------------------ (x1, y1)    
                |                                 |
    [Button_B]  |         [ Remaining ]           |
                |                                 |
            (x0, y2) ------------------------ (x1, y2)

    """
    x0, x1 = 0, 240
    y0, y1, y2 = 0, 67.5, 135

    def time_slot(self, in_text):
        draw_text_align_in_range(self.x0, self.y0, self.x1, self.y1 + 20, in_text)

    def remaining(self, in_text):
        draw_text_align_in_range(self.x0, self.y1 - 20, self.x1, self.y2, in_text)

    def background(slef, width, color):
        draw.rectangle((0, 0, width, 135), outline=0, fill=color)

display = Display()

class TimeSlot:
    color = "White"
    title = "Truman Clock"
    greeting = "Hi Truman"
    start_time = 0
    end_time = 100
    word_color = "White"
    # background_color = "Black"

    def __init__ (self):
        return

    def in_range(self, in_time):
        # if in range
        if self.start_time <= self.end_time:
            return self.start_time <= in_time < self.end_time
        return self.start_time <= in_time or in_time < self.end_time

    def get_width(self, in_time):

        # Get the length of pixel 
        # in_min = in_time
        # start_min = self.start_time
        # end_min = self.end_time

        # if start_min < in_min: 
        #     w = 240 * (end_min - in_min) / (end_min - start_min)
        # elif in_min < end_min: 
        #     w = 240 * (end_min - in_min) / (end_min + 1440 - start_min)
        return 240 * self.get_percentage(in_time)

    def get_percentage(self, in_time):
        in_min = in_time
        start_min = self.start_time
        end_min = self.end_time

        if in_min == start_min:
            return 1.00

        if start_min < in_min: 
            percentage = (end_min - in_min) / (end_min - start_min)
        # elif in_min < end_min: 
        #     percentage = (end_min - in_min) / (end_min + 1440 - start_min)
        else:
            percentage = (in_min - start_min) / (end_min - start_min)
        
        if percentage > 1:
            return 1
        return percentage

    def show(self, in_time):
        clear_image()
        self.show_background(in_time)
        self.show_greeting()
        self.show_percentage(in_time)
        # Display Text

    def show_background(self, in_time):
        w = self.get_width(in_time)
        print("W" , w)
        print(self.color)
        display.background(w, self.color)

    def show_greeting(self):
        display.time_slot(self.greeting)
        # draw_text_align(self.greeting)

    def show_percentage(self, in_time):
        percentage = "{0:.2%}".format(self.get_percentage(in_time))
        
        print(percentage)
        display.remaining(percentage)
        # draw_text_align(percentage)


# Morning
MORNING = TimeSlot()
MORNING.color = "#98DB8D"
MORNING.title = "morning"
MORNING.greeting = "Good Morning!"
MORNING.start_time = to_min(6, 0)
MORNING.end_time = to_min(12, 0)

# Afternoon
AFTERNOON = TimeSlot()
AFTERNOON.color = "#FFC061"
AFTERNOON.title = "afternoon"
AFTERNOON.greeting = "Good Afternoon!"
AFTERNOON.start_time = to_min(12, 0)
AFTERNOON.end_time = to_min(18, 0)

# Evening
EVENING = TimeSlot()
EVENING.color = "#4F8AFF"
EVENING.title = "evening"
EVENING.greeting = "Good Evening!"
EVENING.start_time = to_min(18, 0)
EVENING.end_time = to_min(0, 0)

# Night
NIGHT = TimeSlot()
NIGHT.color = "#8254BD"
NIGHT.title = "night"
NIGHT.greeting = "Good Night!"
NIGHT.start_time = to_min(0, 0)
NIGHT.end_time = to_min(6, 0)

VOIDTIME = TimeSlot()

# Default Settings
TIME_SLOTS = [MORNING, AFTERNOON, EVENING, NIGHT]


def get_slot(in_time):
    for t in TIME_SLOTS:
        if t.in_range(in_time):
            return t
    return VOIDTIME

# Run it!

def show_info(_time):
    curr_slot = get_slot(_time)
    curr_slot.show(_time);
    # Display image.
    disp.image(image, rotation)

is_real = True
sleep_time = 0.2
fake_time = 0
while True:
    # Draw a black filled box to clear the image.

    # check buttons:
    if isPressed_A():
        # switch between real and fake time
        is_real = not is_real
    
    if isPressed_B():
        fake_time = (fake_time + 5) % (24 * 60)

    # clear_image()
    if is_real:
        time = get_current_min()
    else:
        time = fake_time
    print(time)
    show_info(time)

    sleep(sleep_time)




    