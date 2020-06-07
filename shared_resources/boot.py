import gc
import time
import machine  # Built into MicroPython
import network  # Built into MicroPython
import webrepl  # Built into MicroPython

from test import self_test

webrepl.start()
gc.collect()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

try:
    with open("passwords.txt") as f:
        connections = f.readlines()
except OSError:
    print("No passwords.txt file!")
    connections = []


for connection in connections:
    station, password = connection.split()

    print("Connecting to {}.".format(station))

    sta_if.connect(station, password)

    for i in range(15):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print("Connection could not be made.\n")

self_test()
