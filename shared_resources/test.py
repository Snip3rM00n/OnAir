import time

import machine  # Built into MicroPython
from machine import Pin

RED_PIN = Pin(5, Pin.OUT)
GREEN_PIN = Pin(4, Pin.OUT)

def toggle_pin(pin):
    if pin.value() == 0:
        pin.value(1)
    else:
        pin.value(0)

def self_test():
    for __ in range(6):
        toggle_pin(RED_PIN)
        toggle_pin(GREEN_PIN)
        time.sleep(0.5)
    
    RED_PIN.value(0)
    GREEN_PIN.value(0)
