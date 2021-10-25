import Gyro as gyro 
import miniPiTFT as tft
import SandDisplay as display
import RotaryEncoder as rotery
import time

class SandGlass:
    # 5 min
    max_time = 30
    coe = 0.5
    mid = 64

    right_amount = 0
    prev_time = None
    # direction: -1, 0, 1
    prev_direction = 0

    prev_vertical = 1

    def __init__(self):
        self.prev_time = time.time() 

    def draw_amount(self, is_right=True):
        right_amount = self.right_amount
        max_time = self.max_time
        right_pix = int((right_amount / max_time) * self.coe * self.mid)
        left_pix = int(self.coe * self.mid - right_pix)
        if is_right:
            display.rectangle(127 - right_pix, 127)
            display.rectangle(63 - left_pix, 63)
        else:
            display.rectangle(64, 64 + right_pix)
            display.rectangle(0, left_pix)

    def displaySandGlass(self):
        display.clear()

        current_direction = gyro.vertical_y()
        current_time = time.time()
        prev_direction = self.prev_direction
        prev_time = self.prev_time

        if current_direction != 0:
            # draw sand line
            if prev_direction == 0:
                display.startSandDrop()
            print("yes")
            display.sandDrop(current_direction == 1)
        
        if current_direction == 0:
            display.stopSandDrop()
            self.draw_amount(self.prev_vertical == 1)
            
            # Enter setting mode:
            if rotery.simple_pressed():
                self.setCountdown()
                time.sleep(0.5)

        diff_time = current_time - prev_time

        if current_direction == 1:
            self.right_amount += diff_time
            self.right_amount = min(self.right_amount, self.max_time)
            if self.right_amount == self.max_time:
                display.stopSandDrop()
            self.draw_amount(current_direction == 1)


        elif current_direction == -1:
            self.right_amount -= diff_time
            self.right_amount = max(self.right_amount, 0)
            if self.right_amount == 0:
                display.stopSandDrop()
            self.draw_amount(current_direction == 1)


        self.prev_direction = current_direction
        self.prev_time = current_time

        if current_direction == 1:
            self.prev_vertical = 1
        if current_direction == -1:
            self.prev_vertical = -1

        display.drawSandGlass()
        display.show()

    def setCountdown(self):
        prev_position = rotery.get_position()
        updated_time = self.max_time
        while True:
            position = rotery.get_position()
            diff = position - prev_position
            prev_position = position
            updated_time += diff
            updated_time = max(updated_time, 0)
            
            msg = "Timer: {}\"{}\'".format(updated_time // 60, updated_time % 60)
            print(msg)
            display.text(msg)
            # and display something
            if rotery.simple_pressed():
                break
            time.sleep(0.05)
            
        self.max_time = updated_time
        self.right_amount = 0
        time.sleep(0.5)

sg = SandGlass()
while True:
    sg.displaySandGlass()

# display.drawSandGlass()
# display.sandDrop()
# while True:
#     display.sandDrop()
#     display.show()