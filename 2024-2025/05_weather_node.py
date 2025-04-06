from machine import Pin, I2C
from spyc_iot import bme280, wifi
import urequests
import time

# Connect to WiFi
spyc_iot.connect_wifi('PYC_IOT', '15092021')

# BME280 and ESP32 are connected using the following pins (I2C Protocol)
#    VIN --- VCC    (3.3V Power)
#    GND --- GND    (GROUND)
#    SCL --- Pin 22
#    SDA --- Pin 21

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

def post_thp():
    try:
        # Initialize BME280 sensor
        bme = bme280.BME280(i2c=i2c)
        # Read sensor data
        thp = bme.read_compensated_data()
        # Prepare payload
        payload = {
            "pyccode": "pyc12345",
            "node_des": "Measured in ITLC",
            "temperature": thp[0],
            "humidity": thp[2],
            "airPressure": thp[1] / 100,
        }
        print(payload)
        # Send POST request
        r = urequests.post("https://iot.spyc.hk/post_thp", json=payload)
        print(r.text)
        r.close()  # Close the response to free memory
    except Exception as e:
        print("Error occurred:", str(e))

# Initial reading
post_thp()

# Main loop with 30-second interval
while True:
    time.sleep_ms(30000)  # Wait 30 seconds
    post_thp()
