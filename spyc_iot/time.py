import time

def get_time_string():
    current_time = time.gmtime()
    hour = f'{(current_time[3] + 8) % 24:02}'
    minute = f'{current_time[4]:02}'
    second = f'{current_time[5]:02}'
    
    return f'{hour} {minute} {second}'