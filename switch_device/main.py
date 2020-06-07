import time
import urequests    # Built into MicroPython
import machine      # Built into MicroPython
from machine import Pin

RED_PIN = Pin(5, Pin.OUT)   # Switch Value 1
GREEN_PIN = Pin(4, Pin.OUT) # Switch Value 0
SWITCH_PIN = Pin(14, Pin.IN)
RECIEVER = "http://192.168.0.106:8080" # Update this with the Reciever's IP Address

def flash_pin(on_pin, off_pin, interval, kill_after=False):
    on_pin.value(1)
    off_pin.value(0)
    time.sleep(interval)

    if kill_after:
        on_pin.value(0)
        time.sleep(interval)

def show_error(status_code):
    if status_code == 400:
        for __ in range(6):
            flash_pin(RED_PIN, GREEN_PIN, 0.5)
            flash_pin(GREEN_PIN, RED_PIN, 0.5)

    elif status_code == 401:
        for __ in range(6):
            flash_pin(RED_PIN, GREEN_PIN, 0.25, kill_after=True)
            flash_pin(RED_PIN, GREEN_PIN, 0.25, kill_after=True)
            flash_pin(GREEN_PIN, RED_PIN, 0.25, kill_after=True)
            flash_pin(GREEN_PIN, RED_PIN, 0.25, kill_after=True)

    elif status_code != 200:
        for __ in range(6):
            flash_pin(RED_PIN, GREEN_PIN, 0.5, kill_after=True)
            flash_pin(RED_PIN, GREEN_PIN, 0.5, kill_after=True)

def send_status():
    path = "off_air"

    if RED_PIN.value() == 1:
        path = "on_air"
    
    try:
        resp = urequests.get("{}/{}".format(RECIEVER, path))
        show_error(resp.status_code)
    except Exception as ex:
        print(ex)
        show_error(-1)

def listen_to_switch():
    last_val = -1

    while(True):
        switch_val = SWITCH_PIN.value()
        
        if switch_val != last_val:
            if switch_val == 1:
                RED_PIN.value(1)
                GREEN_PIN.value(0)
                print("on air")
            else:
                RED_PIN.value(0)
                GREEN_PIN.value(1)
                print("off air")

            last_val = switch_val
            send_status()


def main():
    print("THIS IS THE SWITCHER DEVICE!")
    listen_to_switch()

if __name__ == "__main__":
    main()
