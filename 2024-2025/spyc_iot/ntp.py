import ntptime
import time
from machine import RTC

ntptime.host = 'time.cloudflare.com'

def sync_time():
    print('Synchronizing time')
    # Fetch the time from NTP server
    try:
        ntp_time_seconds = ntptime.time()
    except OSError:
        print('Synchronization timeout, retrying')
        ntp_time_seconds = ntptime.time()
    # Conver time in seconds to tuple
    ntp_time_tuple = time.gmtime(ntp_time_seconds)
    # The structure of datetime tuples (RTC and time.gmtime) are different 
    RTC().datetime(ntp_time_tuple[0:3] + (ntp_time_tuple[6] + 1,) + ntp_time_tuple[3:6] + (0,))
    print(f'Time synchronized: {time.gmtime()}')