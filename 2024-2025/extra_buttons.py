from spyc_iot import FourButtons
import time

def button1_pressed():
    print("Button 1: Starting system!")

def button2_pressed():
    print("Button 2: Stopping system!")

def button3_pressed():
    print("Button 3: Increasing speed!")

def button4_pressed():
    print("Button 4: Decreasing speed!")

custom_pins = [12, 13, 14, 15]  # Using different GPIO pins
bh = FourButtons(custom_pins)

# Register callbacks for each button
bh.register_callback(1, button1_pressed)
bh.register_callback(2, button2_pressed)
bh.register_callback(3, button3_pressed)
bh.register_callback(4, button4_pressed)

# Main loop
while True:
    pressed_button = bh.check_buttons()
    
    if pressed_button is not None:
        # Execute callback function if registered
        if pressed_button in bh.callbacks:
            bh.callbacks[pressed_button]()
        
    
    time.sleep(0.05)  # Prevent CPU overload
