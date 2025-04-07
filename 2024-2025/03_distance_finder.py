# file: 03_distance_finder_advanced.py
from spyc_iot import Ultrasound  # Import the Ultrasound class
from machine import Pin         # Import Pin to control the LED
from time import sleep          # Import sleep for timing control


# HC-SR04 connection
# VCC → 5V Power (VCC)
# Trig → Pin 5
# Echo → Pin 18
# GND → Ground (GND)


# Learning Target 1:
    # Connecting an INPUT device - Ultrasound
    # Connect different pins on ESP32 to differnt pins of the sensor
    
# Set up the ultrasound sensor (trigger_pin sends, echo_pin receives)
sensor = Ultrasound(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

# Set up the LED on Pin 2 as an output device
led = Pin(2, Pin.OUT)

while True:  # Run this loop forever
    distance = sensor.distance_cm()  # Measure distance in centimeters
    print('Distance:', distance, 'cm')  # Show the distance on screen
    
    # Learning Target 2:
        # Control LED blink rate based on distance
        # Understand conditional logic (if-elif-else)
        # The blink rate changes based on distance using if-statements
        # Try changing the blink_delay value to make it blink faster when object is near
    
    if distance < 10:        # Very close (less than 10cm)
        blink_delay = 0.5    
    elif distance < 50:      # Medium range (10cm to 50cm)
        blink_delay = 0.5    
    else:                    # Far (more than 50cm)
        blink_delay = 0.5    
    
    # Blink the LED once with the calculated delay
    led.on()
    sleep(blink_delay)
    led.off()
    sleep(blink_delay)

