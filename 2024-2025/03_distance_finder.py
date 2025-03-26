from spyc_iot import Ultrasound
from time import sleep

# Range of Sensor: 2cm to 400cm
sensor = Ultrasound(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

while True:
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
    sleep(0.1)
