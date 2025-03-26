
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

def show_name(_timer):
    display.scroll_text("Shatin Pui Ying College", 30) # 30 columns per second
#     display.str_dense_and_show("Shatin Pui Ying College")
#     display.scroll_text("23°C 95%")

Timer(1).init(mode=Timer.PERIODIC, period=1000, callback=show_name)





