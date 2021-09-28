import time
import subprocess
import digitalio
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_apds9960.apds9960
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
i2c = busio.I2C(board.SCL, board.SDA)

# datetime
from datetime import datetime, timezone, date
from astral.sun import sun
from astral import LocationInfo

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

# Proximity Sensor
# sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
# sensor.enable_proximity = True

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

def draw_text_align(min_x, min_y, max_x, max_y, msg, font=font, fill="#FFFFFF"):
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def display_date_time():
    # current_time = strftime("%m/%d/%Y %H:%M:%S")
    padding = 15
    interval = (135 - 2 * padding) / 3
    current_time = utc_to_local(datetime.utcnow())

    draw_text_align(0, padding, 240, padding + interval, current_time.strftime("%m/%d/%Y"), font=font, fill="#FFFFFF")
    draw_text_align(0, padding + interval, 240, padding + 2 * interval, current_time.strftime("%H:%M:%S"), font=font, fill="#FFFFFF")
    draw_text_align(0, padding + 2 * interval, 240, padding + 3 * interval, str(time.tzname[0]), font=font, fill="#FFFFFF")

def tini_bar():
    return

bottom_area = (0, 75, 240, 135)

# Scenarios
class Scenario:
    is_progress = 0
    is_date_time = 1


class AstralClock:
    CheckPoints = {}
    Today = None

    Colormap = {
        'midnight': '#1d3557',
        'dawn': '#FDA396',
        'sunrise': '#E66075',
        'noon': '#FFC061', 
        'sunset': '#FDA396', 
        'evening': '#457b9d', 
    }

    # 6 time slots:
    # midnight - dawn - sunrise - noon - sunset - night - midnight (next day)

    def __init__(self):
        city = LocationInfo("New York City", "New York State", "est", 40.730610, -73.935242)
        self.Today = date.today()
        s = sun(city.observer, date=self.Today)
        for name, t in s.items():
            self.CheckPoints[name] = utc_to_local(t)
        self.CheckPoints['midnight'] = datetime.now().astimezone(tz=None).replace(hour=0, minute=0, second=0, microsecond=0)
    
    def get_fraction(self, pre_time, current, next_time):
        fraction = (current - pre_time).total_seconds() / (next_time - pre_time).total_seconds()
        print(fraction)
        return fraction

    def show_progress_bar(self, timeslot, frac, next_slot):
        timeslot_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        precentage_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

        color = self.Colormap[timeslot]
        draw.rectangle((0, 0, width * frac, height), outline=0, fill=color)

        # timeslot
        draw_text_align(0, 31.5, 240, 67.5, timeslot.upper(), font=timeslot_font)
        # fraction to timeslot
        percentage = "{:.2%}".format(frac)
        msg = percentage + " to " + next_slot.capitalize()

        draw_text_align(0, 67.5, 240, 103.5, msg, font=precentage_font)

        return


    # Hard coded
    def show_progress(self):
        if date.today() != self.Today:
            # update date
            self.Today = date.today()
        current = utc_to_local(datetime.utcnow())

        current_timeslot = None
        pre_time = None
        next_time = None
        # midnight - dawn
        if current < self.CheckPoints['dawn']:
            pre_time = self.CheckPoints['midnight']
            next_time = self.CheckPoints['dawn']
            current_timeslot = "midnight"
            next_slot = 'dawn'

        elif current < self.CheckPoints['sunrise']:
            pre_time = self.CheckPoints['dawn']
            next_time = self.CheckPoints['sunrise']
            current_timeslot = "dawn"
            next_slot = 'sunrise'

        elif current < self.CheckPoints['noon']:
            pre_time = self.CheckPoints['sunrise']
            next_time = self.CheckPoints['noon']
            current_timeslot = "sunrise"
            next_slot = 'noon'

        elif current < self.CheckPoints['sunset']:
            pre_time = self.CheckPoints['noon']
            next_time = self.CheckPoints['sunset']
            current_timeslot = "noon"
            next_slot = 'sunset'

        elif current < self.CheckPoints['dusk']:
            pre_time = self.CheckPoints['sunset']
            next_time = self.CheckPoints['dusk']
            current_timeslot = "sunset"
            next_slot = 'dusk'

        else:
            pre_time = self.CheckPoints['dusk']
            next_time = self.CheckPoints['midnight']
            current_timeslot = "evening"
            next_slot = 'midnight'

        frac = self.get_fraction(pre_time, current, next_time)
        self.show_progress_bar(current_timeslot, frac, next_slot)
        
        # print(self.CheckPoints)

# proximity class
class Proximity: 
    prox_time = 0
    prox_threshold = 5
    duration = 5
    is_prox = False
    scenario = Scenario.is_progress
    sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
    sensor.enable_proximity = True

    def __inti__(self):
        return

    def show_prox(self):
        prox = self.sensor.proximity
        x_min, y_min, x_max, y_max = bottom_area
        draw_text_align(x_min, y_min, x_max, y_max, str(prox), font=font, fill="#FFFFFF")

    def count_prox(self):
        prox = self.sensor.proximity
        current_time = time.time()

        if (prox >= self.prox_threshold):
            self.scenario = Scenario.is_date_time
            self.prox_time = current_time
            self.is_prox = True
        else:
            self.is_prox = False

        if (current_time - self.prox_time > self.duration):
            self.scenario = Scenario.is_progress
        # print(self.is_prox)
        print(self.scenario)

p = Proximity()
astral = AstralClock()

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if p.scenario == Scenario.is_date_time:
        display_date_time()
    else:
        astral.show_progress()

    # p.show_prox()
    p.count_prox()
    # print(time.time())
    # Display image.
    disp.image(image, rotation)
    time.sleep(0.05)
