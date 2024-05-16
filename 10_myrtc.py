# This is just one of the answers on the implementation of the clock
# Yours can be better than mine

# Packages required for SPI communications and time related functions
from machine import Pin, SPI, Timer, I2C
import time
import spyc_iot

# BME280 and ESP32 are connected using the following pins (I2C Protocol)
#    VIN --- VCC    (3.3V Power)
#    GND --- GND    (GROUND)
#    SCL --- Pin 22
#    SDA --- Pin 21
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)

# Tell ESP32 that our LED matrix (we name it display) is on PIN D5 and there is 4 matrices
display = spyc_iot.max7219.Matrix8x8(SPI(2), Pin(5), 4)

# Set the brightness to 1
display.brightness(1)

# Fill the code here!
# Clears the display
display.fill(0)

# The following displays a smiling face, starting at column 16 row 0
# To get your own byte sequence, which is helpful if you want to display another pattern, visit https://xantorohara.github.io/led-matrix-editor/
# and copy the 'hex' value next to the buttons. Replace '3c42818100242400' with your new value (keep the 0x).
display.byte_sequence(0x3c42818100242400, 16, 0)

# This will show everything that is previously requested (e.g. the smiling face), the matrix will not be updated unless display.show() is called
display.show()

# Connect to Wi-Fi
spyc_iot.connect_wifi('PYC_IOT', '15092021')


# This function displays the current time on the LED matrix
def display_time(_timer):
    # Fill the code here!
    display.fill(0)
    display.str_dense_and_show(spyc_iot.get_time_string(), 0, 0)

# This function synchronizes the clock    
def ntp_sync_time(_timer):
    spyc_iot.sync_time()
    
# This function displays the temperature and humidity data
def display_temp(_timer):
    bme = spyc_iot.bme280.BME280(i2c=i2c)
    thp = bme.read_compensated_data()
    print(f"Temperature: {thp[0]}")
    print(f"Humidity: {thp[2]}")
    display.fill(0)  # this line clears whatever exists on the LED matrix
    display.scroll_text(f"{int(thp[0])}°C {int(thp[1])}%", 70)

def display_date(_timer):
    current_datetime = time.gmtime()
    year = current_datetime[0]
    month = current_datetime[1]
    day = current_datetime[2]
    display.fill(0)
    display.scroll_text(f"{year}.{month}.{day}", 70)
    

# Call this function to sync the clock for the first time
ntp_sync_time(None)

# Here is two timer which will run the function display_time every second (1000 milliseconds) and ntp_sync_time every hour (3600000 milliseconds)
Timer(1).init(mode = Timer.PERIODIC, period = 1000, callback=display_time)
Timer(2).init(mode = Timer.PERIODIC, period = 3600 * 1000, callback=ntp_sync_time)
Timer(3).init(mode = Timer.PERIODIC, period = 20000, callback=display_temp)
Timer(4).init(mode = Timer.PERIODIC, period = 10000, callback=display_date)