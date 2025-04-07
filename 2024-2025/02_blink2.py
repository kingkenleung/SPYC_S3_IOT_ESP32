from machine import Pin
from time import sleep

# Define an I/O device called led
# led is connected to Pin 2; it is an Output device
led = Pin(2, Pin.OUT)

while True:  # Run the following forever
    led.on()
    sleep(0.1)
    led.off()
    sleep(0.1)

# Learning Target 1:
    # Your ESP32 CANNOT multitask
    # When a while-true program is running, you cannot modify any code and run any other code
    # You must first stop the program to do other things (by pressing the red "stop" button on Thonny)
    
# Learning Target 2:
    # Adjust the sleeping time to make different flashing patterns
