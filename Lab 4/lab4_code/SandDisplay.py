import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

"""
              OLED 128 x 32
 (0, 0)---------------------------(127, 0)
    |--------------------------------|
 (0, 31)--------------------------(127, 31)
"""

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# draw = ImageDraw.Draw(image)

font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

def text(msg):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)    
    draw.text((0, 0), msg, font=font2, fill=1)
    oled.image(image)
    print("draw msg ", msg)
    oled.show()

def drawSandGlass():
    lx, ly = 63, 11
    ry = 20
    # oled.pixel(63, 13, 1)
    # mid point
    # oled.pixel(63, 15, 1)
    lineSet = set()

    # oled.fill(1)

    for i in reversed(range(0, ly + 1)):
        x1, x2, y1, y2 = lx - i, lx + i, ly - i, ry + i
        oled.pixel(x1, y1, 1)
        oled.pixel(x2, y1, 1)
        oled.pixel(x1, y2, 1)
        oled.pixel(x2, y2, 1)

        for j in range(0, y1 - 1):
            oled.pixel(x1, j, 0)
            oled.pixel(x2, j, 0)
        
        for j in range(y2 + 1, 32):
            oled.pixel(x1, j, 0)
            oled.pixel(x2, j, 0)

        lineSet.add((x1, y1))
        lineSet.add((x1, y2))
        lineSet.add((x2, y1))
        lineSet.add((x2, y2))
    
    for i in range(0, 52):
        oled.pixel(i, 0, 1)
        oled.pixel(i, 31, 1)
        lineSet.add((i, 0))
        lineSet.add((i, 31))

    for i in range(74, 128):
        oled.pixel(i, 0, 1)
        oled.pixel(i, 31, 1)
        lineSet.add((i, 0))
        lineSet.add((i, 31))
    
    for j in range(0, 32):
        oled.pixel(0, j, 1)
        oled.pixel(127, j, 1)
        lineSet.add((0, j))
        lineSet.add((127, j))

    for i in range(0, 128):
        for j in range(0, 32):
            if (i, j) in lineSet:
                continue
            if (i, j - 1) in lineSet or (i, j + 1) in lineSet \
            or (i - 1, j) in lineSet or (i + 1, j) in lineSet:
                oled.pixel(i, j, 0)

    oled.show()
mid_x = 63
mid_y = 15
first_sand = mid_x
start_time = time.time()
sand_direction = True
time_interval = 0.1
point_interval = 5

def show():
    oled.show()

def clear():
    oled.fill(0)

def startSandDrop():
    global first_sand
    global start_time 
    start_time= time.time()
    first_sand = mid_x
    start_time = time.time()
    # True direction: positive direction. 

def sandDrop(positive_direction=True):
    now = time.time()
    if positive_direction:

        first_sand = mid_x + int((now - start_time) // time_interval) 
        print(first_sand)
        modx = first_sand % point_interval
        first_sand = first_sand if first_sand < 128 else 127 - modx
        for i in range(first_sand, mid_x, -1):
            if i % point_interval == modx:
                oled.pixel(i, mid_y, 1)
            else:
                oled.pixel(i, mid_y, 0)
        # oled.pixel(63, 15, 1)
    else:
        first_sand = mid_x +-int((now - start_time) // time_interval) 
        print(first_sand)
        modx = first_sand % point_interval
        first_sand = first_sand if first_sand > 0 else modx
        for i in range(first_sand, mid_x, 1):
            if i % point_interval == modx:
                oled.pixel(i, mid_y, 1)
            else:
                oled.pixel(i, mid_y, 0)

def stopSandDrop():
    for i in range(0, 127):
        oled.pixel(i, mid_y, 0)

def rectangle(x_min, x_max):
    for i in range(x_min, x_max + 1):
        for j in range(0, 32):
            oled.pixel(i, j, 1)

# def SandGlass(precent, direction=Positive):
#     if direction:



# start with a blank screen
# oled.fill(0)
# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
# oled.show()

# oled.pixel(0, 0, 1)

# sandDrop()
# drawSandGlass()
# oled.show()

# while True:
#     sandDrop(False)
#     drawSandGlass()
#     oled.show()
