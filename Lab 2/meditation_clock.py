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

class Stage:
    default = 0
    yes = 1
    notyet = 2
    ongoing = 3
    pause = 4
    cont = 5
    exit = 6
    done = 7

# Helper Functions: 
def clear_image():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def isPressed_A():
    return not buttonA.value

def isPressed_B():
    return not buttonB.value

# Events: 
def next_event(scenario):
    return isPressed_A() and isPressed_B()

def yes_event(scenario):
    return scenario.stage == Stage.default and isPressed_A()

def notyet_event(scenario):
    return scenario.stage == Stage.default and isPressed_B()

def pause_event(scenario):
    return scenario.stage == Stage.yes and isPressed_A()

def continue_event(scenario):
    return scenario.stage == Stage.pause and isPressed_A()

def quit_event(scenario):
    return scenario.stage == Stage.yes and isPressed_B()

# TODO: resolve pause
def done_event(scenario):
    if scenario.stage == Stage.pause:
        return False
    current_time = time.time()
    return current_time - scenario.starttime >= scenario.duration


def draw_text_align(min_x, max_x, min_y, max_y, msg, font=font, fill="#FFFFFF"):
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)
    # print((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2))

class Scenario(object): 
    x_sidebar = 0
    x_content = 67.5
    font = font
    sidebar_color = "#F9F5F5"
    starttime = 0
    duration = 40
    isPause = False
    pausetimestamp = 0

    def __init__(self):
        self.title=input
        self.color=None
        self.greeting="Greeting"
        self.stage=Stage.default

        # self.themeColor="white"

    def show(self):
        if self.stage == Stage.pause:
            self.pause()
        if self.stage == Stage.cont:
            self.go()

        self.display_greeting()
        self.display_sidebar()

    def display_buttons(self, buttonA_text, buttonB_text):
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

        # ButtonA: 
        draw_text_align(self.x_sidebar, self.x_content, 0, height / 2, buttonA_text, font, "black")
        # ButtonB:
        draw_text_align(self.x_sidebar, self.x_content, height / 2, height, buttonB_text, font, "black")

    def yes(self):
        self.stage = Stage.yes
        self.starttime = time.time()
        print("Choose Yes!")


    def display_sidebar(self):
        draw.rectangle((0, 0, self.x_content, height), outline=0, fill=self.sidebar_color)
        if self.stage == Stage.default:
            self.display_buttons("Yes", "Nope")

        if self.stage == Stage.yes or self.stage == Stage.cont:
            self.display_buttons("Pause", "Quit")

        if self.stage == Stage.pause:
            self.display_buttons("Go", "Quit")
        
        
    def pause(self):
        self.pausetimestamp = time.time()

    def go(self):
        self.stage = Stage.cont
        bonustime = time.time() - self.pausetimestamp
        self.duration += bonustime

    def done(self):
        self.stage = Stage.default
        print("Done!")

    def display_themeColor(self):
        draw.rectangle((self.x_content, 0, width, height), outline=0, fill=self.color)

    def display_greeting(self):
        self.display_themeColor()
        draw_text_align(self.x_content, 240, 0, height, self.greeting, font, fill="black")

# Pre-set scenarios
def create_scenarios(type):
    scenario = Scenario()
    if type == "morning":
        scenario.title = 'Morning'
        scenario.color = "#98DB8D"
        scenario.greeting = "Good Morning"
        scenario.stage = Stage.default
    
    if type == "afternoon":
        scenario.title = 'Afternoon'
        scenario.color = "#89B1FF"
        scenario.greeting = "Good Afternoon"
        scenario.stage = Stage.default
    
    if type == "evening":
        scenario.title = 'Evening'
        scenario.color = "#FFC061"
        scenario.greeting = "Good Evening"
        scenario.stage = Stage.default
    return scenario


schedule = ["morning", "afternoon", "evening"]
curr_index = 0
curr_scenario = create_scenarios(schedule[curr_index])

# Event Listening
while True:
    # Draw a black filled box to clear the image.
    clear_image()

    # Switch to the next meditation
    if next_event(curr_scenario):
        print("next_event")
        curr_index = (curr_index + 1) % len(schedule)
        curr_scenario = create_scenarios(schedule[curr_index])

    elif yes_event(curr_scenario):
        print("yes_event")
        curr_scenario.stage = Stage.yes

    elif notyet_event(curr_scenario):
        print("notyet_event")
        curr_scenario.stage = Stage.notyet

    elif pause_event(curr_scenario):
        print("pause_event")
        curr_scenario.stage = Stage.pause
    
    elif continue_event(curr_scenario):
        print("continue_event")
        curr_scenario.stage = Stage.cont

    elif quit_event(curr_scenario):
        print("exit_event")
        curr_scenario.stage = Stage.exit

    elif done_event(curr_scenario):
        print("done_event")
        curr_scenario.stage = Stage.done

    curr_scenario.show()

    # Display image.
    disp.image(image, rotation)
    sleep(0.5)
