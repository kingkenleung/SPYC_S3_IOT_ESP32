
from machine import Pin, SPI, Timer
import time

import spyc_iot

# MAX7219 and ESP32 are connected using the following pins (SPI Protocol)
#    VCC --- VCC    (3.3V Power)
#    GND --- GND    (GROUND)
#    DIN --- Pin 23
#    CS  --- Pin 5
#    CLK --- Pin 18
display = spyc_iot.max7219.Matrix8x8(SPI(2), Pin(5), 4)

# Set the brightness to 1
display.brightness(1)

# Clears the display
display.fill(0)

# The following displays a smiling face, starting at column 16 row 0
# To get your own byte sequence, which is helpful if you want to display another pattern, visit https://xantorohara.github.io/led-matrix-editor/
# and copy the 'hex' value next to the buttons. Replace '3c42818100242400' with your new value (keep the 0x).
display.byte_sequence(0x3c42818100242400, 16, 0)


# This will show everything that is previously requested (e.g. the smiling face), the matrix will not be updated unless display.show() is called
display.show()
time.sleep(0.5)

display.fill(0)

def show_name(_timer):
#     display.scroll_text("Shatin Pui Ying College", 30)
    display.time_dense_and_show("12345")

Timer(1).init(mode=Timer.PERIODIC, period=3000, callback=show_name)



