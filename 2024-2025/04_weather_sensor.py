from machine import Pin, I2C
import time  # Needed for delay control
from spyc_iot import bme280

# BME280 and ESP32 connection (I2C Protocol)
# VIN → 5V Power (VCC)
# GND → Ground (GND)
# SCL → Pin 22
# SDA → Pin 21

# Initialize I2C communication (bus 0) 
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

# Create BME280 sensor object
bme = bme280.BME280(i2c=i2c)

# Main loop to continuously read sensor data
while True:  # Loop forever
    # Read temperature, humidity, pressure (compensated values)
    thp = bme.read_compensated_data()
    
    # Extract and print values with clear labels
    # thp[0] = temperature (°C), [1] = pressure (Pa), [2] = humidity (%)
    print(f"Temperature: {thp[0]}°C")  # f-string for formatting
    print(f"Humidity: {thp[2]}%")
    print(f"Air Pressure: {thp[1]/100} hPa\n")  # Convert Pascal to hectopascals
    
    time.sleep(1)  # Wait 1 second between readings

