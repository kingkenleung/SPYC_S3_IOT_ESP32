from machine import Pin
import time

class FourButtons:
    def __init__(self, pins=[12, 13, 14, 15], debounce_ms=100):
        """Initialize buttons on specified pins with pull-up resistors"""
        self.buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in pins]
        self.callbacks = {}  # Dictionary to store button callbacks
        self.debounce_ms = debounce_ms  # Debounce time in milliseconds
        self.last_press_time = 0  # Track last button press time
        print("Starting button detection...")

    def check_buttons(self):
        """Check which button is pressed and return its number (1-4) or None"""
        current_time = time.ticks_ms()
        
        # Check if enough time has passed since last press (debouncing)
        if time.ticks_diff(current_time, self.last_press_time) < self.debounce_ms:
            return None
            
        for i, button in enumerate(self.buttons, 1):
            if button.value() == 0:  # 0 means pressed (with pull-up)
                self.last_press_time = current_time
                return i    # Return button number (1-4)
        return None  # No button pressed

    def register_callback(self, button_num, callback):
        """Register a callback function for a specific button"""
        self.callbacks[button_num] = callback