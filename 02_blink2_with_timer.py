from machine import Pin, Timer
from time import sleep

led = Pin(2, Pin.OUT)

def blink(_timer):
    led.on()
    sleep(0.1)
    led.off()
    sleep(0.1)

Timer(1).init(mode = Timer.PERIODIC, period = 100, callback=blink)



