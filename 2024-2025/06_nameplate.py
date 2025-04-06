from machine import Pin, SPI
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

# Keep running forever
while True:
    display.scroll_text("Hello-World!", 15)
#     display.show_text("00:00:00")


