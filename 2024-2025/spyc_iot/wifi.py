import network
from time import sleep

station = network.WLAN(network.STA_IF)

from time import sleep

def load_scene():
    for i in range(1, 8):
        msg = 'Connecting WiFi' + '.' * i
        print(msg, end='')
        sleep(0.2)
        print('\r' + ' ' * len(msg), end='\r')


def connect_wifi(ssid, pw):
    if station.isconnected():
        print(f'Already connected on {station.ifconfig()}, skipping')
        return
    
    print('Initializing WLAN')
    station.active(True)
    print('Initialization of WLAN completed')

    station.connect(ssid, pw)
    while not station.isconnected():
        load_scene()

    print(f'\nWiFi Connected on {station.ifconfig()}')
