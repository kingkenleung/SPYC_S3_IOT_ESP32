from machine import Pin, I2C, Timer
from spyc_iot import bme280

# BME280 and ESP32 are connected using the following pins (I2C Protocol)
#    VIN --- VCC    (3.3V Power)
#    GND --- GND    (GROUND)
#    SCL --- Pin 22
#    SDA --- Pin 21

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

def get_thp(_timer):
    bme = bme280.BME280(i2c=i2c)
    thp = bme.read_compensated_data()
    print(f"Temperature: {thp[0]}")
    print(f"Humidity: {thp[2]}")
    print(f"Air Pressure: {thp[1] / 100}")
    # Try to find the current altitude (in meter) based on the following formula
    # Altitude(m) = 44330 * (1 - (current_pressure / seaLevelPressure)^(1/5.255))
    print()


Timer(1).init(mode=Timer.PERIODIC, period=1000, callback=get_thp)

