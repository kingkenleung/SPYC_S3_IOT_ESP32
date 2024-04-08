# Packages required for SPI communications and time related functions
from machine import Pin, SPI, Timer, ADC
import time

import spyc_iot

# Tell ESP32 that our LED matrix (we name it display) is on PIN D5 and there is 4 matrices
display = spyc_iot.max7219.Matrix8x8(SPI(2), Pin(5), 4)

# configure brightness sensor connected to Pin 13
brightness = ADC(Pin(32))
brightness.atten(ADC.ATTN_11DB)

# Set the brightness to 1
display.brightness(15)

# Fill the code here!
# Clears the display
display.fill(0)

# The following displays a smiling face, starting at column 16 row 0
# To get your own byte sequence, which is helpful if you want to display another pattern, visit https://xantorohara.github.io/led-matrix-editor/
# and copy the 'hex' value next to the buttons. Replace '3c42818100242400' with your new value (keep the 0x).
display.byte_sequence(0x3c42818100242400, 16, 0)

# This will show everything that is previously requested (e.g. the smiling face), the matrix will not be updated unless display.show() is called
display.show()

# Connect to Wi-Fi
spyc_iot.connect_wifi('PYC_IOT', '15092021')

def map_range(value, old_min, old_max, new_min, new_max):
       return (value-old_min) / (old_max-old_min) * (new_max-new_min) + new_min

def adjust_brightness(_timer):
    display_brightness = int(map_range(brightness.read(), 0, 4095, 4, 15))
    print(display_brightness)
    display.brightness(display_brightness)

# This function displays the current time on the LED matrix
def display_time(_timer):
    # Fill the code here!
    display.fill(0)
    display.time_dense_and_show(spyc_iot.get_time_string(), 0, 0)

# This function synchronizes the clock    
def ntp_sync_time(_timer):
    # Fill the code here!
    spyc_iot.sync_time()

# Call this function to sync the clock for the first time
ntp_sync_time(None)

# Here is two timer which will run the function display_time every second (1000 milliseconds) and ntp_sync_time every hour (3600000 milliseconds)
Timer(1).init(mode = Timer.PERIODIC, period = 1000, callback=display_time)
Timer(2).init(mode = Timer.PERIODIC, period = 3600 * 1000, callback=ntp_sync_time)
Timer(3).init(mode = Timer.PERIODIC, period = 450, callback=adjust_brightness)


