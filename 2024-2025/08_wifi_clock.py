# Packages needed for SPI (to talk to the LED matrix) and time functions
from machine import Pin, SPI
import time

import spyc_iot

# Set up our LED matrix display (we call it 'display') on PIN D5 with 4 matrices
display = spyc_iot.max7219.Matrix8x8(SPI(2), Pin(5), 4)

# Set brightness to 1 (0 is dimmest, 15 is brightest)
display.brightness(1)

# Clear the display (turn off all LEDs)
display.fill(0)

# Use this tool to create new patterns
# https://aero.pyc.edu.hk/~lkh1/matrix.html
display.byte_sequence(0x3c42818100242400, 16, 0)

# Actually show everything we set up on the LED matrix
display.show()

# Connect to Wi-Fi network named 'KL' with password 'duckduckduck0315'
spyc_iot.connect_wifi('PYC_IOT', '15092021')

# Sync the clock with internet time right away
spyc_iot.sync_time()

# Keep track of time for our loops
last_time_update = time.time()  # When we last showed the time
last_ntp_sync = time.time()     # When we last synced with internet time

# Main loop that runs forever
while True:
    # Get current time in seconds
    current_time = time.time()
    
    # Check if 1 second has passed since last time display
    if current_time - last_time_update >= 1:
        # Clear the display
        display.fill(0)
        # Show the current time as text starting at column 0, row 0
        display.show_text(spyc_iot.get_time_string(), 0, 0)
        # Remember when we updated the time display
        last_time_update = current_time
    
    # Check if 1 hour (3600 seconds) has passed since last internet time sync
    if current_time - last_ntp_sync >= 3600:
        # Sync the clock with internet time
        spyc_iot.sync_time()
        # Remember when we synced the time
        last_ntp_sync = current_time
    
    # Small delay so we don't check too often and use less power
    time.sleep(0.1)
