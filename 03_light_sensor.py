# Import necessary modules from the machine library
from machine import Pin, Timer, ADC

# Light Sensor and ESP32 are connected using the following pins (ADC)
#    OUT --- Pin 32    
#    VCC --- VCC    (3.3V Power)
#    GND --- GND    (GROUND)

# Create an ADC object for reading the light sensor's value
# ADC stands for Analog-to-Digital Converter.
# It's a device or a circuit that converts an analog signal, which can have any value within a range, into a digital value.
brightness = ADC(Pin(32))

# Set the ADC's attenuation to 11dB for full-scale input voltage up to 3.6V
# ADC attenuation refers to the process of reducing the amplitude of the input signal before it is converted to a digital value.
# This is done to ensure that the input signal does not exceed the maximum voltage that the ADC can handle,
# which is crucial for preventing damage to the ADC.
brightness.atten(ADC.ATTN_11DB)

# Define a function to show the current brightness level
def show_brightness(_timer):
    # The ADC value ranges from 0 (dark) to 4095 (very bright)
    # Read the current value from the light sensor and print it
    print(brightness.read())
    
    
# Initialize a Timer object
# Set it to trigger the show_brightness function every 200 milliseconds (0.2 seconds)
Timer(1).init(mode=Timer.PERIODIC, period=200, callback=show_brightness)

