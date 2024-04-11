from machine import Pin, I2C, Timer
from spyc_iot import bme280, wifi
import urequests

# Connect to WiFi
wifi.connect_wifi("PYC_IOT", "15092021")

# BME280 and ESP32 are connected using the following pins (I2C Protocol)
#    VIN --- VCC    (3.3V Power)
#    GND --- GND    (GROUND)
#    SCL --- Pin 22
#    SDA --- Pin 21

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)


def post_thp(_timer):
    bme = bme280.BME280(i2c=i2c)
    thp = bme.read_compensated_data()
    payload = {
        "location": "XXXXXXX",
        "node_des": "created by XXXXXXXX",
        "temp": thp[0],
        "humidity": thp[2],
        "airPressure": thp[1] / 100,
    }
    print(payload)
    r = urequests.post("https://iot.spyc.hk/post_thp", json=payload)
    print(r.text)


Timer(1).init(mode=Timer.PERIODIC, period=30000, callback=post_thp)
