# file: 04_weather_sensor.py
from machine import Pin, I2C    # Import Pin and I2C for hardware control
import time                     # Needed for delay control
from spyc_iot import bme280     # Import the BME280 sensor library

# Learning Target 1:
    # Learn about the BME280 sensor
    # This sensor measures temperature, humidity, and air pressure
    # Does the temperature match what you feel in the room?

    # BME280 and ESP32 connection (I2C Protocol)
    # VIN → 5V Power (VCC)
    # GND → Ground (GND)
    # SCL → Pin 22 (clock line for I2C)
    # SDA → Pin 21 (data line for I2C)

# Initialize I2C communication (bus 0)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)  # Set up I2C with a frequency of 10kHz

# Create BME280 sensor object
bme = bme280.BME280(i2c=i2c)  # Link the sensor to the I2C bus

# Main loop to continuously read sensor data
while True:  # Loop forever
    # Read temperature, humidity, pressure (compensated values)
    thp = bme.read_compensated_data()
    
    # Extract and print values with clear labels
    # thp[0] = temperature (°C), [1] = pressure (Pa), [2] = humidity (%)
    print(f"Temperature: {thp[0]}°C")           # f-string makes the output easy to read
    print(f"Humidity: {thp[2]}%")               # Show humidity as a percentage
    print(f"Air Pressure: {thp[1]/100} hPa\n")  # Convert Pascal to hectopascals (hPa)
    
    time.sleep(1)  # Wait 1 second between readings
    
    
